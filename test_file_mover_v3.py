from playwright.sync_api import Page, sync_playwright
import os
from dotenv import load_dotenv
from pathlib import Path
import pytest
import boto3
from datetime import datetime, timedelta
import pytz
from botocore.exceptions import ClientError
#import time

load_dotenv()

usuario = os.getenv("OKTA_USER")
password = os.getenv("OKTA_PASS")
bucket_name = os.getenv("S3_BUCKET_NAME")

# credenciales iniciales (usuario IAM)
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.getenv("AWS_REGION_TOKEN")
region_name = os.getenv("AWS_REGION_NAME")

# ARN del rol
role_arn = os.getenv("AWS_ROLE_ARN")

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

def get_s3_client():
    """
    Asume el rol definido en AWS_ROLE_ARN usando las credenciales del usuario IAM
    y devuelve un cliente de S3 con credenciales temporales.
    """
    # Cliente STS con tus credenciales de usuario
    sts_client = boto3.client(
        "sts",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name,
    )

    # Asumir el rol
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="qa-session"
    )

    credentials = assumed_role["Credentials"]

    # Crear cliente S3 con credenciales temporales
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
        region_name=region_name
    )
    return s3_client

def verify_file_in_s3(bucket_name, object_key, max_age_seconds=60):
    #s3 = get_s3_client()

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )

    try:
        response = s3.head_object(Bucket=bucket_name, Key=object_key)
        last_modified = response["LastModified"]

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
    
def test_example(page: Page) -> None:
    page.goto("https://ssodev.wbd.com/app/twdev_clpfilemover_1/exk2080qwj3HLaaVK0h8/sso/saml?SAMLRequest=jZFBb8IwDIX%2FSpR7mzRoUCIoYuMAGtPQ6DjsgtI2g4w0KXFa%2BPlTy9DYBe1o2X6f%2Fd5oci41aqQDZc0YRyHFk2QEotQVn9Z%2Bb97ksZbg0bnUBnjXGOPaGW4FKOBGlBK4z%2Fl6%2BrLkLKS8ctbb3GqMFrMx3kYDNmBFPBT9bMiKLKJZxjDaXIEspBgtAGq5MOCF8WPMKHsIaBywKI16nMWc9UJG%2Bx8YrX6kH5UplNndvyO7DAGfp%2BkqWL2uU4xmErwywnfovfcVcEIAbCGb8JQVYW5LIqqK%2BFMhm22uq0%2BlZWkb6bYRkecDozE9nr5686UQm2e6j9tl0pqC0RRAulb5yRqoS%2BnW0jUql%2B9vy19Wqxd0gmHLNNIGt2xtd8qQXGidifyAL0Hwzh53k8D9x8X1EJz8DzsiN5jkUv1NP%2FkG")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill(usuario)
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Verify").click()
    page.get_by_role("link", name="Select to get a push").click()
    page.wait_for_url("https://file-mover.dev.neo-dev.wbd.com/", timeout=30000)


    # Upload Files
    file_path = Path(__file__).parent / "resources"
    files = [
        str(file_path / "FM_test_8_21_1920x1080.jpg"),
        str(file_path / "FM_test_8_21_1920x1080.png"),
    ]

    page.set_input_files("input[type='file']", files)    
    #page.locator("input[type='file']").set_input_files(files)


    page.get_by_role("switch").click()
    page.get_by_role("row", name="FM_test_8_21_1920x1080.jpg").get_by_role("combobox").click()
    page.get_by_role("option", name="Graphic").click()
    page.get_by_role("combobox").filter(has_text="Select Sub Type").click()
    page.get_by_text("Moving").click()
    page.get_by_role("row", name="FM_test_8_21_1920x1080.jpg").get_by_label("qa").nth(3).click()
    page.get_by_role("row", name="FM_test_8_21_1920x1080.png 4").get_by_role("combobox").click()
    page.get_by_role("option", name="Graphic").click()
    page.get_by_role("combobox").filter(has_text="Select Sub Type").click()
    page.get_by_role("option", name="OFP-AC").click()
    page.get_by_role("row", name="FM_test_8_21_1920x1080.png 4").get_by_label("qa").nth(3).click()
    page.get_by_role("button", name="Upload 2").click()
    page.get_by_role("button", name="Clear 2 Uploaded").wait_for(state="visible")

    # After upload, verify the file in S3
    object_key1 = f"assets/graphics/FM_test_8_21_1920x1080.jpg"
    assert verify_file_in_s3(bucket_name, object_key1), "File 1 verification failed in S3"
    object_key2 = f"assets/graphics/FM_test_8_21_1920x1080.png"
    assert verify_file_in_s3(bucket_name, object_key2), "File 2 verification failed in S3"

    page.get_by_role("button", name="Pablo").click()
    page.get_by_role("button", name="Sign Out").click()
    #time.sleep(10)
    #page.pause()
    #browser.close()