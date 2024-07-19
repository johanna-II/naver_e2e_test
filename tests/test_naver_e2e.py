import pytest
from page_objects.registration_page import RegistrationPage
from page_objects.login_page import LoginPage
from utils.twilio_utils import send_verification_code, wait_for_and_get_verification_code


@pytest.fixture(scope="module")
def phone_number():
    return os.environ['VERIFY_PHONE_NUMBER']


@pytest.mark.parametrize("language", ["ko_KR", "en_US", "zh-Hans_CN", "zh-Hant_TW", "ja_JP"])
def test_valid_register_account(driver, phone_number, language):
    registration_page = RegistrationPage(driver, language)
    registration_page.navigate()
    registration_page.agree_general_conditions()
    registration_page.register_account(
        name="Test User",
        birth_year="1990",
        birth_month="01",
        birth_day="01",
        gender="남자",
        phone=phone_number)

    if language != "ko_KR":
        # Request SMS verification
        registration_page.request_sms_verification()

        # Send verification code using Twilio
        send_verification_code(phone_number)

        # Wait for and retrieve the verification code
        verification_code = wait_for_and_get_verification_code()
        assert verification_code is not None, f"Failed to receive verification code for language: {language}"

        # Enter the verification code
        registration_page.enter_verification_code(verification_code)
    assert registration_page.is_registration_successful()


def test_login_success(driver):
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login("your_test_username", "your_test_password")
    assert login_page.is_login_successful()


def test_login_failure(driver):
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login("wrong_username", "wrong_password")
    assert "아이디 또는 비밀번호가 잘못 입력되었습니다." in login_page.get_error_message()


def test_login_empty_fields(driver):
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login("", "")
    assert "아이디를 입력해 주세요." in login_page.get_id_error_message()
    assert "비밀번호를 입력해 주세요." in login_page.get_pw_error_message()
