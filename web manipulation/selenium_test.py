from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions

import time
import pyautogui

website_url = 'https://skylerelevate.relayr.io'
refresh_interval = 120

browser_options = EdgeOptions()
browser_options.add_argument("--kiosk")
browser_options.add_argument("--disable-notifications")

# Create a new Edge WebDriver instance
browser = webdriver.Edge(options=browser_options)

try:
    # Open the website in fullscreen mode
    browser.get(website_url)

    # Find the username field by ID
    username_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'signInName')))
    username_field.send_keys('rd+sales_demo@cedes.com')
    # Find the password field by ID
    password_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    password_field.send_keys('Cedes7302')
    # Find the submit button by ID and click on it
    submit_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'next')))
    button_position = submit_button.location
    pyautogui.click(button_position['x'] + 60, button_position['y'] + 60)

    cursor_pos = pyautogui.position()
    while True:
        time.sleep(refresh_interval)
        if pyautogui.position() != cursor_pos:
            cursor_pos = pyautogui.position()
        else:
            browser.refresh()
            print("Page refreshed")

except KeyboardInterrupt:
    pass

finally:
    browser.quit()
