_BASE_TEMPLATE = {
    "resource": "",
    "path": "",
    "httpMethod": "GET",
    "headers": None,
    "queryStringParameters": None,
    "multiValueQueryStringParameters": None,
    "multiValueHeaders": [],
    "pathParameters": None,
    "requestContext": {
        "apiId": "CallServerless",
        "accountId": "CallServerless",
        "resourcePath": "",
        "httpMethod": "GET",
        "path": "",
        "protocol": "HTTP/1.1",
        "stage": "",
        "requestId": "CallServerless",
        "requestTime": "30/Aug/2025: 16: 41: 20 +0000",
        "requestTimeEpoch": 1661877680472,
        "identity": {
            "sourceIp": "127.0.0.1",
        },
    },
    "body": None,
    "isBase64Encoded": False,
}


def base_template():
    return _BASE_TEMPLATE.copy()
