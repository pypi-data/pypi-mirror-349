# botrun-hatch-client

A client library for interacting with the BotRun Flow Language (botrun_flow_lang) API. This library provides a simple and intuitive interface for applications to communicate with the BotRun Flow Language service using aiohttp for asynchronous requests.

## About

`botrun-hatch-client` is designed to be a lightweight and easy-to-use async client for the BotRun Flow Language. It abstracts away the complexity of API communication, providing a simple interface for other applications to leverage BotRun's capabilities asynchronously.

## Current Integrations

This client is currently integrated with:

- **botrun_back**: Backend service utilizing the client for core functionality
- **botrun_ask_folder**: Tool that uses the client to analyze folder structures

## Installation

```bash
pip install botrun-hatch-client
```

## Basic Usage

```python
import asyncio
from botrun_hatch_client.client import HatchClient

async def main():
    # Initialize with your API key
    client = HatchClient(api_key="your_api_key")
    
    try:
        # Validate your connection
        status = await client.validate_connection()
        print(status)
        
        # Make an API request
        response = await client.make_request(
            endpoint="some/endpoint",
            method="POST",
            data={"key": "value"}
        )
        print(response)
        
        # Format a payload for the API
        payload = {
            "data": {
                "key": "value",
                "nested": {
                    "subkey": "subvalue"
                }
            }
        }
        formatted = client.format_payload(payload)
        print(formatted)
        
    finally:
        # Always close the client session when done
        await client.close()

# Run the async function
asyncio.run(main())
```

## Development

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/) for dependency management

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd botrun-hatch-client

# Install dependencies
poetry install
```

### Running Tests

```bash
# Run tests using the unittest framework
./run_tests.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
