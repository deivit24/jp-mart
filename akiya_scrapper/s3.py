import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from akiya_scrapper.config import akiya_config


def upload_to_s3(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket

    Parameters:
    - file_name: File to upload
    - bucket: Bucket to upload to
    - object_name: S3 object name. If not specified, file_name is used

    Returns:
    - True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Get AWS credentials from environment variables
    aws_access_key_id = akiya_config.aws_access_key_id
    aws_secret_access_key = akiya_config.aws_secret_access_key
    aws_region = akiya_config.aws_default_region

    # Check if credentials are available
    if not aws_access_key_id or not aws_secret_access_key:
        raise NoCredentialsError(
            "AWS credentials not available in environment variables"
        )

    # Create a session using the credentials and region
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    # Create an S3 client
    s3_client = session.client("s3")

    try:
        # Upload the file
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded to {bucket}/{object_name}")
        return True
    except NoCredentialsError as e:
        print(f"Credentials not available: {e}")
        return False
    except PartialCredentialsError as e:
        print(f"Incomplete credentials provided: {e}")
        return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
