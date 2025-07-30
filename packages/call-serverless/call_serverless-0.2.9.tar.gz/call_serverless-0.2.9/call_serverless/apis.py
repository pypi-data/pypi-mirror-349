import asyncio
import atexit
import json
from typing import Optional, Union

import boto3
import botocore
import botocore.exceptions
from aiobotocore.session import AioSession, get_session

from .exceptions import LambdaAccessError
from .formatter import format_request
from .response import CLResponse

_clients = {}
_async_clients = {}


def _get_lambda_client(region: str):
    global _clients
    if region not in _clients:
        _clients[region] = boto3.client("lambda", region_name=region)
    return _clients[region]


async def _get_async_lambda_client(region: str):
    global _async_clients

    if region not in _async_clients:
        session: AioSession = get_session()
        async with session.create_client("lambda", region_name=region) as client:
            _async_clients[region] = client
    return _async_clients[region]


async def _cleanup_async_clients():
    """Cleanup function to close all async clients."""
    for client in _async_clients.values():
        await client.close()
    _async_clients.clear()


def _cleanup_sync_clients():
    """Cleanup function to close all sync clients."""
    for client in _clients.values():
        client.close()
    _clients.clear()


# Register cleanup handlers
atexit.register(_cleanup_sync_clients)
atexit.register(lambda: asyncio.run(_cleanup_async_clients()))


def call_lambda(
    lambda_arn: str,
    path: str,
    method: str = "GET",
    stage: str = "prod",
    headers: Union[dict, None] = None,
    path_params: Union[dict, None] = None,
    query_params: Union[dict, None] = None,
    body: Union[dict, str, None] = None,
) -> CLResponse:
    """
    Invokes an AWS Lambda function by sending an HTTP-like request with the specified method, path,
    and headers. The function simulates an API Gateway request to the Lambda function.

    Args:
        lambda_arn (str): The Amazon Resource Name (ARN) of the Lambda function to invoke.
            The region will be automatically extracted from this ARN.
        path (str): The API Gateway path to invoke on the Lambda function (e.g., `/users/{id}`,
            `/items`). It must be exactly how it is defined in the app.
        method (str): The HTTP method to use for the request (e.g., 'GET', 'POST', 'PUT', 'DELETE').
            Defaults to 'GET'.
        stage (str): The deployment stage of the API (e.g., 'dev', 'prod'). Defaults to 'prod'.
        headers (Union[dict, None], optional): Additional headers to send in the request.
            Defaults to None.
        path_params (Union[dict, None], optional): Path parameters to send in the request.
            For example, if path is `/users/{id}`, path_params could be `{"id": "123"}`.
            Defaults to None.
        query_params (Union[dict, None], optional): Query parameters to send in the request.
            For example, `{"filter": "active", "sort": "name"}`.
            Defaults to None.
        body (Union[dict, str, None], optional): The request body to send in the Lambda invocation.
            Can be a dictionary (will be JSON serialized) or a string. Defaults to None.

    Returns:
        CLResponse: A response object containing:
            - status_code (int): The HTTP status code from the Lambda response
            - body (Union[dict, str]): The response body, parsed as JSON if possible

    Raises:
        ValueError: If the lambda_arn is invalid and region cannot be extracted
        botocore.exceptions.ClientError: If there is an error in the Lambda client during invocation
        LambdaAccessError: If there are issues accessing or executing the Lambda function
        InvalidResponseFormat: If the Lambda response is not in the expected format
        ErrorResponse: If the Lambda returns a status code >= 400

    Example:
        >>> response = call_lambda(
                lambda_arn="arn:aws:lambda:us-west-2:123456789012:function:MyFunction",
                path="/users/{id}",
                method="GET",
                path_params={"id": "123"},
                query_params={"include": "profile"},
                headers={"Authorization": "Bearer token123"}
            )
        >>> print(response.status_code)  # 200
        >>> print(response.body)  # {"name": "John Doe", "email": "john@example.com"}
    """

    payload = format_request(
        path=path,
        method=method,
        stage=stage,
        headers=headers,
        path_params=path_params,
        query_params=query_params,
        body=body,
    )
    try:
        region = lambda_arn.split(":")[3]
    except IndexError:
        raise ValueError(f"Invalid lambda ARN: {lambda_arn}")

    client = _get_lambda_client(region)
    try:
        response = client.invoke(
            FunctionName=lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload),
        )
    except botocore.exceptions.ClientError as exc:
        raise LambdaAccessError(f"Issue with the lambda execution: {str(exc)}") from exc

    response_str = response["Payload"].read().decode("utf-8")
    return CLResponse.from_response(response_str)


async def call_lambda_async(
    lambda_arn: str,
    path: str,
    method: str = "GET",
    stage: str = "prod",
    headers: Optional[dict] = None,
    path_params: Optional[dict] = None,
    query_params: Optional[dict] = None,
    body: Optional[Union[dict, str]] = None,
) -> CLResponse:
    """
    Asynchronously invokes an AWS Lambda function by sending an HTTP-like request with the specified method, path,
    and headers. The function simulates an API Gateway request to the Lambda function.

    This is the asynchronous version of call_lambda. It uses aiobotocore for async AWS operations.
    For detailed parameter descriptions, return values, and possible exceptions, see call_lambda.

    Example:
        >>> async def get_user():
        ...     response = await call_lambda_async(
        ...         lambda_arn="arn:aws:lambda:us-west-2:123456789012:function:MyFunction",
        ...         path="/users/{id}",
        ...         method="GET",
        ...         path_params={"id": "123"},
        ...         query_params={"include": "profile"},
        ...         headers={"Authorization": "Bearer token123"}
        ...     )
        ...     print(response.status_code)  # 200
        ...     print(response.body)  # {"name": "John Doe", "email": "john@example.com"}
    """
    payload = format_request(
        path=path,
        method=method,
        stage=stage,
        headers=headers,
        path_params=path_params,
        query_params=query_params,
        body=body,
    )

    try:
        region = lambda_arn.split(":")[3]
    except IndexError:
        raise ValueError(f"Invalid lambda ARN: {lambda_arn}")

    client = await _get_async_lambda_client(region)
    try:
        response = await client.invoke(
            FunctionName=lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload),
        )
    except botocore.exceptions.ClientError as exc:
        raise LambdaAccessError(f"Issue with the lambda execution: {str(exc)}") from exc
    response_str = (await response["Payload"].read()).decode("utf-8")
    return CLResponse.from_response(response_str)
