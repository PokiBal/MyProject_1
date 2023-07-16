import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging


class Test_class:

    logger = None

    @pytest.fixture(autouse=True)
    def setup(self):
        self.logger = self.setup_logging()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Ensure GUI is off
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)  # Using ChromeDriver instead of Firefox
        driver.implicitly_wait(5)
        driver.maximize_window()
        yield driver
        driver.close()
        driver.quit()
        self.logger.info("Test Completed")

    def setup_logging(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # create a file handler
        handler = logging.FileHandler('logfile.log')
        handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(handler)

        return logger

    def test_signup(self, setup):
        driver = setup
        driver.get("http://35.86.197.56:5000/")  # slave_1
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
            self.logger.error(msg)
            raise AssertionError(msg)
        else:
            self.logger.info("Test Passed successfully")
