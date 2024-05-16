import csv
import boto3

ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')

bucket = 'samplebucket'
file_name = 'volume_details.csv'


def get_volumes():
    response = ec2_client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    return response['Volumes']


def create_csv(data):
    filepath = f'/tmp/{file_name}'
    fieldnames = ["VolumeId", "AvailabilityZone", "Size", "VolumeType"]

    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({key: row[key] for key in fieldnames})
    return filepath


def upload_to_s3(path):
    s3_client.upload_file(path, bucket, f'volume_report/{file_name}')


def create_snapshots(vol_ids):
    for vol_id in vol_ids:
        ec2_client.create_snapshot(
            Description="Unattached Volume's Snapshot",
            VolumeId=vol_id,
            TagSpecifications=[
                {'ResourceType': 'snapshot', 'Tags': [{'Key': 'AssociatedVolumeID', 'Value': vol_id}]}]
        )


def lambda_handler(event, context):
    raw_data = get_volumes()
    csv_path = create_csv(raw_data)
    upload_to_s3(csv_path)

    volume_ids = []
    for row in raw_data:
        volume_ids.append(row["VolumeId"])
    create_snapshots(volume_ids)

    return {
        'statusCode': 200, 'payload': volume_ids
    }
