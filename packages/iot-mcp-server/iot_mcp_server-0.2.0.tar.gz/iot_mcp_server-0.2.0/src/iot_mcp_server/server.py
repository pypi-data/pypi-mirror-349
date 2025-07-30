import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from iot_mcp_server import util

# Load environment variables
load_dotenv()

# Create an MCP server
mcp = FastMCP("IoT MCP Server")

@mcp.tool()
def list_products() -> str:
    """List products"""
    products = util.list_products()
    return products

@mcp.tool()
def get_product_definition(product_key: str) -> str:
    """Get product TSL definition by productKey"""
    tsl_json = util.get_product_tsl_json(product_key)
    return tsl_json

@mcp.tool()
def list_devices(product_key: str) -> str:
    """List devices in product which is specified by productKey"""
    devices = util.list_devices(product_key)
    return devices
