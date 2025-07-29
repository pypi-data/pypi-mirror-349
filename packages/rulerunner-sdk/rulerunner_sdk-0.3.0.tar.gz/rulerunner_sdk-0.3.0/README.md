# RuleRunner Python SDK

Official Python SDK for the RuleRunner API - a compliance-as-a-service platform for blockchain transactions.

## Installation

```bash
pip install rulerunner-sdk
```

## Quick Start

```python
from rulerunner_sdk import RuleRunnerClient

# Initialize the client with your API key
client = RuleRunnerClient(api_key="YOUR_API_KEY")

# Check if a transaction is compliant
result = client.is_compliant(
    from_address="0x7FF9cFad3877F21d41Da833E2F775dB0569eE3D9",
    to_address="0x742d35Cc6634C0532925a3b844Bc454e4438f44f",
    amount="1.0"
)

print(f"Transaction is compliant: {result['is_compliant']}")
print("--------------------------------")
print(result.get("from_entity_details"))
print("--------------------------------")

# Verify a proof locally
if not result['is_compliant'] and result.get('from_address_proof'):
    is_valid = client.verify_proof_locally(
        address="0x7FF9cFad3877F21d41Da833E2F775dB0569eE3D9",
        proof=result.get("from_address_proof"),
        root=result['merkle_root']
    )
    print(f"Local proof verification: {is_valid}")
```

## Features

- Transaction compliance checking
- Local proof verification
- Health check endpoint
- API key management

## API Reference

### RuleRunnerClient

```python
client = RuleRunnerClient(
    api_key: str,
    base_url: str = "https://api.rulerunner.com"  # Optional custom base URL
)
```

### Methods

#### is_compliant

Check if a transaction is compliant with sanctions lists.

```python
result = client.is_compliant(
    from_address: str,
    to_address: str,
    amount: str
)
```

#### verify_proof_locally

Verify a Merkle proof locally without making an API call.

```python
is_valid = client.verify_proof_locally(
    address: str,
    proof: List[Dict[str, Any]],
    root: str
)
```

#### health_check

Check the health status of the API.

```python
status = client.health_check()
```

## Error Handling

The SDK raises custom exceptions for different error cases:

- `RuleRunnerAPIError`: API-level errors (4xx, 5xx)
- `RuleRunnerConnectionError`: Network/connection issues
- `RuleRunnerProofVerificationError`: Invalid proof data

## License

MIT License 