from tkinter import *
import time

class TypingSpeedTesterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Speed Tester")
        self.master.geometry("600x400")
        
        self.text_to_type = "The quick brown fox jumps over the lazy dog. and then Using Tkinter and what you have learnt about building GUI applications with Python, build a desktop app that assesses your typing speed. Give the user some sample text and detect how many words they can type per minute."
        self.user_input = ""
        self.start_time = None
        
        self.setup_ui()
        
    def setup_ui(self):
        self.instructions_label = Label(self.master, font=("Arial-Bold", 15, "bold"), text="Type the text below:")
        self.instructions_label.pack(pady=10)
        
        self.text_display = Text(self.master, height=7, width=70, wrap=WORD, font=("Arial", 13))
        self.text_display.insert(END, self.text_to_type)
        self.text_display.config(state=DISABLED)
        self.text_display.pack(pady=10)
        
        self.input_entry = Entry(self.master, width=50, font=("Arial", 11))
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<KeyRelease>", self.check_input)
        
        self.result_label = Label(self.master, text="")
        self.result_label.pack(pady=10)
        
    def check_input(self, event):
        if self.start_time is None:
            self.start_time = time.time()
        
        self.user_input = self.input_entry.get()
        
        if self.user_input.lower() == self.text_to_type.lower():
            elapsed_time = time.time() - self.start_time
            speed = len(self.user_input.split()) / (elapsed_time / 60)
            self.result_label.config(text=f"Congratulations! Your typing speed is {speed:.2f} WPM.")
            self.input_entry.config(state=DISABLED)
        
    def reset(self):
        self.user_input = ""
        self.start_time = None
        self.input_entry.delete(0, END)
        self.result_label.config(text="")
        self.input_entry.config(state=NORMAL)