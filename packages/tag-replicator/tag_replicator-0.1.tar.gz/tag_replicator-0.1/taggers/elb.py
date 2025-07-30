import boto3

def get_tags(resource_arn):
    elb = boto3.client('elbv2')
    response = elb.describe_tags(ResourceArns=[resource_arn])
    return {tag['Key']: tag['Value'] for tag in response['TagDescriptions'][0]['Tags']}

def apply_tags(resource_arn, tags, clean=False):
    elb = boto3.client('elbv2')
    if clean:
        elb.remove_tags(ResourceArns=[resource_arn], TagKeys=list(get_tags(resource_arn).keys()))
    elb.add_tags(ResourceArns=[resource_arn], Tags=[{'Key': k, 'Value': v} for k, v in tags.items()])