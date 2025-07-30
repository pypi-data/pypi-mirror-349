import boto3

def get_tags(resource_arn):
    eks = boto3.client('eks')
    return eks.list_tags_for_resource(resourceArn=resource_arn).get('tags', {})

def apply_tags(resource_arn, tags, clean=False):
    eks = boto3.client('eks')
    if clean:
        current = get_tags(resource_arn)
        if current:
            eks.untag_resource(resourceArn=resource_arn, tagKeys=list(current.keys()))
    eks.tag_resource(resourceArn=resource_arn, tags=tags)