import boto3

def get_tags(bucket_name):
    s3 = boto3.client('s3')
    try:
        tagging = s3.get_bucket_tagging(Bucket=bucket_name)
        return {tag['Key']: tag['Value'] for tag in tagging['TagSet']}
    except s3.exceptions.NoSuchTagSet:
        return {}

def apply_tags(bucket_name, tags, clean=False):
    s3 = boto3.client('s3')
    tag_set = [{'Key': k, 'Value': v} for k, v in tags.items()]
    s3.put_bucket_tagging(Bucket=bucket_name, Tagging={'TagSet': tag_set})