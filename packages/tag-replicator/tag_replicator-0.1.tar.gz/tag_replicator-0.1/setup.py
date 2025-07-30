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
