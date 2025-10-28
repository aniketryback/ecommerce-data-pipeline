import boto3
session = boto3.Session()
print(session.get_credentials())