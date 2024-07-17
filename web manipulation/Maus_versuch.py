import time
import pywebview
from datetime import datetime, timedelta

webpage_url = "https://example.com"  # Replace with the URL of the webpage you want to reload
inactive_threshold = timedelta(seconds=120)  # Adjust the threshold as needed

last_move_time = datetime.now()

def on_move(x, y):
    global last_move_time
    last_move_time = datetime.now()

def reload_webpage():
    pywebview.evaluate_js("location.reload(true);")

pywebview.create_window("Reloadable WebPage", url=webpage_url, js_api=on_move)

try:
    while True:
        current_time = datetime.now()
        inactive_time = current_time - last_move_time

        if inactive_time >= inactive_threshold:
            print(f'Inactive time: {inactive_time}, Reloading webpage...')
            reload_webpage()
            last_move_time = datetime.now()  # Reset last move time
        
        time.sleep(1)  # Sleep for 1 second to avoid high CPU usage

except KeyboardInterrupt:
    pywebview.destroy_window()
