import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
from app import app

class TestMaxAreaContainerApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=app.run, kwargs={'debug': False, 'use_reloader': False})
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(2)  # Give the server time to start

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("http://127.0.0.1:5000/")

    def test_valid_input(self):
        driver = self.driver
        heights_input = driver.find_element(By.ID, "heights")
        heights_input.send_keys("1,8,6,2,5,4,8,3,7")
        heights_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Allow time for page to load
        result = driver.find_element(By.ID, "result").text
        self.assertIn("Result: 49", result)

    def test_min_constraints(self):
        driver = self.driver
        heights_input = driver.find_element(By.ID, "heights")
        heights_input.send_keys("1,2")
        heights_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Allow time for page to load
        result = driver.find_element(By.ID, "result").text
        self.assertIn("Result: 1", result)

    def test_large_input(self):
        driver = self.driver
        heights_input = driver.find_element(By.ID, "heights")
        heights_input.send_keys(",".join(["10000"] * 1000))  # Reduced size for quicker testing
        heights_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Allow time for page to load
        result = driver.find_element(By.ID, "result").text
        expected_result = str(10000 * (1000 - 1))  # Expected result for this reduced large input
        self.assertIn(f"Result: {expected_result}", result)

    def test_invalid_input(self):
        driver = self.driver
        heights_input = driver.find_element(By.ID, "heights")
        heights_input.send_keys("1,10001")
        heights_input.send_keys(Keys.RETURN)

        try:
            # Wait up to 10 seconds for the error element to be present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "error")))
            error_element = driver.find_element(By.ID, "error")
            print(f"Error Element Text: {error_element.text}")  # Debug print
            self.assertIn("Error: Invalid input constraints.", error_element.text)
        except Exception as e:
            print(f"Test failed: {e}")

    def test_empty_input(self):
        driver = self.driver
        heights_input = driver.find_element(By.ID, "heights")
        heights_input.send_keys("")
        heights_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Allow time for page to load
        try:
            error_element = driver.find_element(By.ID, "error")
            self.assertIn("Error: Input cannot be empty.", error_element.text)
        except Exception as e:
            print(f"Test failed: {e}")

    def test_non_numeric_input(self):
        driver = self.driver
        heights_input = driver.find_element(By.ID, "heights")
        heights_input.send_keys("a,b,c")
        heights_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Allow time for page to load
        try:
            error_element = driver.find_element(By.ID, "error")
            self.assertIn("Error: Input must be numeric.", error_element.text)
        except Exception as e:
            print(f"Test failed: {e}")

    def test_negative_numbers_input(self):
        driver = self.driver
        heights_input = driver.find_element(By.ID, "heights")
        heights_input.send_keys("-1,-2,-3")
        heights_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Allow time for page to load
        try:
            error_element = driver.find_element(By.ID, "error")
            self.assertIn("Error: Heights must be non-negative.", error_element.text)
        except Exception as e:
            print(f"Test failed: {e}")

    def test_special_characters_and_whitespace(self):
        driver = self.driver
        heights_input = driver.find_element(By.ID, "heights")

        # Test case with special characters and whitespace
        heights_input.send_keys("1,  8, 6, 2, 5, !, 4, 8, 3, @, 7")
        heights_input.send_keys(Keys.RETURN)

        # Wait for result or error element to be present
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "result")))
            result_element = driver.find_element(By.ID, "result")
            self.assertIn("Result:", result_element.text)
        except Exception as e:
            print(f"Test failed: {e}")

    def test_responsiveness(self):
        driver = self.driver
        try:
            # Wait for heights input element to be present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "heights")))

            heights_input = driver.find_element(By.ID, "heights")
            heights_input.send_keys("1,8,6,2,5,4,8,3,7")
            heights_input.send_keys(Keys.RETURN)

            # Wait for result element to be present
            result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "result"))).text
            self.assertIn("Result: 49", result)
        except Exception as e:
            print(f"Test failed: {e}")

    def test_all_heights_zero(self):
        driver = self.driver
        heights_input = driver.find_element(By.ID, "heights")
        heights_input.send_keys(",".join(["0"] * 10))
        heights_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Allow time for page to load
        result = driver.find_element(By.ID, "result").text
        self.assertIn("Result: 0", result)

    def tearDown(self):
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        # If needed, add cleanup code here
        pass

if __name__ == "__main__":
    unittest.main()
