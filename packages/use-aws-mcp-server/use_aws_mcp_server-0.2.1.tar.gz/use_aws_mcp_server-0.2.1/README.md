# use-aws-mcp-server

MCP server that provides AWS CLI integration for AI assistants, enabling execution of AWS API calls with proper parameter validation and error handling.

## Features

- Execute AWS CLI commands through an MCP server interface
- Support for all AWS services and operations
- Parameter validation and error handling

## Prerequisites

### Installation Requirements

1. Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/) or the [GitHub README](https://github.com/astral-sh/uv#installation)
2. Install Python 3.10 or newer using `uv python install 3.10` (or a more recent version)
3. AWS CLI configured with appropriate credentials

## Installation

To add this MCP server to your Amazon Q or Claude, add the following to your MCP config file. With Amazon Q, create (if does not yet exist) a file named `.amazonq/mcp.json` under the same directory that is running `q chat`. Then add the following config:

```json
{
  "mcpServers": {
    "use-aws-mcp-server": {
        "command": "uvx",
        "args": ["use-aws-mcp-server@latest"]
    }
  }
}
```

## Tools

### use_aws

Make an AWS CLI api call with the specified service, operation, and parameters.

```python
def use_aws(
    region: str,
    service_name: str,
    operation_name: str,
    label: str,
    parameters: dict = None,
    profile_name: str = None,
) -> str:
```
