# mighty-sdk-core

This directory contains the core functionalities of the Mighty Network's official SDK. It includes essential modules and utilities that provide the foundational features required for the SDK to operate efficiently.

# Quick Start
This section guides you through setting up and using the `MightyUserDataClient` to fetch and decrypt user data from the `Mighty Network API`.

### Prerequisites

- Python 3.12+
- Install required dependencies:
    
    ```bash
    pip install aiohttp mighty-sdk-core
    ```
    
- Obtain your API key, public key, and private key from the Mighty Network API dashboard.
- Ensure the Mighty API base URL is accessible (defaults to `http://localhost:8080`).

### Basic Usage

1. **Initialize the Client**:
Create an instance of `MightyUserDataClient` with your API credentials.
    
    ```python
    from mighty_sdk_core.mighty.user_data_client import MightyUserDataClient
    
    # Replace with your actual credentials
    api_key = "your-data-api-key"
    public_key = "data-api-key-public-key"
    private_key = "data-api-key-private-key"
    
    client = MightyUserDataClient(
        api_key=api_key,
        api_public_key=public_key,
        api_private_key=private_key
    )
    ```
    
2. **Fetch and Decrypt Data**:
Use the `get_data` method to asynchronously retrieve and decrypt user data.
    
    ```python
    import asyncio
    
    async def main():
        try:
            data = await client.get_data()
            print("Decrypted Data:", data)
        except Exception as e:
            print(f"Error: {e}")
    
    # Run the async function
    asyncio.run(main())
    
    ```
    

### Environment Configuration

You can configure the API base URL using an environment variable:

```bash
export MIGHTY_BASE_URL="<https://your-mighty-api-url>"

```

If not set, it defaults to `http://localhost:8080`.

### Notes

- Ensure your API credentials are kept secure and not hard-coded in production code.
- The `get_data` method handles HTTP requests and decryption automatically, returning the decrypted data as a string.
- Errors during fetching or decryption will be raised as exceptions, so use try-except blocks for robust error handling.

This setup should get you up and running quickly with the `MightyUserDataClient`. For advanced usage, refer to the full documentation.