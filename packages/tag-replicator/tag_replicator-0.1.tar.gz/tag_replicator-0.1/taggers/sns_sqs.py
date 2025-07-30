import boto3

def get_tags(resource_arn):
    if ":sns:" in resource_arn:
        sns = boto3.client('sns')
        return sns.list_tags_for_resource(ResourceArn=resource_arn).get('Tags', {})
    elif ":sqs:" in resource_arn:
        sqs = boto3.client('sqs')
        return sqs.list_queue_tags(QueueUrl=resource_arn).get('Tags', {})
    return {}

def apply_tags(resource_arn, tags, clean=False):
    if ":sns:" in resource_arn:
        sns = boto3.client('sns')
        if clean:
            current = get_tags(resource_arn)
            if current:
                sns.untag_resource(ResourceArn=resource_arn, TagKeys=list(current.keys()))
        sns.tag_resource(ResourceArn=resource_arn, Tags=tags)
    elif ":sqs:" in resource_arn:
        sqs = boto3.client('sqs')
        sqs.tag_queue(QueueUrl=resource_arn, Tags=tags)