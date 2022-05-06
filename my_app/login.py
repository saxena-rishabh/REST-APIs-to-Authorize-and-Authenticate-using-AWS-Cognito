import json
import os
import boto3



def lambda_handler(event, context):

    data = json.loads(event['body'])

    username = data['username']
    password = data['password']

    client = boto3.client("cognito-idp", region_name="ap-south-1")

    print('client ID is: ' + os.environ.get("COGNITO_USER_CLIENT_ID"))

    # Initiating the Authentication, 
    response = client.initiate_auth(
    ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
    AuthFlow="USER_PASSWORD_AUTH",
    AuthParameters={"USERNAME": username, "PASSWORD": password},
    )

    # From the JSON response you are accessing the AccessToken
    print(response)
    # Getting the user details.
    access_token = response["AuthenticationResult"]["AccessToken"]

    response = client.get_user(AccessToken=access_token)
    print(response)

    print('User Logged In Successfully!')

    message = {
   'message': 'User Logged In Successfully!'
    }

    return {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps(message)
    }


    