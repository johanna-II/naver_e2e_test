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

    def __init__(self, driver, language="ko_KR"):
        super().__init__(driver)
        self.language = language

    def navigate(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.wait_for_element(self.ID_FIELD).send_keys(username)
        self.wait_for_element(self.PASSWORD_FIELD).send_keys(password)
        self.wait_for_clickable(self.LOGIN_BUTTON).click()

    def is_login_successful(self):
        return "로그아웃" in self.driver.page_source

    def get_error_message(self):
        mismatch_idpw_messages = {
            "ko_KR": "아이디(로그인 전화번호, 로그인 전용 아이디) 또는 비밀번호가 잘못 되었습니다. 아이디와 비밀번호를 정확히 입력해 주세요.",
            "en_US": "Your ID (login phone number or login ID) or password is incorrect.",
            "zh-Hans_CN": "ID(登录手机号、登录专用ID)或密码错误, 请输入正确的ID和密码。",
            "zh-Hant_TW": "ID(登入手機號碼、登入ID)或密碼錯誤, 請輸入正確的ID與密碼。",
        }
        return mismatch_idpw_messages[self.language] in self.wait_for_element(self.ERROR_MESSAGE).text

    def get_id_error_message(self):
        return self.wait_for_element(self.ID_ERROR_MSG).text

    def get_pw_error_message(self):
        return self.wait_for_element(self.PW_ERROR_MSG).text