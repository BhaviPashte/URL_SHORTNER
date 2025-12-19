import json, boto3, random, string
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLE_NAME')

def generate_code(length=5):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def lambda_handler(event, context):
    print("EVENT:", event)

    user_id = event['requestContext']['authorizer']['claims']['sub']
    body = json.loads(event['body'])

    code = generate_code()

    table.put_item(Item={
        'code': code,
        'user_id': user_id,
        'target_url': body['target_url'],
        'created_at': datetime.utcnow().isoformat(),
        'click_count': 0
    })

    return {
        "statusCode": 201,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "authorization,content-type",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
        },
        "body": json.dumps({"code": code})
    }
