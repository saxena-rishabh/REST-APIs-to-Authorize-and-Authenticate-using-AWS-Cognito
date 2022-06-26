import boto3
import botocore
import pytest
import json
from datetime import datetime
from botocore.stub import ANY, Stubber
import os

@pytest.fixture(scope="function")
def cognito_stub():
    from login import client

    with Stubber(client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()



@pytest.fixture(scope="function")
def valid_event():
    return {'body': '{"username":"test", "password":"pass@123"}'}


@pytest.fixture(scope="function")
def invalid_event():
    return {'body': '{"username":"test"}'}


def test_valid_event(cognito_stub: Stubber, lambda_context, valid_event):
    from login import lambda_handler
    cognito_stub.add_response(
        "initiate_auth", 
        service_response={
                "AuthenticationResult": { 
                    "AccessToken": "a.b.c",
                    "ExpiresIn": 300,
                    "IdToken": "a.b.c",
                    "NewDeviceMetadata": { 
                        "DeviceGroupKey": "string",
                        "DeviceKey": "string"
                    },
                    "RefreshToken": "string",
                    "TokenType": "string"
                },
                "ChallengeName": "string",
                "ChallengeParameters": { 
                    "string" : "string" 
                },
                "Session": "12345678901234567890"
                },
    )


    resp = lambda_handler(event=valid_event, context=lambda_context)


def test_invalid_event(cognito_stub: Stubber, lambda_context, invalid_event):
    from login import lambda_handler
    cognito_stub.add_response(
        "initiate_auth", 
        service_response={
                "AuthenticationResult": { 
                    "AccessToken": "a.b.c",
                    "IdToken": "a.b.c",
                    "NewDeviceMetadata": { 
                        "DeviceGroupKey": "string",
                        "DeviceKey": "string"
                    },
                    "RefreshToken": "string",
                    "TokenType": "string"
                },
                "ChallengeName": "string",
                "ChallengeParameters": { 
                    "string" : "string" 
                },
                "Session": "12345678901234567890"
                },
    )


    resp = lambda_handler(event=invalid_event, context=lambda_context)
    assert resp == {
        'statusCode': 400,
        }

