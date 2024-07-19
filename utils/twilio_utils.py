from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import time
import os

# Twilio credentials should be set as environment variables
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_number = os.environ['TWILIO_PHONE_NUMBER']
verify_number = os.environ['VERIFY_PHONE_NUMBER']

client = Client(account_sid, auth_token)


def send_verification_code(phone_number):
    """Send a verification code to the specified phone number."""
    try:
        message = client.messages.create(
            body="Your verification code is: 123456",
            from_=twilio_number,
            to=phone_number
        )
        return message.sid
    except TwilioRestException as e:
        print(f"Error sending SMS: {e}")
        return None


def get_latest_message():
    """Retrieve the latest message sent to the verify number."""
    try:
        messages = client.messages.list(to=verify_number, limit=1)
        if messages:
            return messages[0].body
        return None
    except TwilioRestException as e:
        print(f"Error retrieving SMS: {e}")
        return None


def extract_verification_code(message):
    """Extract the verification code from the message body."""
    if message and "verification code is:" in message:
        return message.split("verification code is:")[1].strip()
    return None


def wait_for_and_get_verification_code(timeout=60, interval=5):
    """Wait for a new message and extract the verification code."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        message = get_latest_message()
        code = extract_verification_code(message)
        if code:
            return code
        time.sleep(interval)
    return None
