from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils import generate_random_string


class RegistrationPage(BasePage):
    URL = "https://nid.naver.com/user2/V2Join"

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
    GENDER_FIELD = (By.ID, "gender")
    EMAIL_FIELD = (By.ID, "email")
    PHONE_FIELD = (By.ID, "phoneNo")
    JOIN_BUTTON = (By.ID, "btnJoin")

    def navigate(self):
        self.driver.get(self.URL)

    # agree general conditions all
    def agree_general_conditions(self):
        self.wait_for_element(self.SELECT_ALL).click()
        self.wait_for_clickable(self.NEXT_BUTTON).click()

    def verify_sms(self):
        raise NotImplementedError('Need to be implemented')

    def register_account(self, name, birth_year, birth_month, birth_day, gender, phone):
        self.wait_for_element(self.ID_FIELD).send_keys(generate_random_string(8))
        self.wait_for_element(self.PASSWORD_FIELD).send_keys("StrongPassword123!")
        self.wait_for_element(self.PASSWORD_CONFIRM_FIELD).send_keys("StrongPassword123!")
        self.wait_for_element(self.NAME_FIELD).send_keys(name)
        self.wait_for_element(self.BIRTH_YEAR_FIELD).send_keys(birth_year)
        self.wait_for_element(self.BIRTH_MONTH_FIELD).send_keys(birth_month)
        self.wait_for_element(self.BIRTH_DAY_FIELD).send_keys(birth_day)
        self.wait_for_element(self.GENDER_FIELD).send_keys(gender)
        self.wait_for_element(self.EMAIL_FIELD).send_keys(f"{generate_random_string(8)}@example.com")
        self.wait_for_element(self.PHONE_FIELD).send_keys(phone)
        self.wait_for_clickable(self.JOIN_BUTTON).click()

    def is_registration_successful(self):
        return "가입 완료" in self.driver.page_source
