# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:38:42 2023

@author: selva
"""

import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import csv
import webbrowser
class SpeechRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Recognition App")
        self.text_widget = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=10)
        self.text_widget.pack(padx=10, pady=10)
        self.recognizer = sr.Recognizer()
        self.listen_button = tk.Button(self.root, text="Start Listening", command=self.start_listening)
        self.listen_button.pack(pady=10)
        # Load CSV data
        self.commands = self.load_commands("inba.csv")
    def start_listening(self):
        self.text_widget.delete(1.0, tk.END)
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.text_widget.insert(tk.END, "Listening...\n")
            audio = self.recognizer.listen(source)
            try:
                user_input = self.recognizer.recognize_google(audio)
                self.text_widget.insert(tk.END, f"You said: {user_input}\n")
                # Check user input against labels in CSV
                relative_url = self.check_user_input(user_input)
                # Open URL based on relative URL from CSV
                if relative_url:
                    full_url = f"{relative_url}"
                    self.text_widget.insert(tk.END, f"Opening URL: {full_url}\n")
                    webbrowser.open(full_url)
                else:
                    self.text_widget.insert(tk.END, "No matching command found in CSV.\n")
            except sr.UnknownValueError:
                self.text_widget.insert(tk.END, "Sorry, could not understand audio.\n")
            except sr.RequestError as e:
                self.text_widget.insert(tk.END, f"Could not request results from Google Speech Recognition service; {e}\n")
    def load_commands(self, csv_file):
        commands = {}
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    label = row['Lable'].lower()
                    relative_url = row['URL']
                    commands[label] = relative_url
        except FileNotFoundError:
            self.text_widget.insert(tk.END, f"Error: {csv_file} not found.\n")
        return commands
    def check_user_input(self, user_input):
        return self.commands.get(user_input.lower())
if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechRecognitionApp(root)
    root.mainloop()