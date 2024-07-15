from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    URL = "https://nid.naver.com/nidlogin.login"

    # Locators
    ID_FIELD = (By.ID, "id")
    PASSWORD_FIELD = (By.ID, "pw")
    LOGIN_BUTTON = (By.ID, "log.login")
    ERROR_MESSAGE = (By.CLASS_NAME, "error_message")
    ID_ERROR_MSG = (By.ID, "id_error_msg")
    PW_ERROR_MSG = (By.ID, "pw_error_msg")

    def navigate(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.wait_for_element(self.ID_FIELD).send_keys(username)
        self.wait_for_element(self.PASSWORD_FIELD).send_keys(password)
        self.wait_for_clickable(self.LOGIN_BUTTON).click()

    def is_login_successful(self):
        return "로그아웃" in self.driver.page_source

    def get_error_message(self):
        return self.wait_for_element(self.ERROR_MESSAGE).text

    def get_id_error_message(self):
        return self.wait_for_element(self.ID_ERROR_MSG).text

    def get_pw_error_message(self):
        return self.wait_for_element(self.PW_ERROR_MSG).text