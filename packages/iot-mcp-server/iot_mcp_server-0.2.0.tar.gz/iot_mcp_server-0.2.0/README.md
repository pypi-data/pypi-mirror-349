sample config.json
====
{
  "globalShortcut": "",
  "mcpServers": {
    "IoTCloud": {
      "command": "C:\\Users\\gatem\\.local\\bin\\uv.EXE",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "pyjwt",
        "--with",
        "requests",
        "mcp",
        "run",
        "C:\\Users\\gatem\\app\\mcp-server-demowin\\server.py"
      ],
      "env": {
        "BASE_URL": "https://iot-api.quectelcn.com",
        "ACCESS_KEY": "YOUR_ACCESS_KEY_HERE",
        "ACCESS_SECRET": "YOUR_ACCESS_SECRET_HERE"
      }
    }
  }
}
