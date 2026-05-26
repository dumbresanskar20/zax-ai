# ZAX AI - Voice Activated Virtual Desktop Assistant

Zax AI is an intelligent virtual assistant featuring a premium, futuristic sci-fi web dashboard that seamlessly bridges a browser interface with deep local OS automation. Using real-time WebSockets, Zax AI listens to voice commands to control active windows, open native applications, automate keyboard navigation, fetch real-time weather information, and trigger local hardware (such as cameras and screenshots).

---

## 🚀 Key Features

* **Real-Time Voice Streaming:** Fast, responsive bi-directional communication using WebSockets (`Flask-SocketIO`).
* **Desktop & OS Automation:** Control native applications (Notepad, Excel, Chrome, PowerPoint, Calculator) and manage active windows (focus, switch, minimize, maximize, and alt-tab).
* **Keyboard Hotkey Emulation:** Perform typing and standard editing actions (Select All, Copy, Cut, Paste, Undo, Redo, Scroll Up/Down) entirely hands-free.
* **Hardware Integration:** Programmatically trigger local screenshot captures and webcam photo captures (`OpenCV`).
* **Desktop Overlay HUD:** A native floating Tkinter overlay showing state updates ("Listening...", "Stopped Listening") directly on top of other applications.
* **star-Rating Feedback System:** An interactive feedback portal sending secure verification emails using TLS to users and administrative reports.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.13, Flask, Flask-SocketIO, Flask-Mail
* **Automation:** SpeechRecognition, PyAutoGUI, PyGetWindow, OpenCV, PyAudio
* **Frontend:** HTML5, CSS3, JavaScript, jQuery, Socket.IO Client

---

## 📋 Prerequisites

Since this application interacts directly with your computer's operating system and physical hardware, ensure you have:
1. **Operating System:** Windows (recommended for native OS automation, `winsound`, and window-manipulation features).
2. **Python:** Python 3.12 or 3.13 (stable and supported).
3. **Hardware:** A working microphone (for voice commands) and a webcam (for taking pictures).

---

## 📥 Installation & Setup

Follow these steps to run the application locally on your machine after downloading it from GitHub:

### 1. Clone the Repository
```bash
git clone https://github.com/dumbresanskar20/zax-ai.git
cd zax-ai
```

### 2. Install Dependencies
Make sure your Python environment has the necessary libraries. Run:
```bash
pip install flask flask-socketio flask-mail opencv-python pyaudio pyautogui pygetwindow speechrecognition python-dotenv requests
```
*(Note: If you run into build errors compiling `pyaudio` on Windows, ensure you are running a stable version of Python like 3.12 or 3.13 where pre-built binary wheels are automatically provided).*

### 3. Configure Environment Variables
Since your private credentials are excluded from GitHub for security, you need to create a local `.env` file in the root directory:

1. Create a file named `.env` in the root of the project.
2. Add the following fields:
```env
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-gmail-app-password
ADMIN_EMAIL=your-email@gmail.com
```
> [!IMPORTANT]
> For `EMAIL_PASS`, do **not** use your standard account password. Generate a 16-character **App Password** through your Google Account security panel (under 2-step verification).

---

## 🏃 How to Run the App

1. Start the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to:
   ```url
   http://127.0.0.1:5000
   ```
3. Click the **Start Listening** button on the home dashboard. The native desktop overlay will appear, indicating that the assistant is listening.

---

## 🎙️ Supported Voice Commands

You can speak any of the following commands once the assistant is listening:

| Command Category | Example Phrases | Action Performed |
| :--- | :--- | :--- |
| **Application Launching** | `"open notepad"`, `"open chrome"`, `"open calculator"` | Launches the respective application |
| **Window Management** | `"focus on chrome"`, `"switch to excel"`, `"minimize app"`, `"maximize app"`, `"last application focus"` | Switches window focus, sizes, or runs an Alt+Tab trigger |
| **Hardware Actions** | `"take screenshot"`, `"take picture"` | Captures full-screen snapshot or launches webcam capture |
| **Search & Information** | `"search for space rockets"`, `"get weather"` | Opens Google search in browser; gets current weather in Pune |
| **Editing & Automation** | `"select all"`, `"copy"`, `"paste"`, `"undo"`, `"redo"`, `"scroll down"` | Simulates system-wide hotkeys and mouse actions |
| **Application Controls** | `"save file"`, `"close application"`, `"volume up"`, `"volume down"` | Controls volume, closes the active app, or triggers Save (Ctrl+S) |
| **Shutdown** | `"exit program"` | Terminates the voice assistant script |
