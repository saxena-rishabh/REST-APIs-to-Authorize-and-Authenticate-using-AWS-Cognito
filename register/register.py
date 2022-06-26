import json
import os
import boto3


TableForUserDetails = os.environ.get("USER_DETAILS_TABLE")

dynamodb = boto3.resource('dynamodb')
client = boto3.client("cognito-idp", region_name="ap-south-1")

def lambda_handler(event, context):
    print(f"event:::{event}")
    data = json.loads(event['body'])

    username = data['username']
    password = data['password']

    print('client ID is: ' + os.environ.get("COGNITO_USER_CLIENT_ID"))

    # The below code, will do the sign-up
    response = client.sign_up(
        ClientId=os.environ.get("COGNITO_USER_CLIENT_ID"),
        Username=username,
        Password=password,
        UserAttributes=[{"Name": "email", "Value": username}],
    )
    print("response", response)
    
    user_details = client.admin_get_user(
        UserPoolId=os.environ.get("USER_POOL_ID"),
        Username=username
    )

    print(user_details)
    print(type(user_details))

    email = user_details['UserAttributes'][2]['Value']
    userCreationDate = user_details['UserCreateDate'].strftime("%Y-%m-%d %H:%M:%S")

    print(username)
    print(email)
    print(userCreationDate)

    table = dynamodb.Table(TableForUserDetails)
    
    data = {
        'username': username,
        'email': email,
        'userCreationDate': userCreationDate
    }

    table.put_item(Item=data)
    print('User Registered Successfully!')

    message = {
   'message': 'User Registered Successfully!'
    }

    return {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps(message)
    }
