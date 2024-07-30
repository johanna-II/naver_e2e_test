import pytest
from page_objects.registration_page import RegistrationPage
from page_objects.login_page import LoginPage
from utils.twilio_utils import send_verification_code, wait_for_and_get_verification_code

LANGUAGES = ["ko_KR", "en_US", "zh-Hans_CN", "zh-Hant_TW", "ja_JP"]


@pytest.fixture(params=LANGUAGES)
def language(request):
    return request.param


@pytest.fixture
def registration_data(language):
    data = {
        "name": "Test User",
        "birth_year": "1990",
        "birth_month": "01",
        "birth_day": "01",
        "phone": "1234567890",  # This should be replaced with the actual phone number
        "gender": "Male" if language != "ko_KR" else "남자",
    }
    if language == "ko_KR":
        data["foreigner"] = "내국인"
    return data


@pytest.fixture(scope="module")
def phone_number():
    return os.environ['VERIFY_PHONE_NUMBER']


def test_valid_register_account(driver, language, registration_data):
    registration_page = RegistrationPage(driver, language)
    registration_page.navigate()
    registration_page.agree_general_conditions()
    registration_page.register_account(**registration_data)

    if language != "ko_KR":
        verify_sms(registration_page, registration_data["phone"], language)

    registration_page.submit_registration()

    assert registration_page.is_registration_successful(), f"Registration failed for language: {language}"


def verify_sms(registration_page, phone_number, language):
    registration_page.request_sms_verification()
    send_verification_code(phone_number)
    verification_code = wait_for_and_get_verification_code()
    assert verification_code is not None, f"Failed to receive verification code for language: {language}"
    registration_page.enter_verification_code(verification_code)


def test_invalid_register_account(driver, language, registration_data):
    # Test with invalid data
    invalid_data = registration_data.copy()
    invalid_data["birth_year"] = "invalid_year"

    registration_page = RegistrationPage(driver, language)
    registration_page.navigate()
    registration_page.agree_general_conditions()

    registration_page.register_account(**invalid_data)
    registration_page.submit_registration()

    assert not registration_page.is_registration_successful(), f"Registration should have failed for language: {language}"


@pytest.mark.parametrize("missing_field", ["name", "birth_year", "birth_month", "birth_day", "phone", "gender"])
def test_missing_required_field(driver, language, registration_data, missing_field):
    incomplete_data = registration_data.copy()
    incomplete_data.pop(missing_field)

    registration_page = RegistrationPage(driver, language)
    registration_page.navigate()
    registration_page.agree_general_conditions()

    registration_page.register_account(**incomplete_data)
    registration_page.submit_registration()

    assert not registration_page.is_registration_successful(), f"Registration should have failed for language: {language} with missing {missing_field}"


def test_login_success(driver):
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login("your_test_username", "your_test_password")
    assert login_page.is_login_successful()


@pytest.mark.skipif("language == 'ja_JP'", reason="Skipping Japanese language test")
def test_login_failure(driver, language):
    login_page = LoginPage(driver, language)
    login_page.navigate()
    login_page.login("wrong_username", "wrong_password")
    assert not login_page.is_login_successful()
    assert login_page.get_error_message(), f"Login should have failed for language: {language}"


def test_login_empty_fields(driver):
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login("", "")
    assert "아이디를 입력해 주세요." in login_page.get_id_error_message()
    assert "비밀번호를 입력해 주세요." in login_page.get_pw_error_message()
