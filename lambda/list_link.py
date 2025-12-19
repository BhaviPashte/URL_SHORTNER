import json, boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLE_NAME')

# Helper to convert Decimal → int/float
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o)
        return super().default(o)

def lambda_handler(event, context):
    claims = event['requestContext']['authorizer']['claims']
    user_id = claims['sub']

    response = table.scan(
        FilterExpression=Attr('user_id').eq(user_id)
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "authorization,content-type",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
        },
        "body": json.dumps(response['Items'], cls=DecimalEncoder)
    }
