import os
from datetime import date

import netCDF4
import requests
from bs4 import BeautifulSoup

def get_ilon(lon):
    """
    Calculate the index of a given longitude on a 1440-point grid.

    Args:
        lon (float): The longitude value to be converted. It should be in the
                     range of -180 to 180 degrees.

    Returns:
        int: The index corresponding to the given longitude on the 1440-point grid.
    """
    dlon = 360.0 / 1440.0
    return int(round((lon + 180.0 - dlon / 2.0) / dlon))

def get_ilat(lat):
    """
    Calculate the index of a given latitude in a grid.

    Args:
        lat (float): The latitude value to be converted to an index.
                     It should be in the range of -90 to 90 degrees.

    Returns:
        int: The index corresponding to the given latitude in the grid.
    """
    dlat = 180.0 / 720.0
    return int(round((lat + 90.0 - dlat / 2.0) / dlat))

def get_dict(lon, lat, nc_file):
    """
    Extract and return a dictionary containing UV index and ozone information
    for a given longitude and latitude from a netCDF file.

    Args:
        lon (float): Longitude of the location.
        lat (float): Latitude of the location.
        nc_file (str): Path to the netCDF file.

    Returns:
        dict: A dictionary with the following structure:
            {
                "longitude": lon,
                "latitude": lat,
                "infos": [
                    {
                        "date": date,
                        "uv_index": uv_index,
                        "ozone": ozone
                    },
                    ...
                ]
            }
    """
    ilon = get_ilon(lon)
    ilat = get_ilat(lat)

    data = {
        "longitude": lon,
        "latitude": lat,
        "infos": []
    }

    with netCDF4.Dataset(nc_file, 'r') as nc:
        dates = nc.groups['PRODUCT'].variables['date'][:]
        n_days = len(dates)

        uvief = nc.groups['PRODUCT'].variables['uvi_clear'][:, ilat, ilon]
        ozone = nc.groups['PRODUCT'].variables['ozone_column'][:, ilat, ilon]

    for i_day in range(n_days):
        data["infos"].append({
            "date": dates[i_day],
            "uv_index": uvief[i_day],
            "ozone": ozone[i_day]
        })

    return data

def get_first_nc_link(url="https://www.temis.nl/uvradiation/nrt/uvindex.php"):
    """
    Retrieve the first link containing a .nc file from a given URL.

    Args:
        url (str): The URL to fetch and parse.
                   Defaults to "https://www.temis.nl/uvradiation/nrt/uvindex.php".

    Returns:
        str: The absolute URL of the first .nc file found, or None if no such file is found or an error occurs.
    """
    try:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        for link in soup.find_all('a', href=True):
            if link['href'].endswith('.nc'):
                return requests.compat.urljoin(url, link['href'])
    except Exception as e:
        print(f"Error: {e}")
    return None

def download(path, url):
    """
    Download a file from the given URL and save it to the specified local path.

    Args:
        path (str): The local file path where the downloaded file will be saved.
        url (str): The URL of the file to be downloaded.

    Raises:
        requests.exceptions.RequestException: If there is an error during the HTTP request.
        Exception: If there is an error while saving the file.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(path, "wb") as file:
            file.write(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Error during file download: {e}")
    except Exception as e:
        print(f"Error saving the file: {e}")

def get_data():
    """
    Retrieve the path to a NetCDF file for the current date.

    Returns:
        str: The file path to the NetCDF file for the current date.
    """
    
    # Répertoire où les données seront enregistrées (volume monté)
    data_dir = "/app/data"
    date_today = date.today().strftime("%Y%m%d")

    directory = os.path.join(data_dir, 'DOWNLOAD', date_today)
    path_nc = os.path.join(directory, 'uvief_fc.nc')

    if not os.path.exists(path_nc):
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory: {e}")

        nc_link = get_first_nc_link()
        download(path_nc, nc_link)

    return path_nc

def request_uv_week(lon, lat):
    """
    Request UV index data for a week for the given longitude and latitude.

    Args:
        lon (float): The longitude of the location.
        lat (float): The latitude of the location.

    Returns:
        dict: A dictionary containing the UV index data for the specified location and time period.
    """
    path_nc = get_data()
    return get_dict(lon, lat, path_nc)
