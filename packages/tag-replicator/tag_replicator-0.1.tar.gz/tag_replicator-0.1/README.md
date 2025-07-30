# Tag Replicator CLI

A command-line tool to replicate AWS resource tags from one resource to another, with optional cleaning.

## 🧩 Supported Resources

- EC2 (including EBS, Snapshots)
- S3 Buckets
- ELB (Application/Network Load Balancers)
- RDS (DB Instances, Clusters)
- EFS (Elastic File Systems)
- EKS (Kubernetes Clusters)
- Lambda Functions
- CloudWatch Log Groups
- Backup Vaults
- SNS Topics
- SQS Queues

## 🚀 Usage

```bash
python tag-replicate.py --type=<resource_type> --model=<source_id> --target=<target_id> [--clean]
```

### Parameters

- `--type`   : Type of AWS resource (e.g., ec2, s3, rds, lambda, etc.)
- `--model`  : Resource ID or ARN of the source resource (tags copied from here)
- `--target` : Resource ID or ARN of the target resource (tags applied here)
- `--clean`  : Optional flag. If set, tags not in source will be removed from the target.

### Example

```bash
python tag-replicate.py --type=ec2 --model=i-0123456789abcdef0 --target=i-0fedcba9876543210
```

```bash
python tag-replicate.py --type=s3 --model=my-source-bucket --target=my-target-bucket --clean
```

## ⚙️ Setup

Requires Python 3 and `boto3` library.

```bash
pip install boto3
```

## 📁 Project Structure

```
replicate_tags/
├── main.py (rename to tag-replicate.py)
├── taggers/
│   ├── __init__.py
│   ├── ec2.py
│   ├── s3.py
│   ├── elb.py
│   ├── rds.py
│   ├── efs.py
│   ├── eks.py
│   ├── lambda_fn.py
│   ├── logs.py
│   ├── backup.py
│   └── sns_sqs.py
```

## 📦 Packaging as CLI (Optional)

If you want to install it system-wide with `pip`:

1. Create `setup.py` and `setup.cfg`
2. Rename `main.py` to `tag_replicate.py`
3. Add entry point:

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name='tag-replicator',
    version='0.1',
    packages=find_packages(),
    py_modules=['tag_replicate'],
    entry_points={
        'console_scripts': [
            'tag-replicate=tag_replicate:main',
        ],
    },
    install_requires=['boto3'],
)
```

Then:

```bash
pip install .
tag-replicate --help
```
