import boto3

ec2_client = boto3.client('ec2')


def delete_volumes(data):
    for vol in data:
        ec2_client.delete_volume(VolumeId=vol)


def lambda_handler(event, context):
    volume_ids = event['payload']
    delete_volumes(volume_ids)
    return {
        'statusCode': 200,

    }
