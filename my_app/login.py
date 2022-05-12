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
    resp = client.initiate_auth(
    ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
    AuthFlow="USER_PASSWORD_AUTH",
    AuthParameters={"USERNAME": username, "PASSWORD": password},
    )

    # From the JSON response you are accessing the AccessToken
    print("Log in success")
    print("ACCESS TOKEN:")
    access_token =  resp['AuthenticationResult']['AccessToken']

    print(access_token)
    print('###################################')

    id_token =  resp['AuthenticationResult']['IdToken']

    print('ID TOKEN:')
    print(id_token)
    print('##########################')
    # Getting the user details.

    user_details = client.get_user(AccessToken=access_token)
    print('USER DETAILS USING ACCESS TOKEN:')
    print(user_details)

    print('User Logged In Successfully!')

    message = {
   'message': 'User Logged In Successfully!'
    }

    return {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps(message)
    }


    