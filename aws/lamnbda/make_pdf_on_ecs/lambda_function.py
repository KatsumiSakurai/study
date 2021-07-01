import json
import boto3


ecs = boto3.client('ecs')


def lambda_handler(event, context):
    name = event['queryStringParameters']['name']
    print(name)
    
    response = ecs.run_task(
        cluster='sakurai-make-pdf',
        taskDefinition='sakurai-make-pdf:2',
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-3b739961',
                    'subnet-96c84abd',
                    'subnet-0c269e44'
                ],
                'securityGroups': [
                    'sg-9816e4dd'
                ],
                'assignPublicIp': 'ENABLED'
            }  
        },
        overrides={
            'containerOverrides': [
                {
                    "name": "sakurai-make-pdf",
                    'environment': [
                        {
                            'name': 'name',
                            'value': name,
                        }
                    ]
                }
            ]
        })
        
    print(response)
    failures = response['failures']
    if len(failures) > 0:
        print(failures)
        return {
            'statusCode': 500,
            'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
            'body': json.dumps('task error')
        }
        
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('OK')
    }
    