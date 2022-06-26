import boto3
import botocore
import pytest
import json
from datetime import datetime
from botocore.stub import ANY, Stubber
import os

@pytest.fixture(scope="function")
def cognito_stub():
    from account_verify import client

    with Stubber(client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


@pytest.fixture(scope="function")
def valid_event():
    return {'body': '{"username":"test", "verification code":"123456"}'}


def test_valid_event(cognito_stub: Stubber, lambda_context, valid_event):
    from account_verify import lambda_handler
    cognito_stub.add_response(
        "confirm_sign_up", 
        service_response={
        },
    )

    resp = lambda_handler(event=valid_event, context=lambda_context)

