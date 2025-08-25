from playwright.sync_api import Page, sync_playwright
from dotenv import load_dotenv
import os
import pytest
from pathlib import Path
import time
import boto3
from datetime import datetime, timedelta
import pytz
from botocore.exceptions import ClientError

load_dotenv()

usuario = os.getenv("OKTA_USER")
password = os.getenv("OKTA_PASS")
bucket_name = os.getenv("S3_BUCKET_NAME")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.getenv("AWS_REGION_TOKEN")
region_name = os.getenv("AWS_REGION_NAME")

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

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Cambiar a True en CI/CD
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def page(browser):
    page = browser.new_page()
    yield page

@pytest.mark.file_mover_caso1
@pytest.mark.skip
def test_file_mover_caso1(page: Page):
    # Login en Okta
    page.goto("https://ssodev.wbd.com/app/twdev_clpfilemover_1/exk2080qwj3HLaaVK0h8/sso/saml?SAMLRequest=jZFBb4JAEIX%2FCtk77IIt0o1gbD1oalOj1EMvZlmmSl12KbOgP78Ba2ovpsfJzLxv5r3R%2BFQqp4UaC6Nj4nuMjJMRilJVfNLYvV7BVwNonVOpNPK%2BEZOm1twILJBrUQJyK%2Fl68rLggcd4VRtrpFHEmU9jss380A%2BHoRwEGctzMRwE0ZA4mwsw8Bhx5ogNzDVaoW1MAhbcuyxy%2FbvUj7gf8mDoPYT%2BO3GWP9KPhc4Lvbt9R3YeQj5L06W7fF2nxJkC2kIL26P31lbIKUU0ObTeMcs9aUoqqoraYw7tVqrqo1BQmhbqrU%2FhdAhYxL6On4PZQojNM9tH3TLtTCHOBBHqTvnJaGxKqNdQt4WEt9Xil9Xpub2g1zE1GPearcyu0FQKpTIhD%2BQcBO%2Ftqa8SuP24uBxCkv9hR%2FQKk5yrv%2Bkn3w%3D%3D")

    page.get_by_role("textbox", name="Username").fill(usuario)
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Verify").click()

    # Selección de push
    page.get_by_role("link", name="Select to get a push").click()
    page.wait_for_url("https://file-mover.dev.neo-dev.wbd.com/", timeout=30000)

    # Upload Files
    file_path = Path(__file__).parent / "resources" / "test_qa_image.png"
    page.set_input_files("input[type='file']", str(file_path))    

    page.get_by_role("combobox").click()
    page.get_by_role("option", name="Graphic").click()
    page.get_by_role("combobox").filter(has_text="Select Sub Type").click()
    page.get_by_text("Moving").click()
    page.get_by_role("cell", name="prod uat qa dev local").get_by_label("qa").click()
    #time.sleep(3)
    page.get_by_role("button", name="Upload 1").click()
    time.sleep(5)

    #After upload, verify the file in S3
    object_key = f"assets/graphics/test_qa_image.png"
    assert verify_file_in_s3(bucket_name, object_key), "File verification failed in S3"