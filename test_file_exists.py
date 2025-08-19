import boto3
from datetime import datetime, timedelta
import pytz
from botocore.exceptions import ClientError

bucket_name = "wbd-syndication-us-east-1-media-qa"
aws_access_key_id = "ASIAU6GDVWX3WEPMMAPG"
aws_secret_access_key = "DJuBbcBRVzkWxwOu2GTSKGsRXfT6h6jiI13IKpn+"
aws_session_token = "FwoGZXIvYXdzEIj//////////wEaDIErHZslZp6DO/f+iSLzAZ5As8hb7pVYUe2e/AGmQn/r9dNUiczhQ9A155JnK2p/SletkbdditMu2LCVuZF674PEIy3L1I4hN9Iozi83GsngRAkNUDwI+AHvTG/ieZkqEH1U8E+YJW90xIQfRgzQ/sxOFI6vvKz26/El7SNThRuWODGKNhAXN2fXx+4fhaKf0nXN6le5+IbEf3epFPgaEk+NVjj0dwQsjWuUGBzv7lYT8WTp5lR7R6HIIjudXyi0lqStHG2fDuuPvaIVtiCOGBaAwNPRNiwBJJE5kQbV4tvxn74TAmswv4H6nle3XWEx/gUy7fmFmnzQyOrbH/q2ICOEIiiYk5LFBjIr4Bm8XgvV7JBkrCQTRS0auqe2wnI+LC8r7xqYX+KCaqWnE5PeIQatyJUyqA=="
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
    object_key = f"assets/graphics/test_qa_image.png"
    result = verify_file_in_s3(bucket_name, object_key)
    print(result)
