import boto3

def get_tags(log_group_name):
    logs = boto3.client('logs')
    return logs.list_tags_log_group(logGroupName=log_group_name).get('tags', {})

def apply_tags(log_group_name, tags, clean=False):
    logs = boto3.client('logs')
    if clean:
        current = get_tags(log_group_name)
        if current:
            logs.untag_log_group(logGroupName=log_group_name, tags=list(current.keys()))
    logs.tag_log_group(logGroupName=log_group_name, tags=tags)