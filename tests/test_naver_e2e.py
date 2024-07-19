import pytest
from page_objects.registration_page import RegistrationPage
from page_objects.login_page import LoginPage
from utils.twilio_utils import send_verification_code, wait_for_and_get_verification_code


@pytest.fixture(scope="module")
def phone_number():
    return os.environ['VERIFY_PHONE_NUMBER']


def test_register_account_ko(driver):
    registration_page = RegistrationPage(driver)
    registration_page.navigate()
    registration_page.agree_general_conditions()
    registration_page.set_language('ko_KR')
    # need to implement about SMS verification
    registration_page.verify_sms()
    registration_page.register_account("Test User", "1990", "01", "01", "남자", "01012345678")
    assert registration_page.is_registration_successful()


def test_register_account_en(driver):
    registration_page = RegistrationPage(driver)
    registration_page.navigate()
    registration_page.agree_general_conditions()
    registration_page.set_language('en_US')
    # need to implement about SMS verification
    registration_page.verify_sms()
    registration_page.register_account("Test User", "1990", "01", "01", "남자", "08712345678")
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
