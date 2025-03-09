import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        root.update()  # Update UI while listening
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        try:
            audio = recognizer.listen(source, timeout=1)
            name = recognizer.recognize_google(audio)
            name_entry.delete(0, tk.END)  # Clear previous text
            name_entry.insert(0, name)  # Insert recognized name
            status_label.config(text="Recognition Successful ✅")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand the audio. Please try again.")
            status_label.config(text="Try Again ❌")
        except sr.RequestError:
            messagebox.showerror("Error", "Could not request results. Check your internet connection.")
            status_label.config(text="Connection Error 🚫")

# GUI Setup
root = tk.Tk()
root.title("Voice Recognition Name Input")
root.geometry("400x200")

# Labels
tk.Label(root, text="Enter Your Name:", font=("Arial", 12)).pack(pady=10)
name_entry = tk.Entry(root, font=("Arial", 14), width=30)
name_entry.pack(pady=5)

# Button to trigger voice input
record_button = tk.Button(root, text="🎤 Speak Name", font=("Arial", 12), command=recognize_speech)
record_button.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="Click the button and say your name.", font=("Arial", 10), fg="blue")
status_label.pack(pady=5)

root.mainloop()
