import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Safari()

    def test_ll(self):
        user = "workrate"
        pwd = "gounomavs1a"

        # Log In
        driver = self.driver
        driver.maximize_window()
        driver.get("http://localhost:8080/auth")
        elem = driver.find_element_by_id("input-16")
        elem.send_keys(user)
        time.sleep(5)
        elem = driver.find_element_by_id("input-20")
        elem.send_keys(pwd)
        time.sleep(5)
        elem.send_keys(Keys.RETURN)
        elem = driver.find_element_by_xpath("//div/main/div/div/div/div/div/div[3]/form/button")
        elem.click()
        time.sleep(5)

        #Click Tasks
        elem = driver.find_element_by_xpath("//div/header/div/div[3]/a[2]/span")
        elem.click()


        #assert that Task List table is present
        try:
            # attempt to find the Task List table - if found, the user is on the Tasks Page
           elem = driver.find_element_by_xpath("//div/main/div/main/div/div/div[2]/div")
           assert True

        except NoSuchElementException:
            self.fail("Home Page Failed - user is not on the Home Page")
            assert False

        time.sleep(3)


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()
