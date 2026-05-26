import pyautogui
import pygetwindow as gw
import speech_recognition as sr
import time
import uuid
import sys
import os
import cv2
import webbrowser
import urllib.parse
import winsound
import requests
# 🎯 GLOBAL SETTINGS FOR FASTER RESPONSE
pyautogui.FAILSAFE = False  # Prevents accidental failsafe errors
pyautogui.PAUSE = 0.1  # Reduces delay between actions
# 📌 FUNCTION: WINDOW FOCUS
def focus_application(app_name):
    """Finds an application and brings it to focus."""
    windows = gw.getWindowsWithTitle(app_name)
    if windows:
        win = windows[0]
        win.activate()
        print(f"Focusing on: {app_name}")
    else:
        print(f"Application '{app_name}' not found.")
# 📌 FUNCTION: OPEN APPLICATION
def open_application(app_name):
    """Opens an application and ensures it remains in focus."""
    pyautogui.press('win')
    pyautogui.write(app_name, interval=0.2)
    pyautogui.press('enter')

# 🎵 FUNCTION: VOLUME CONTROL
def control_volume(action):
    """Adjusts system volume."""
    if action == "up":
        pyautogui.press("volumeup", presses=3)
    elif action == "down":
        pyautogui.press("volumedown", presses=3)
# 📸 FUNCTION: SCREENSHOT & CAMERA
def take_screenshot():
    """Captures and saves a screenshot."""
    try:
        file_name = f"screenshot_{uuid.uuid4().hex[:8]}.png"
        pyautogui.screenshot(file_name)
        print(f"Screenshot saved: {file_name}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")
def open_camera():
    """Opens webcam and captures an image."""
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not access the camera.")
        return
    ret, frame = cam.read()
    if ret:
        file_name = f"captured_{uuid.uuid4().hex[:8]}.png"
        cv2.imwrite(file_name, frame)
        print(f"Picture saved: {file_name}")
    else:
        print("Error: Could not capture image.")
    cam.release()
    cv2.destroyAllWindows()
def search_google(query):
    """Opens Google with a search query."""
    encoded_query = urllib.parse.quote(query)
    webbrowser.open(f"https://www.google.com/search?q={encoded_query}")
# 📝 FUNCTION: SET REMINDER
def set_reminder(reminder_text):
    """Displays a reminder after a delay."""
    print(f"Reminder set: {reminder_text}")
    time.sleep(10)  # Adjust as needed
    winsound.Beep(1000, 1000)
def get_weather(location):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={location['lat']}&longitude={location['lon']}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    if "current_weather" in data:
        temp = data["current_weather"]["temperature"]
        condition = data["current_weather"]["weathercode"]
        return f"The current temperature in {location['name']} is {temp}°C."
    else:
        return "Error: Unable to fetch weather data."
# 🔀 FUNCTION: SWITCH APPLICATION
def switch_application(app_name):
    """Switches focus to an open application."""
    windows = gw.getWindowsWithTitle(app_name)
    if windows:
        windows[0].activate()
        print(f"Switched to: {app_name}")
    else:
        print(f"Application '{app_name}' not found.")
# 📌 FUNCTION: WINDOW CONTROL
def minimize_window():
    """Minimizes active window."""
    win = gw.getActiveWindow()
    if win:
        win.minimize()
def maximize_window():
    """Maximizes active window."""
    win = gw.getActiveWindow()
    if win:
        win.maximize()
def save_file():
    """Saves file with a random name."""
    file_name = f"file_{uuid.uuid4().hex[:8]}.txt"
    file_path = os.path.join(os.getcwd(), file_name)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)
    pyautogui.write(file_path)
    pyautogui.press('enter')
    print(f"File saved as {file_path}")
# ❌ FUNCTION: EXIT PROGRAM
def exit_program():
    """Terminates the program."""
    print("Exiting program...")
    sys.exit(0)
# 🎙 FUNCTION: VOICE RECOGNITION
def take_command():
    """Captures and processes voice commands."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.5
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
        except sr.WaitTimeoutError:
            return "Listening... No voice detected."
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in').lower()
        print(f"Command recognized: {query}")
        # COMMAND HANDLING
        if "open" in query:
            open_application(query.replace("open", "").strip())
        elif "switch to" in query:
            switch_application(query.replace("switch to", "").strip())
        elif "focus on" in query:
            focus_application(query.replace("focus on", "").strip())
        elif "close application" in query:
            pyautogui.hotkey('alt', 'f4')
        # VOLUME CONTROL
        elif "volume up" in query or "volume increase" in query:
            control_volume("up")
        elif "volume down" in query or "volume decrease" in query:
            control_volume("down")
        # SCREENSHOT & CAMERA
        elif "take screenshot" in query or "take a screenshot" in query:
            take_screenshot()
        elif "take picture" in query or "take a picture" in query:
            open_camera()
        # GOOGLE SEARCH
        elif "search for" in query:
            search_google(query.replace("search for", "").strip())
        # REMINDER
        elif "set reminder" in query:
            set_reminder(query.replace("set reminder", "").strip())
        elif "get weather" in query:
            location = {'lat': 18.5204, 'lon': 73.8567, 'name': 'Pune'}
            query=get_weather(location)
        # WINDOW MANAGEMENT
        elif "minimize app" in query or "minimise app" in query:
            minimize_window()
        elif "maximize app" in query or "maximise app" in query:
            maximize_window()
        elif "last application focus" in query:
            pyautogui.hotkey('alt', 'tab')
        # EMAIL & FILE ACTIONS
        elif "send new mail" in query:
            pyautogui.hotkey('ctrl', 'n')
        elif "send mail" in query:
            pyautogui.hotkey('ctrl', 'enter')
        elif "save file" in query:
            save_file()
        # Text Entry
        elif "new line" in query:
            pyautogui.press('enter')
        elif "select" in query:
            pyautogui.press('enter')
        # Whatsapp Message
        elif "search chat" in query:
            pyautogui.hotkey('ctrl', 'f')
        elif "new chat" in query:
            pyautogui.hotkey('ctrl', 'n')
        elif "next chat" in query or "down" in query:
            pyautogui.hotkey('ctrl', 'tab')
        elif "previous chat" in query:
            pyautogui.hotkey('ctrl', 'shift', 'tab')
        elif "send message" in query:
            pyautogui.press('enter')
        # Keyboard Shortcuts
        elif "tab" in query:
            pyautogui.press('tab')
        elif "previous" in query:
            pyautogui.hotkey('shift', 'tab')
        elif "next" in query:
            pyautogui.press('tab')
	    # ⌨ KEYBOARD SHORTCUTS
        elif "select all" in query:
            pyautogui.hotkey('ctrl', 'a')
        elif "clear" in query:
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
        elif "cut" in query:
            pyautogui.hotkey('ctrl', 'x')
        elif "copy" in query:
            pyautogui.hotkey('ctrl', 'c')
        elif "paste" in query:
            pyautogui.hotkey('ctrl', 'v')
        elif "undo" in query:
            pyautogui.hotkey('ctrl', 'z')
        elif "redo" in query:
            pyautogui.hotkey('ctrl', 'y')
        elif "scroll up" in query:
            pyautogui.scroll(500)
        elif "scroll down" in query:
            pyautogui.scroll(-500)
        elif "space key" in query:
            pyautogui.press('space')
        elif "up arrow" in query:
            pyautogui.hotkey('up')
        elif "down arrow" in query:
            pyautogui.hotkey('down')
        elif "left arrow" in query:
            pyautogui.hotkey('left')
        elif "right arrow" in query:
            pyautogui.hotkey('right')
        elif "cancel" in query:
            pyautogui.hotkey('esc')
        elif "click" in query:
            pyautogui.click()
        # EXIT PROGRAM
        elif "exit program" in query:
            exit_program()
        else:
            pyautogui.write(query)
            print("Command not recognized.")
        return query
    except sr.UnknownValueError:
        return "Could not understand audio."
    except Exception as e:
        return f"Error: {e}"
# 🔄 MAIN LOOP
if __name__ == "__main__":
    while True:
        try:
            take_command()
        except Exception as e:
            print(f"Error in loop: {e}")