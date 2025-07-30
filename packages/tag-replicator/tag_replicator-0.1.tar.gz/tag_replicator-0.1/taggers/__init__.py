from . import ec2, s3, elb, rds, efs, eks, lambda_fn, logs, backup, sns_sqs

TAGGER_MAP = {
    'ec2': ec2,
    'ebs': ec2,
    'snapshot': ec2,
    's3': s3,
    'elb': elb,
    'rds': rds,
    'efs': efs,
    'eks': eks,
    'lambda': lambda_fn,
    'logs': logs,
    'backup': backup,
    'sns': sns_sqs,
    'sqs': sns_sqs,
}

def get_tagger(resource_type):
    return TAGGER_MAP.get(resource_type.lower())