import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLE_NAME')

def lambda_handler(event, context):
    code = event['pathParameters']['code']

    response = table.update_item(
        Key={'code': code},
        UpdateExpression="ADD click_count :inc",
        ExpressionAttributeValues={':inc': 1},
        ReturnValues="ALL_NEW"
    )

    return {
        "statusCode": 301,
        "headers": {
            "Location": response['Attributes']['target_url']
        }
    }
