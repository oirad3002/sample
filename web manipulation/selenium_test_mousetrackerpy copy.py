from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import TimeoutException

import time
import pyautogui

URL = 'https://skylerelevate.relayr.io'
REFRESH_INTERVAL_IN_S = 600

USER_NAME = 'rd+sales_demo@cedes.com'
USER_PWD  = 'Cedes7302'

class SkylerElevateDashboard:
    
    def __init__(self) -> None:
        browser_options = EdgeOptions()
        browser_options.add_argument("--kiosk")
        browser_options.add_argument("--disable-notifications")

        self.browser = webdriver.Edge(options=browser_options)
        self.browser.get(URL)

        self.last_update = time.time()
        self.cursor_pos = pyautogui.position()

    def login(self) -> bool:
        try:
            # Find the username field by ID
            elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'signInName')))
            elem.send_keys(USER_NAME)
            # Find the password field by ID
            elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'password')))
            elem.send_keys(USER_PWD)
            # Find the submit button by ID and click on it
            elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'next')))
            elem_pos = elem.location
            pyautogui.click(elem_pos['x'] + 60, elem_pos['y'] + 60)
            return True
        except:
            return False

    def idle_refresh_handler(self) -> None:
        # if pyautogui.position() != self.cursor_pos:
        #     self.cursor_pos = pyautogui.position()
        #     return
        
        if time.time() - self.last_update > REFRESH_INTERVAL_IN_S:
            self.last_update = time.time()
            self.browser.get(URL)

    def disable_buttons(self) -> None:
        # try:
        #     elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='appbar-avatar']")))
        #     self.browser.execute_script("arguments[0].setAttribute('disabled', 'true');", elem)
        # except TimeoutException:
        #     print(f"Element not found: {value}")

        elements_to_remove = [
            (By.CSS_SELECTOR, "[href='/']"),
            (By.CSS_SELECTOR, "[data-testid='team_button']"),
            (By.CSS_SELECTOR, "[data-testid='create_reports']"),
            (By.CSS_SELECTOR, "[data-testid='customers_button']"),
            (By.CSS_SELECTOR, "[data-testid='email_notifications']"),
            (By.CSS_SELECTOR, "[data-testid='documentation_button']")
        ]
        
        for by, value in elements_to_remove:
            try:
                element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((by, value)))
                self.browser.execute_script("arguments[0].setAttribute('onclick', 'return false;');", element)
            except TimeoutException:
                print(f"Element not found: {value}")
                self.login()

    def run(self) -> None:
        while True:
            try:
                self.idle_refresh_handler()
                self.disable_buttons()
            except:
                pass
            finally:
                time.sleep(0.5)

if __name__ == '__main__':
    app = SkylerElevateDashboard()
    if app.login():
        app.run()
