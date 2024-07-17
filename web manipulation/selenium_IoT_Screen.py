from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions

import time
import pyautogui

URL = 'https://skylerelevate.relayr.io'
REFRESH_INTERVAL_IN_S = 120

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
        
    # def check_login_status(self) -> bool:
    #     try:
    #         # Check if the login form is present
    #         WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'signInName')))
    #         return False  # Login form is present, indicating user is logged out
    #     except:
    #         return True  # Login form not found, indicating user is logged in

    # def handle_login(self) -> None:
    #     if not self.check_login_status():
    #         # User is logged out, perform login
    #         self.login()

    def idle_refresh_handler(self) -> None:
        if pyautogui.position() != self.cursor_pos:
            self.cursor_pos = pyautogui.position()
            self.last_update = time.time()
            return
        
        if time.time() - self.last_update > REFRESH_INTERVAL_IN_S:
            self.browser.refresh()

    def disable_buttons(self) -> None:
        # Logo (top left)
        elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, 'a[@href="/"')))
        self.browser.execute_script("arguments[0].setAttribute('onclick', 'return false;');", elem)
        # Avatar (top right)
        elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, 'button[@data-testid="appbar-avatar"]')))
        self.browser.execute_script("arguments[0].setAttribute('disabled', 'true');", elem)
        # Team (left navigation area)
        elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, 'a[@data-testid="team_button"]')))
        self.browser.execute_script("arguments[0].removeAttribute('onclick');", elem)
        # create reports (left navigation area)
        elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, 'a[@data-testid="create_reports"]')))
        self.browser.execute_script("arguments[0].setAttribute('onclick', 'return false;');", elem)
        # customers_button (left navigation area)
        elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, 'a[@data-testid="customers_button"]')))
        self.browser.execute_script("arguments[0].setAttribute('onclick', 'return false;');", elem)
        # email_notifications (left navigation area)
        elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, 'a[@data-testid="email_notifications"]')))
        self.browser.execute_script("arguments[0].setAttribute('onclick', 'return false;');", elem)
        # Document button (left navigation area)
        elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, 'a[@href="https://se-docu.relayr.io"]')))
        self.browser.execute_script("arguments[0].setAttribute('onclick', 'return false;');", elem)
        # self.browser.execute_script('document.querySelector("[data-testid=\'documentation_button\']").remove();')

    def run(self) -> None:
        while True:
            try:
                # self.handle_login()
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
