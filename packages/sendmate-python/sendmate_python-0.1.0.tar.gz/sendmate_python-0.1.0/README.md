# SendMate Python SDK

A Python SDK for the SendMate payment processing and wallet management API.

## Installation

```bash
pip install sendmate-python
```

## Usage

```python
from sendmate import SendMate, Currency, PaymentType

# Initialize the client
client = SendMate(api_key="your_api_key")  # Or set SENDMATE_API_KEY environment variable

# Create a checkout session
checkout = client.create_checkout(
    amount=100.00,
    currency=Currency.USD,
    payment_type=PaymentType.CARD,
    customer_email="customer@example.com",
    customer_name="John Doe"
)

# Get checkout URL
print(f"Checkout URL: {checkout['checkout_url']}")

# Check transaction status
status = client.get_transaction_status("transaction_id")
print(f"Transaction status: {status}")
```

## Features

- Payment processing
- Checkout session management
- Transaction status tracking
- Type-safe API with Pydantic models
- Environment-based configuration

## Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   pytest
   ```

## Publishing to PyPI

1. Build the package:
   ```bash
   python setup.py sdist bdist_wheel
   ```

2. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

## License

MIT License 