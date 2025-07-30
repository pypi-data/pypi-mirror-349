
commands
====
uv init --package iot-mcp-server
cd iot-mcp-server
uv add "mcp[cli]"
uv add pyjwt
uv add requests

uv run mcp install server.py # install to Claude Desktop
uv run mcp dev server.py     # debug
uv run mcp run server.py     # run
uv run main.py               # test main.py without mcp

uv run mcp install server.py --with requests --with pyjwt --env-var BASE_URL=https://iot-api.quectelcn.com --env-var ACCESS_KEY=24b9zq36CtkVFHSiBW9aMeLF --env-var ACCESS_SECRET=6AUSH6PmD22dYjMLonHuiKEp5S83GkQ83epBbDqG

sample prompt
====
List product from IoTCloud.
请列出我在IoTCloud上的所有产品。

Get the full product definition of the Light1 
product.
找到产品Light1的productKey并据此获取它的完整定义。

Get the productKey of product Light1 and use it to list devices of the product.

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
        "ACCESS_KEY": "24b9zq36CtkVFHSiBW9aMeLF",
        "ACCESS_SECRET": "6AUSH6PmD22dYjMLonHuiKEp5S83GkQ83epBbDqG"
      }
    }
  }
}


