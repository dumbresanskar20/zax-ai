from flask import Flask, render_template, request, redirect, url_for, flash # type: ignore
from flask_socketio import SocketIO, emit
from flask_mail import Mail, Message # type: ignore
import threading
import voicecmd  # Ensure this script exists with a working take_command() function
import tkinter as tk
from tkinter import Label
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "secret123"  # For flash messages

# ✅ Email Configuration - Secure using Environment Variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')          # Your Gmail address from .env
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')          # App password from .env
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')    # Sender email address from .env

mail = Mail(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
listening = False

# 🎯 Tkinter Overlay Window for Voice Feedback
def create_overlay():
    global overlay, overlay_label
    overlay = tk.Tk()
    overlay.overrideredirect(True)  # Hide window decorations
    overlay.attributes('-topmost', True)  # Keep window on top
    overlay.geometry("+5+100")  # Position on the screen
    overlay_label = Label(overlay, text="Listening...", font=("Arial", 14), bg="black", fg="white", padx=5, pady=5)
    overlay_label.pack()
    overlay.withdraw()  # Initially hidden
    overlay.mainloop()

def update_overlay(message):
    overlay_label.config(text=message)
    overlay.deiconify()  # Show the overlay
    overlay.after(3000, overlay.withdraw)  # Auto-hide after 3 seconds

# Run Tkinter in a separate thread
tk_thread = threading.Thread(target=create_overlay, daemon=True)
tk_thread.start()

# 🎙️ Voice Command Recognition
def recognize_speech():
    global listening
    while listening:
        try:
            command = voicecmd.take_command()  # Ensure this function works properly
            if command:
                print(f"Recognized: {command}")
                socketio.emit('recognized_word', {'word': command})
                update_overlay(command)
        except Exception as e:
            socketio.emit('recognized_word', {'error': str(e)})
            update_overlay(f"Error: {str(e)}")

# 🔊 Flask-SocketIO Event Handlers
@socketio.on('start_listening')
def start_listening():
    global listening
    if not listening:
        listening = True
        threading.Thread(target=recognize_speech).start()
    emit('recognized_word', {'word': 'Listening...'})
    update_overlay("Listening...")

@socketio.on('stop_listening')
def stop_listening():
    global listening
    listening = False
    emit('recognized_word', {'word': 'Stopped listening.'})
    update_overlay("Stopped Listening.")

# 🌐 Routes
@app.route('/home.html')
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/features.html')
def blog():
    return render_template('features.html')

@app.route('/contact', methods=['GET', 'POST'])
@app.route('/feedback.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        rating = int(request.form.get('rating', 0))

        if not name or not email or not message or rating == 0:
            flash("All fields are required, including rating!", "danger")
            return redirect(url_for('contact'))

        # Create a star display for the email (using ★ for filled stars and ☆ for empty)
        star_display = '★' * rating + '☆' * (5 - rating)

        try:
            # ✅ Confirmation email to the user
            msg_user = Message("Thank You for Your Feedback", recipients=[email])
            msg_user.body = (
                f"Hello {name},\n\n"
                f"Thank you for your valuable feedback!\n"
                f"Your Rating: {star_display} ({rating} stars)\n"
                f"Your Message: {message}\n\n"
                "Best Regards,\nZAX AI"
            )
            mail.send(msg_user)

            # ✅ Notification email to the admin
            admin_email = os.getenv('ADMIN_EMAIL') or os.getenv('EMAIL_USER')
            msg_admin = Message("New ZAX AI Feedback Received", recipients=[admin_email])
            msg_admin.body = (
                f"New feedback received from {name}, \nMail: {email}\n\n"
                f"Rating: {star_display} ({rating} stars)\n"
                f"Message: {message}\n\n"
                "Please review and respond accordingly."
            )
            mail.send(msg_admin)

            flash("Feedback submitted successfully! A confirmation email has been sent.", "success")
        except Exception as e:
            flash(f"Error sending email: {str(e)}", "danger")

        return redirect(url_for('contact'))

    return render_template('feedback.html')

# 🚀 Run the App
if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=5000, allow_unsafe_werkzeug=True)
