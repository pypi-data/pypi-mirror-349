import boto3

def get_tags(resource_arn):
    backup = boto3.client('backup')
    return backup.list_tags(ResourceArn=resource_arn).get('Tags', {})

def apply_tags(resource_arn, tags, clean=False):
    backup = boto3.client('backup')
    if clean:
        current = get_tags(resource_arn)
        if current:
            backup.untag_resource(ResourceArn=resource_arn, TagKeyList=list(current.keys()))
    backup.tag_resource(ResourceArn=resource_arn, Tags=tags)