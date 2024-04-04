import json
import boto3
from datetime import datetime
import http.client
import requests

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    userTable = dynamodb.Table('User')
    
    # --- Helper Functions ---
    def send_message(phone_number, message):
        data = json.dumps({"phoneNumber": phone_number, "message": message})
        headers = {"Content-Type": "application/json"}
        conn = http.client.HTTPSConnection("aqwgmthqlk.execute-api.us-east-2.amazonaws.com")
        try:
            conn.request("POST", "/default/smsSender-SmsHandleOutboundFunction-c1mnlkMhXvty", body=data, headers=headers)
            response = conn.getresponse()
            if response.status == 200:
                responseData = response.read().decode()
                print("Response sending message:", responseData)
            else:
                print("Failed to send message:", response.status, response.reason)

        finally:
            conn.close()

    def log_message_to_slack(message, error=False):
        webhook_url = 'https://hooks.slack.com/services/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'
        if error:
            data = {
                'text': f'*ERROR* : {message}',
            }
            response = requests.post(webhook_url, json=data)
            return response

        base_text = f'*SUCCESS* : "{message}"'
        data = {
            'text': base_text,
        }

        response = requests.post(webhook_url, json=data)

        return response

    # --- main() ---    

    # TODO Reminder execution should be total users in the database.
    log_message_to_slack("Started reminder execution with *1* user(s) queued.")
    # send_message('+12103161487', 'Good morning')
    log_message_to_slack(f"Sent reminder messages successfully to *1* user(s), *0* failed.")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Success",
        }),
    }
