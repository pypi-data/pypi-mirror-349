# Observe Python SDK

A Python SDK for tool usage logging and monitoring.

## Installation

```bash
pip install observee
```

## Usage

You can set the MCP server name either globally or per decorator:

### Global Configuration

```python
from observee import ObserveeConfig, observee_usage_logger

# Set the MCP server name globally
ObserveeConfig.set_mcp_server_name("your-mcp-server-name")

@observee_usage_logger
async def your_function():
    # Your code here
    pass
```

### Per-Decorator Configuration

```python
from observee import ObserveeConfig, observee_usage_logger

@observee_usage_logger
async def your_function():
    # Your code here
    pass
```

## Features

- Tool usage logging with async support
- Automatic logging of:
  - Tool name
  - Input parameters
  - Response data
  - Execution duration
  - Error information (if any)
- Configurable logging endpoint (defaults to Observe API)
- Error handling and reporting
- Performance tracking
- Flexible MCP server name configuration

## Logging Details

The SDK automatically logs the following information for each tool usage:
- MCP server name
- Tool name (derived from function name)
- Tool input parameters (as JSON)
- Tool response
- Execution duration in milliseconds
- Any errors that occur during execution

Logs are sent asynchronously to avoid impacting tool performance.

## Requirements

- Python 3.8 or higher
- Dependencies:
  - httpx
  - pydantic

## License

MIT 