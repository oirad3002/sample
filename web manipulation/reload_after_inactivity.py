import time
from pynput.mouse import Listener
from datetime import datetime, timedelta
import pyautogui


inactive_threshold = timedelta(seconds=5)  # Adjust the threshold as needed

last_move_time = datetime.now()

def on_move(x, y):
    global last_move_time
    last_move_time = datetime.now()

def reload_webpage():
    # Exit full screen mode
    pyautogui.press('f11')

    # Focus on the address bar for chrome once f6 edge twice f6
    # pyautogui.press('f6')
    pyautogui.press('f6')
    # Type and enter the web address
    web_address = "http://skylerelevate.relayr.io"
    pyautogui.write(web_address)
    pyautogui.press('enter')

    time.sleep(0.2)

    # Enter full screen mode again
    pyautogui.press('f11')

# Create a listener
with Listener(on_move=on_move) as listener:
    try:
        while True:
            current_time = datetime.now()
            inactive_time = current_time - last_move_time
            print(inactive_threshold - inactive_time)

            if inactive_time < timedelta(seconds=6):


                if inactive_time >= inactive_threshold:
                    print(f'Inactive time: {inactive_time}, Reloading webpage...')
                    reload_webpage()

            
            time.sleep(1)  # Sleep for 1 second to avoid high CPU usage
            
    except KeyboardInterrupt:
        pass
