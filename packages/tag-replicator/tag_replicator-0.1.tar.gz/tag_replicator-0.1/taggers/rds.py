import boto3

def get_tags(resource_arn):
    rds = boto3.client('rds')
    response = rds.list_tags_for_resource(ResourceName=resource_arn)
    return {tag['Key']: tag['Value'] for tag in response['TagList']}

def apply_tags(resource_arn, tags, clean=False):
    rds = boto3.client('rds')
    if clean:
        rds.remove_tags_from_resource(ResourceName=resource_arn, TagKeys=list(get_tags(resource_arn).keys()))
    rds.add_tags_to_resource(ResourceName=resource_arn, Tags=[{'Key': k, 'Value': v} for k, v in tags.items()])