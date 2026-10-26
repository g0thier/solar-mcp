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
    uv_index: float
    ozone: float

class UVResponse(BaseModel):
    longitude: float
    latitude: float
    infos: List[UVInfo]

# Initialize FastMCP server
mcp = FastMCP(
    name="🔆 Solar MCP",
    instructions="This API provides the UV index and ozone concentration for your location.",
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
    Retrieve UV index data for a week for a specified location.

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
