from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel, Field
import custom

class UVInfo(BaseModel):
    date: int
    uv_index: float = Field(description="Clear-sky UV index forecast.")
    ozone: float = Field(description="Total ozone column in Dobson units (DU).")

class UVResponse(BaseModel):
    longitude: float
    latitude: float
    infos: List[UVInfo]

# Initialize FastMCP server
mcp = FastMCP(
    name="🔆 Solar MCP",
    instructions="TEMIS forecasts of clear-sky UV index and total ozone in DU for your location.",
    version="1.0.0",
)

# Load HTML content for homepage
try:
    with open("index.html", "r", encoding="utf-8") as html_file:
        html_content = html_file.read()
except FileNotFoundError:
    html_content = "<html><body><h1>🔆 Solar MCP</h1><p>Homepage content not available.</p></body></html>"

# Define homepage and MCP tool
@mcp.custom_route("/", methods=["GET"])
async def homepage(request: Request):
    """
    Serve the HTML homepage.

    Returns:
        HTMLResponse: The content of the homepage.
    """
    return HTMLResponse(content=html_content)

@mcp.tool(tags={"UV Data"})
def get_uv_week(
    longitude: Annotated[float, Field(description="Longitude of the location.")] = 6.132936441,
    latitude: Annotated[float, Field(description="Latitude of the location.")] = 46.220473615,
) -> UVResponse:
    """
    Retrieve weekly TEMIS forecasts: clear-sky UV index and total ozone column in Dobson units (DU).

    Args:
        longitude (float): The longitude of the location.
        latitude (float): The latitude of the location.

    Returns:
        UVResponse: UV index data for the specified location.
    """
    return UVResponse(**custom.request_uv_week(longitude, latitude))

app = mcp.http_app(middleware=[
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["mcp-session-id"],
    )
])
