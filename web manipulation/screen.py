import os
import time

def touchscreen_inactive_time(touchscreen_path='/dev/input/eventX', idle_timeout=5):
    """
    Function to track the inactive time of a touchscreen.

    Parameters:
        touchscreen_path (str): Path to the touchscreen device. Default is '/dev/input/eventX'.
        idle_timeout (int): Maximum idle time in seconds. Default is 5.

    Returns:
        int: The inactive time of the touchscreen in seconds.
    """
    last_move_time = time.time()

    try:
        with open(touchscreen_path, 'rb') as f:
            while True:
                event = f.read(24)
                if event:
                    # If there's data, update last move time
                    last_move_time = time.time()
                elif time.time() - last_move_time > idle_timeout:
                    # If no data and idle timeout reached, return inactive time
                    return int(time.time() - last_move_time)
    except KeyboardInterrupt:
        print("Interrupted")

# Example usage:
inactive_time = touchscreen_inactive_time(touchscreen_path='/dev/input/eventX', idle_timeout=5)
print(f"Touchscreen inactive time: {inactive_time} seconds")

