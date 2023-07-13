# import time
# import pytest
# from selenium.webdriver.common.by import By
# from tests_logs import BaseClass
# from config_test import setup
# from webdriver_manager.chrome import ChromeDriverManager



# # @pytest.mark.usefixtures("setup")
# class Test_class(BaseClass):
#     def test_signup(self,setup):
#         global driver
#         log = self.log_conf()
#         driver = setup
#         driver.get("http://44.234.84.98:5000/")#slave_1
#         sign_up = driver.find_element(By.CSS_SELECTOR, ".signup")
#         sign_up.click()
#         name = 'inbal'
#         user_name = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Full Name"]').send_keys(name)
#         email = driver.find_element(By.CSS_SELECTOR,'input[placeholder="E-Mail"]').send_keys('inbalamr@gmail.com')
#         sign_up_button = driver.find_element(By.CSS_SELECTOR,'input[value="Sign-Up"]').click()
#         hello_user = driver.find_element(By.CSS_SELECTOR,'.helo').text
#         time.sleep(5)
#         try:
#             assert hello_user == f"Welcome {name}"
#         except AssertionError as msg:
#             log.error(msg)
#             raise AssertionError(msg)
#         else:
#             log.info("Test Passed successfully")


import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging

class Test_class:

    @pytest.fixture(scope="module", autouse=True)
    def setup(self):
        global driver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Ensure GUI is off
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options) # Using ChromeDriver instead of Firefox
        driver.implicitly_wait(5)
        driver.maximize_window()
        yield
        driver.close()
        driver.quit()
        logging.info("Test Completed")

    def test_signup(self, setup):
        global driver
        driver.get("http://34.223.43.96:5000/")  # slave_1
        sign_up = driver.find_element(By.CSS_SELECTOR, ".signup")
        sign_up.click()
        name = 'inbal'
        user_name = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Full Name"]').send_keys(name)
        email = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="E-Mail"]').send_keys('inbalamr@gmail.com')
        sign_up_button = driver.find_element(By.CSS_SELECTOR, 'input[value="Sign-Up"]').click()
        hello_user = driver.find_element(By.CSS_SELECTOR, '.helo').text
        time.sleep(5)
        try:
            assert hello_user == f"Welcome {name}"
        except AssertionError as msg:
            logging.error(msg)
            raise AssertionError(msg)
        else:
            logging.info("Test Passed successfully")