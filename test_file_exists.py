import boto3
from datetime import datetime, timedelta
import pytz
from botocore.exceptions import ClientError

bucket_name = "wbd-syndication-us-east-1-media-qa"
aws_access_key_id = "ASIAU6GDVWX3T432IGYE"
aws_secret_access_key = "cCkFmtY0I2Oonp1Habzj7zixcBtUOub8DrAre+3+"
aws_session_token = "FwoGZXIvYXdzEM7//////////wEaDDH+O5kHQdtDfe27RSLzATUW3JZB8oiZczHtYB7TLFl1f9UTNoL9K8G/7PpJRGbN2X2KW92ZdpU64lNfQj8Y7V+SqebBfDLW5/v8tAN3O0ayDILHSgrMFEeg0pAmVEXHfx6pb5BqbT5aXCcJXytXTzRakP+JDogDgrHs3GIjjq3v35L1UShcFW0LqQ9Y600UyruYa3JdhTGLvW8/op3aO5wNe+sMEzOFODEdloQt/DYibp6F+1ghnwCtHHCsFl4uHUtXy3OWSuXk/2ht3eZw0jjL9x+EAQAu+8XFbmENEnkf19rQdQr7TtosFHAp14LhMJTWko8I/k9HPmors+8G7BQyVCjVzqHFBjIrQ3pg8Zxp7Weplm7nDvx8q0QuRLorNVRiEKaEWfi82BwUyrSd4EEHABM13w=="
region_name = "us-east-1"

def verify_file_in_s3(bucket_name, object_key, max_age_seconds=60):

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )

    try:
        response = s3.head_object(Bucket=bucket_name, Key=object_key)
        last_modified = response['LastModified']

        # Convert both datetimes to UTC for comparison
        now_utc = datetime.now(pytz.utc)
        last_modified_utc = last_modified.replace(tzinfo=pytz.utc)

        age = now_utc - last_modified_utc
        print(f"File age: {age.total_seconds()} seconds")

        if age <= timedelta(seconds=max_age_seconds):
            print("File is within the allowed age.")
            return True
        else:
            print("File is too old.")
            return False
    except ClientError as e:
        print(f"Error checking file: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


if __name__ == "__main__":
    result = False
    object_key = f"assets/graphics/FM_test_8_21_1920x1080.jpg"
    if verify_file_in_s3(bucket_name, object_key):
        object_key = f"assets/graphics/FM_test_8_21_1920x1080.png"
        result = verify_file_in_s3(bucket_name, object_key)
    print(result)