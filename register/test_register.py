import boto3
import botocore
import pytest
import json
from datetime import datetime
from botocore.stub import ANY, Stubber
import os

@pytest.fixture(scope="function")
def cognito_stub():
    from register import client

    with Stubber(client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


@pytest.fixture(scope="function")
def dynamodb_resource_stub():
    from register import dynamodb

    with Stubber(dynamodb.meta.client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()

@pytest.fixture(scope="function")
def valid_event():
    return {'body': '{"username":"test", "password":"pass@123"}'
    }


def test_valid_event(cognito_stub: Stubber, dynamodb_resource_stub: Stubber, lambda_context, valid_event):
    from register import lambda_handler
    cognito_stub.add_response(
        "sign_up", 
        service_response={
            "UserConfirmed": False,
            "CodeDeliveryDetails": {},
            "UserSub": "test"
        },
    )

    cognito_stub.add_response(
        "admin_get_user",
        service_response={
            "Enabled": True,
            "MFAOptions": [ 
                { 
                    "AttributeName": "string",
                    "DeliveryMedium": "string"
                }
            ],
            "PreferredMfaSetting": "string",
            "UserAttributes": [ 
                { 
                    "Name": "string",
                    "Value": "test@gmail.com"
                },
                { 
                    "Name": "string",
                    "Value": "test2@gmail.com"
                },
                { 
                    "Name": "string",
                    "Value": "test3@gmail.com"
                }
            ],
            "UserCreateDate": datetime.fromisoformat('2011-11-04'),
            "UserLastModifiedDate": "2022-06-07 00:00:00",
            "UserMFASettingList": [ "string" ],
            "Username": "string",
            "UserStatus": "string"
        }
    )

    dynamodb_resource_stub.add_response(
        "put_item",
        service_response={}
    )
    resp = lambda_handler(event=valid_event, context=lambda_context)





