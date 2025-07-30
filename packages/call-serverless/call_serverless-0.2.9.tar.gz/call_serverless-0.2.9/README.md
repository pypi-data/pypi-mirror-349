# Call Serverless
`call-serverless` is a Python library designed to remotely invoke AWS Lambda functions that have API Gateway integration. It simplifies the process of invoking Lambda functions with HTTP-like requests, providing both synchronous and asynchronous methods to send requests and handle responses.

## Features
- **Invoke AWS Lambda Functions**: Call Lambda functions via their ARN using HTTP methods (GET, POST, PUT, DELETE)
- **Simulate API Gateway Requests**: Send requests with customizable paths, headers, stages, and body payloads
- **Async Support**: Built-in support for asynchronous operations using aiobotocore
- **Simple Setup**: Built on top of boto3/aiobotocore, the library manages AWS Lambda client connections and simplifies API invocation
- **Response Handling**: Automatic parsing of Lambda responses with proper error handling

## Installation
To install the library, use pip:
```bash
pip install call-serverless
```

## Requirements
- Python 3.6 or higher
- `boto3` for AWS SDK integration
- `aiobotocore` for async operations

## Usage

### Synchronous Lambda Invocation
```python
from call_serverless.apis import call_lambda

# Basic GET request
response = call_lambda(
    lambda_arn="arn:aws:lambda:us-west-2:123456789012:function:MyFunction",
    path="/users/{id}",
    method="GET",
    path_params={"id": "123"},
    query_params={"include": "profile"},
    headers={"Authorization": "Bearer token123"}
)

print(response.status_code)  # 200
print(response.body)  # {"name": "John Doe", "email": "john@example.com"}

# POST request with body
response = call_lambda(
    lambda_arn="arn:aws:lambda:us-west-2:123456789012:function:MyFunction",
    path="/users",
    method="POST",
    body={"username": "new_user", "email": "user@example.com"},
    headers={"Content-Type": "application/json"}
)

# Handle errors
try:
    response.raise_for_status()
except ErrorResponse as e:
    print(f"Error: {e}")
```

### Asynchronous Lambda Invocation
```python
import asyncio
from call_serverless.apis import call_lambda_async

async def get_user():
    response = await call_lambda_async(
        lambda_arn="arn:aws:lambda:us-west-2:123456789012:function:MyFunction",
        path="/users/{id}",
        method="GET",
        path_params={"id": "123"},
        query_params={"include": "profile"},
        headers={"Authorization": "Bearer token123"}
    )
    return response.body

# Run the async function
user = asyncio.run(get_user())
```

## Response Object
The library returns a `CLResponse` object that provides:
- `status_code`: HTTP status code from the Lambda response
- `body`: Response body (automatically parsed as JSON if possible)
- `raise_for_status()`: Method to raise an exception for error status codes (>= 400)

## Error Handling
The library provides several exception classes:
- `LambdaAccessError`: Raised when there are issues accessing or executing the Lambda function
- `InvalidResponseFormat`: Raised when the Lambda response is not in the expected format
- `ErrorResponse`: Raised when the Lambda returns a status code >= 400

## Contributing
If you want to contribute to this project, please submit a pull request or open an issue on GitHub.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.