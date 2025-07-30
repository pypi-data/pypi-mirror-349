import boto3

def get_tags(file_system_id):
    efs = boto3.client('efs')
    response = efs.describe_tags(FileSystemId=file_system_id)
    return {tag['Key']: tag['Value'] for tag in response['Tags']}

def apply_tags(file_system_id, tags, clean=False):
    efs = boto3.client('efs')
    if clean:
        efs.delete_tags(FileSystemId=file_system_id, TagKeys=list(get_tags(file_system_id).keys()))
    efs.create_tags(FileSystemId=file_system_id, Tags=[{'Key': k, 'Value': v} for k, v in tags.items()])