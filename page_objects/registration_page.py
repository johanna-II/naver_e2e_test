from selenium.webdriver.common.by import By
from utils.utils import generate_random_string
from .base_page import BasePage


class RegistrationPage(BasePage):
    """
    Register with multi languages. (lang=ko_KR, en_US, zh-Hans_CN, zh-Hant_TW, ja_JP)
    https://nid.naver.com/user2/join/agree?lang={}&realname=
    """
    URL = "https://nid.naver.com/user2/join/agree?lang={}"

    # Locators
    SELECT_ALL = (By.ID, "chk_all")
    NEXT_BUTTON = (By.ID, "btnAgree")
    ID_FIELD = (By.ID, "id")
    PASSWORD_FIELD = (By.ID, "pswd1")
    PASSWORD_CONFIRM_FIELD = (By.ID, "pswd2")
    NAME_FIELD = (By.ID, "name")
    BIRTH_YEAR_FIELD = (By.ID, "yy")
    BIRTH_MONTH_FIELD = (By.ID, "mm")
    BIRTH_DAY_FIELD = (By.ID, "dd")
    EMAIL_FIELD = (By.ID, "email")
    PHONE_FIELD = (By.ID, "phoneNo")
    SEND_CODE_BUTTON = (By.ID, "btnSend")
    JOIN_BUTTON = (By.ID, "btnJoin")
    NATION_BUTTON = (By.ID, "nationNo")
    SMS_CODE_INPUT = (By.ID, "authNo")  # Update this with the actual ID
    LANGUAGE_SELECTOR = (By.ID, "selectLang")

    def __init__(self, driver, language="ko_KR"):
        super().__init__(driver)
        self.language = language
        self.GENDER_FIELD = (By.ID, "gender1") if self.language != 'ko_KR' else (By.ID, "identityGender1")
        self.FOREIGNER_FIELD = (By.ID, "identityGender1")  # 내국인

    def navigate(self):
        """Navigate to the registration page."""
        self.driver.get(self.URL.format(self.language))

    # to change the language on the page if needed
    def select_language(self, language):
        """Change the language on the page."""
        select = Select(self.wait_for_element(self.LANGUAGE_SELECTOR))
        select.select_by_value(language)
        self.language = language
        # Update GENDER_FIELD based on new language
        self.GENDER_FIELD = (By.ID, "gender1") if language != 'ko_KR' else (By.ID, "identityGender1")

    # agree general conditions all
    def agree_general_conditions(self):
        """Agree to all general conditions."""
        self.wait_for_element(self.SELECT_ALL).click()
        self.wait_for_clickable(self.NEXT_BUTTON).click()

    def register_account(self, **kwargs):
        """Fill in the registration form with provided data."""
        self._fill_common_fields(kwargs)
        self._handle_gender_and_nationality(kwargs)
        self._fill_email_and_phone(kwargs)
        # self.wait_for_clickable(self.JOIN_BUTTON).click()

    def _fill_common_fields(self, data):
        """Fill in common fields for all languages."""
        self.wait_for_element(self.ID_FIELD).send_keys(generate_random_string(8))
        self.wait_for_element(self.PASSWORD_FIELD).send_keys("StrongPassword123!")
        self.wait_for_element(self.PASSWORD_CONFIRM_FIELD).send_keys("StrongPassword123!")
        self.wait_for_element(self.NAME_FIELD).send_keys(data.get('name'))
        self.wait_for_element(self.BIRTH_YEAR_FIELD).send_keys(data.get('birth_year'))
        self.wait_for_element(self.BIRTH_MONTH_FIELD).send_keys(data.get('birth_month'))
        self.wait_for_element(self.BIRTH_DAY_FIELD).send_keys(data.get('birth_day'))

    def _handle_gender_and_nationality(self, data):
        """Handle gender and nationality fields based on language."""
        self.wait_for_element(self.GENDER_FIELD).send_keys(data.get('gender'))
        if self.language == 'ko_KR':
            self.wait_for_element(self.FOREIGNER_FIELD).send_keys(data.get('foreigner'))

    def _fill_email_and_phone(self, data):
        """Fill in email and phone fields."""
        self.wait_for_element(self.EMAIL_FIELD).send_keys(f"{generate_random_string(8)}@example.com")
        if self.language == 'ko_KR':
            self.wait_for_element(self.PHONE_FIELD).send_keys(data.get('phone'))

    def request_sms_verification(self):
        """Request SMS verification if not Korean."""
        if self.language != "ko_KR":
            self.wait_for_clickable(self.SEND_CODE_BUTTON).click()

    def enter_verification_code(self, code):
        """Enter SMS verification code if not Korean."""
        if self.language != "ko_KR":
            self.wait_for_element(self.SMS_CODE_INPUT).send_keys(code)

    def submit_registration(self):
        """Submit the registration form."""
        self.wait_for_clickable(self.JOIN_BUTTON).click()

    def is_registration_successful(self):
        """Check if registration was successful based on language-specific messages."""
        success_messages = {
            "ko_KR": "가입 완료",
            "en_US": "Registration Complete",
            "zh-Hans_CN": "注册完成",
            "zh-Hant_TW": "註冊完成",
            "ja_JP": "登録完了"
        }
        return success_messages[self.language] in self.driver.page_source
