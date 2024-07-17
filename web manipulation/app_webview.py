import webview
import time
from pynput.mouse import Listener
from datetime import datetime, timedelta

window = webview.create_window("Temp", "https://skylerelevate.relayr.io", fullscreen=True)
webview.start(window)

inactive_threshold = timedelta(seconds=10)  # Adjust the threshold as needed

last_move_time = datetime.now()

def on_move(x, y):
    global last_move_time
    last_move_time = datetime.now()

def reload_webpage():
    webview.load_url('http://skylerelevate.relayr.io', window=window)

with Listener(on_move=on_move) as listener:
    try:
        while True:
            current_time = datetime.now()
            inactive_time = current_time - last_move_time
            print(inactive_threshold - inactive_time)

            if inactive_time < timedelta(seconds=11):
                if inactive_time >= inactive_threshold:
                    print(f'Inactive time: {inactive_time}, Reloading webpage...')
                    reload_webpage()

            time.sleep(1)  # Sleep for 1 second to avoid high CPU usage

    except KeyboardInterrupt:
        pass

