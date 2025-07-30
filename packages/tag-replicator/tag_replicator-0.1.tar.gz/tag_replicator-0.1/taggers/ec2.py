import boto3

def get_tags(resource_id):
    ec2 = boto3.client('ec2')
    response = ec2.describe_tags(Filters=[
        {'Name': 'resource-id', 'Values': [resource_id]}
    ])
    return {tag['Key']: tag['Value'] for tag in response['Tags']}

def apply_tags(resource_id, tags, clean=False):
    ec2 = boto3.client('ec2')
    if clean:
        current_tags = get_tags(resource_id)
        if current_tags:
            ec2.delete_tags(Resources=[resource_id], Tags=[{'Key': k} for k in current_tags])
    if tags:
        ec2.create_tags(Resources=[resource_id], Tags=[{'Key': k, 'Value': v} for k, v in tags.items()])