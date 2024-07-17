import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pyautogui

URL = 'https://elevate.cedes-connect.com/'
REFRESH_INTERVAL_IN_S = 120
RESTART_INTERVAL_IN_S = 20  # 5 hours

USER_NAME = 'dario.kaelin+demo@cedes.com'
USER_PWD  = '7302Cedes'

class SkylerElevateDashboard:
    
    def __init__(self) -> None:
        browser_options = EdgeOptions()
        browser_options.add_argument("--kiosk")
        browser_options.add_argument("--disable-notifications")

        self.browser = webdriver.Edge(options=browser_options)
        self.browser.get(URL)

        self.last_update = time.time()
        self.start_time = time.time()
        self.cursor_pos = pyautogui.position()

    def login(self) -> bool:
        try:
            elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'signInName')))
            elem.send_keys(USER_NAME)
            elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'password')))
            elem.send_keys(USER_PWD)
            elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'next')))
            elem.click()
            return True
        except TimeoutException:
            return False

    def is_logged_in(self) -> bool:
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='appbar-avatar']")))
            return True
        except TimeoutException:
            return False

    def check_and_login(self) -> None:
        if not self.is_logged_in():
            print("User is logged out. Performing login...")
            if self.login():
                print("Login successful.")
            else:
                print("Login failed.")

    def idle_refresh_handler(self) -> None:
        if pyautogui.position() != self.cursor_pos:
            self.cursor_pos = pyautogui.position()
            self.last_update = time.time()
            return
        
        if time.time() - self.last_update > REFRESH_INTERVAL_IN_S:
            self.last_update = time.time()
            self.browser.refresh()

    def find_element_with_check(self, by, value):
        element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((by, value)))
        self.check_and_login()
        return element

    def disable_buttons(self) -> None:
        try:
            elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='appbar-avatar']")))
            self.browser.execute_script("arguments[0].setAttribute('disabled', 'true');", elem)
        except TimeoutException:
            print(f"Element not found: {value}")

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

                # Restart script after specified interval
                if time.time() - self.start_time > RESTART_INTERVAL_IN_S:
                    print("Restarting script...")
                    self.browser.quit()
                    os.execv(sys.executable, ['python'] + sys.argv)
            except Exception as e:
                print(f"Error occurred: {e}")
            finally:
                time.sleep(0.5)

if __name__ == '__main__':
    app = SkylerElevateDashboard()
    if app.login():
        app.run()
