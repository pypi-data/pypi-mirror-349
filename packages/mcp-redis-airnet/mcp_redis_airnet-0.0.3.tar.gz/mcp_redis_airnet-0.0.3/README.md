# mcp-redis-airnet: A Redis MCP Server for AirNet 
# purpose：base mcp-server-redis add tools get_info、get_list、get_dbsize...
## Chagne-Tip:
### version = "0.0.1"
  1、__main__.py & __init__.py invalid syntax：from mcp-redis-airnet import main Revise to from mcp_redis_airnet import main
  2、add tools `get_info`: Get Redis server information
### version = "0.0.2"
  1、add tools `get_list`: Get client connection list using Redis CLIENT LIST command
### version = "0.0.3"
  1、add tools `get_dbsize`: Get the number of keys in the current database

---

> The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) is an open protocol that enables seamless integration between LLM applications and external data sources and tools. Whether you're building an AI-powered IDE, enhancing a chat interface, or creating custom AI workflows, MCP provides a standardized way to connect LLMs with the context they need.

This repository is an example of how to create an MCP server for managing Redis data.

[![PyPI version](https://badge.fury.io/py/mcp-redis-airnet.svg)](https://pypi.org/project/mcp-redis-airnet/)

## Overview

A Model Context Protocol server for interacting with Redis. It provides tools for setting, retrieving, listing, and deleting keys in Redis.

## Components

### Tools

The server implements the following tools:

- `set_value`: Set a specified key to a given value
  - Takes a `key` (string) and a `value` (string)
  - Returns a confirmation message upon success

- `get_value`: Retrieve the value of a specified key
  - Takes a `key` (string)
  - Returns the value as a string, or `None` if the key does not exist

- `list_keys`: List Redis keys matching a given pattern
  - Takes a `pattern` (default: "*")
  - Returns a list of matching keys

- `delete_key`: Delete a specified key
  - Takes a `key` (string)
  - Returns the number of keys deleted (0 or 1)

- `get_info`: Get Redis server information
  - Returns Redis server information

- `get_list`: Get client connection list using Redis CLIENT LIST command
  - Returns client connection list

- `get_dbsize`: Get the number of keys in the current database
  - Return redis_client.dbsize()

## Configuration

The server connects to Redis using the following environment variables (all are required):

- `REDIS_HOST`: Redis host  
- `REDIS_PORT`: Redis port  
- `REDIS_DB`: Redis database number  
- `REDIS_PASSWORD`: Redis password  

If any of these variables are missing, the server will raise an error during startup. Make sure to set each of these before running the server.

## Quickstart

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`  
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "redis": {
    "command": "uvx",
    "args": [
      "mcp-redis-airnet"
    ]
  }
}
```
#### Trae Desktop
```json
{
  "mcpServers": {
    "redis-airnet": {
      "command": "uvx",
      "args": [
        "--from",
        "mcp-redis-airnet==0.0.3",
        "--refresh-package",
        "mcp-redis-airnet",
        "mcp-redis-airnet"
      ],
      "env": {
        "REDIS_HOST": "192.168.31.158",
        "REDIS_PORT": "6379",
        "REDIS_DB": "0",
        "REDIS_PASSWORD": "cdatc"
      }
    }
  }
}
```
本地调试运行
```json
{
  "mcpServers": {
    "redis-debug": {
      "command": "uv",
      "args": [
        "--directory",
        "E:\\技术支持室\\Trae\\redis-AirNet\\src\\mcp_redis_airnet\\",
        "run",
        "server.py"
      ],
      "env": {
        "REDIS_HOST": "192.168.31.158",
        "REDIS_PORT": "6379",
        "REDIS_DB": "0",
        "REDIS_PASSWORD": "cdatc"
      }
    }
  }
}
```

## Development

### Building and Publishing

To prepare the package for distribution:
python -m venv .venv
.venv\Scripts\activate
python -m ensurepip --upgrade
python -m pip install --upgrade pip
pip install twine
twine check dist/*
	Checking dist\mcp_redis_airnet-1.0.1-py3-none-any.whl: PASSED
	Checking dist\mcp_redis_airnet-1.0.1.tar.gz: PASSED
  
1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
uv publish --token pypi-Ag...
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD` （PyPI已经移除了对用户名/密码认证的支持）

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory $(PWD) run mcp-redis-airnet
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.