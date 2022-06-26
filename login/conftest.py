import os
from typing import Callable
from uuid import uuid4

import pytest


@pytest.fixture(scope="module")
def sqs_event_factory() -> Callable:
    def factory(body: str):
        return {
            "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
            "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a",
            "body": body,
            "attributes": {},
            "messageAttributes": {},
            "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-east-2:123456789012:my-queue",
            "awsRegion": "us-east-1",
        }

    return factory

class MockContext(object):
    def __init__(self, function_name):
        self.function_name = function_name
        self.function_version = "v$LATEST"
        self.memory_limit_in_mb = 512
        self.invoked_function_arn = (
            f"arn:aws:lambda:us-east-1:ACCOUNT:function:{self.function_name}"
        )
      
        self.aws_request_id = str(uuid4)

@pytest.fixture(scope="module", autouse=True)
def mock_envs():

    """Mocked environments for testing."""
    os.environ["COGNITO_USER_CLIENT_ID"] = "xxxxxx"
    os.environ["USER_POOL_ID"] = "test_pool_id"
    os.environ["USER_DETAILS_TABLE"] = "test_table"

@pytest.fixture
def lambda_context():
    return MockContext("dummy_function")