from .server import mcp

def main():
    """Main entry point for the iot-mcp-server package"""
    print("Starting iot-mcp-server v0.2.4")
    mcp.run()