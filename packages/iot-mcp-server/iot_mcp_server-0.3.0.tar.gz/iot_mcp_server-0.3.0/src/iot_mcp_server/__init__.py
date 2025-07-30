from .server import mcp

def main():
    """Main entry point for the iot-mcp-server package"""
    print("Starting iot-mcp-server v0.3.0")
    mcp.run()