import boto3

def get_tags(function_arn):
    lambda_client = boto3.client('lambda')
    return lambda_client.list_tags(Resource=function_arn).get('Tags', {})

def apply_tags(function_arn, tags, clean=False):
    lambda_client = boto3.client('lambda')
    if clean:
        current = get_tags(function_arn)
        if current:
            lambda_client.untag_resource(Resource=function_arn, TagKeys=list(current.keys()))
    lambda_client.tag_resource(Resource=function_arn, Tags=tags)