import json
import os
import boto3



def lambda_handler(event, context):

    data = json.loads(event['body'])

    username = data['username']
    password = data['password']

    client = boto3.client("cognito-idp", region_name="ap-south-1")

    print('client ID is: ' + os.environ.get("COGNITO_USER_CLIENT_ID"))

    # The below code, will do the sign-up
    response = client.sign_up(
        ClientId=os.environ.get("COGNITO_USER_CLIENT_ID"),
        Username=username,
        Password=password,
        UserAttributes=[{"Name": "email", "Value": username}],
    )

    print('User Registered Successfully!')

    message = {
   'message': 'User Registered Successfully!'
    }

    return {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps(message)
    }
