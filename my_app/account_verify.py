import json
import os
import boto3



def lambda_handler(event, context):

    data = json.loads(event['body'])

    username = data['username']

    client = boto3.client("cognito-idp", region_name="ap-south-1")


    print('client ID is: ' + os.environ.get("COGNITO_USER_CLIENT_ID"))

    verification_code = data['verification code']

    response = client.confirm_sign_up(
    ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
    Username=username,
    ConfirmationCode=verification_code,
    )

    print(response)


    print('Account Verified Successfully!')

    message = {
   'message': 'Account Verified Successfully!'
    }

    return {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps(message)
    }
