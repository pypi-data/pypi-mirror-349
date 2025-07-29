# **Jup Python SDK**

A Python SDK for interacting with Jupiter Exchange APIs.

## **Installation**

To install the SDK in your project, run:
```
sh
pip install jup-ag-sdk
```
## **Quick Start**

Here's a basic example to help you get started with the Jup Python SDK:
```
python
from dotenv import load_dotenv

from jup_python_sdk.clients.ultra_api_client import UltraApiClient
from jup_python_sdk.models.ultra_api.ultra_order_request_model import (
    UltraOrderRequest,
)

load_dotenv()
client = UltraApiClient()

order_request = UltraOrderRequest(
   input_mint="So11111111111111111111111111111111111111112",  # WSOL
   output_mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
   amount=10000000,  # 0.01 WSOL
   taker=client._get_public_key(),
)

try:
   client_response = client.order_and_execute(order_request)
   signature = str(client_response["signature"])
   
   print("Order and Execute API Response:")
   print(f"  - Transaction Signature: {signature}")
   print(f"  - View on Solscan: https://solscan.io/tx/{signature}")

except Exception as e:
   print("Error occurred while processing the order:", str(e))
finally:
   client.close()
```

## **Setup Instructions**

Before using the SDK, please ensure you have completed the following steps:

1. **Environment Variables**:  
   Set up your required environment variables.  
   Example:
   ```sh
   export PRIVATE_KEY=your_private_key_here
   ```

2. **Python Version**:  
   Make sure you are using Python 3.9 or later.

3**Configuration**:  
   TBD

## **Disclaimer**

🚨 **This project is actively worked on.**  
While we don't expect breaking changes as the SDK evolves, we recommend you stay updated with the latest releases.  
Any important updates will be announced in the [Discord server](https://discord.gg/jup).