# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:19:21 2023

@author: selva
"""
print("hi")
import csv
import webbrowser
import tkinter as tk
from tkinter import Menu
class PersonalAssistant:
    def __init__(self, csv_file):
        self.commands = self.load_commands(csv_file)
    def load_commands(self, csv_file):
        commands = {}
        try:
            with open("inba1.csv", 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    command = row['Command'].lower()
                    url = row['URL']
                    commands[command] = url
        except FileNotFoundError:
            print(f"Error: {csv_file} not found.")
        return commands
    def execute_command(self, command):
        if command in self.commands:
            url = self.commands[command]
            webbrowser.open(url)
        else:
            print(f"Command '{command}' not found.")
class GUI(tk.Tk):
    def __init__(self, personal_assistant):
        super().__init__()
        self.personal_assistant = personal_assistant
        self.title("Personal Assistant")
        menubar = Menu(self)
        self.config(menu=menubar)
        command_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Find What through Menu...", menu=command_menu)
        for command in personal_assistant.commands:
            command_menu.add_command(label=command, command=lambda c=command: 
self.execute_command(c))
    def execute_command(self, command):
        self.personal_assistant.execute_command(command)
if __name__ == "__main__":
    assistant = PersonalAssistant("inba.csv")
    gui = GUI(assistant)
    gui.mainloop()