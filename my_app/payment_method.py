import json
import os



def lambda_handler(event, context):

    print("TOKEN:")
    token = event["headers"]["Authorization"]
    print(token)
    print('Token Verified,Payment method selected')

    message = {
   'message': 'Token Verified, Payment method selected'
    }

    return {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps(message)
    }