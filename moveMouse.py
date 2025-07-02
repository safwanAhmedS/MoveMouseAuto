import pyautogui
import keyboard
import time
import json
import threading
from pynput import mouse

# Global list to store recorded actions
actions = []
recording = False
start_time = None

# Step 1: Function to log mouse clickss
def log_mouse_click(x, y, button, pressed):
    if recording and pressed:  # Only log when mouse is pressed
        actions.append({
            "type": "mouse_click",
            "x": x,
            "y": y,
            "button": button.name,
            "time_diff": time.time() - start_time
        })
        print(f"Mouse clicked at ({x}, {y}) with {button.name} button")

# Step 2: Function to log key presses
def log_key_press(event):
    if recording:
        actions.append({
            "type": "key_press",
            "key": event.name,
            "time_diff": time.time() - start_time
        })

# Step 3: Start recording function
def start_recording():
    global recording, start_time, actions
    actions.clear()  # Clear any previous actions
    start_time = time.time()  # Reset start time
    recording = True
    print("Recording started...")

    # Start listeners for mouse and keyboard events
    mouse_listener = mouse.Listener(on_click=log_mouse_click)
    mouse_listener.start()
    keyboard.hook(log_key_press)

# Step 4: Stop recording function
def stop_recording():
    global recording
    recording = False
    keyboard.unhook_all()
    print("Recording stopped.")
    
    # Save actions to a JSON file
    with open("actions.json", "w") as f:
        json.dump(actions, f)
    print("Recording saved to actions.json.")

# Step 5: Replay actions function
def replay_actions():
    try:
        with open("actions.json", "r") as f:
            recorded_actions = json.load(f)
        print(recorded_actions)
        print("Replaying actions...")
        
        # Replay each action based on its time_diff
        for action in recorded_actions:
            time.sleep(action["time_diff"])  # Delay as per recorded time
            if action["type"] == "mouse_click":
                pyautogui.click(x=action["x"], y=action["y"], button=action["button"])
            elif action["type"] == "key_press":
                keyboard.press_and_release(action["key"])
        
        print("Task replay completed.")
    except FileNotFoundError:
        print("No recording found. Please record actions first.")

# Step 6: Set up user interface with threading to avoid blocking
def start_record_thread():
    threading.Thread(target=start_recording).start()

def stop_record_thread():
    threading.Thread(target=stop_recording).start()

def replay_thread():
    threading.Thread(target=replay_actions).start()

# Step 7: Set up a basic command-line UI
def main():
    print("Press 'r' to start recording, 's' to stop recording, and 'p' to replay actions.")
    
    while True:
        user_input = input("Enter command (r=record, s=stop, p=replay, q=quit): ").strip().lower()
        
        if user_input == 'r':
            start_record_thread()
        elif user_input == 's':
            stop_record_thread()
        elif user_input == 'p':
            replay_thread()
        elif user_input == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
