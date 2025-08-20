from tkinter import *
import time
from . import logic, utils


class TypingSpeedTesterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Speed Tester")
        self.master.geometry("900x700")
        self.master.config(bg="#f0f4ff")

        # timing and content
        self.time_limit = 120  # seconds
        self.start_time = None
        self.timer_id = None

        # new: allow choosing text source
        self.text_source = StringVar(value="literature")

        # generate initial block
        self.text_to_type = utils.generate_text(300, source=self.text_source.get())
        self.user_input = ""

        self.setup_ui()

    def setup_ui(self):
        # header
        self.header = Label(
            self.master, text="Typing Speed Tester",
            font=("Segoe UI", 20, "bold"), bg="#f0f4ff", fg="#2b2d42"
        )
        self.header.pack(pady=(12, 6))

        # source dropdown (styled)
        source_frame = Frame(self.master, bg="#f0f4ff")
        source_frame.pack(pady=(0, 6))
        Label(source_frame, text="Text Source:", bg="#f0f4ff", fg="#374151",
              font=("Segoe UI", 11, "bold")).pack(side=LEFT, padx=(0, 6))

        dropdown = OptionMenu(source_frame, self.text_source, "literature", "random")
        dropdown.config(font=("Segoe UI", 11), bg="#e0e7ff", fg="#1e293b",
                        activebackground="#c7d2fe", activeforeground="#1e293b",
                        relief=GROOVE, width=12)
        dropdown["menu"].config(font=("Segoe UI", 11), bg="white")
        dropdown.pack(side=LEFT)

        # instructions
        self.instructions_label = Label(
            self.master, font=("Segoe UI", 12),
            text="Type the text shown below. Press Start to begin a 2-minute timed test.",
            bg="#f0f4ff", fg="#4b5563"
        )
        self.instructions_label.pack(pady=(0, 10))

        # text display
        self.text_frame = Frame(self.master, bg="#ffffff", bd=1, relief=SOLID)
        self.text_frame.pack(padx=20, pady=10, fill=X)
        self.text_display = Text(
            self.text_frame, height=7, width=90, wrap=WORD,
            font=("Consolas", 12), bg="#ffffff", bd=0
        )
        self.text_display.insert(END, self.text_to_type)
        self.text_display.config(state=DISABLED)
        self.text_display.pack(padx=6, pady=6)

        # input area
        self.input_frame = Frame(self.master, bg="#f0f4ff")
        self.input_frame.pack(pady=(6, 0))
        self.input_entry = Text(self.input_frame, height=4, width=85, font=("Consolas", 12))
        self.input_entry.config(state=DISABLED, bg="#eef2ff")
        self.input_entry.pack()

        # controls
        self.controls_frame = Frame(self.master, bg="#f0f4ff")
        self.controls_frame.pack(pady=10)

        self.start_button = Button(
            self.controls_frame, text="Start", command=self.start_test,
            bg="#10b981", fg="white", padx=12, pady=6
        )
        self.start_button.grid(row=0, column=0, padx=6)

        self.reset_button = Button(
            self.controls_frame, text="Reset", command=self.reset,
            bg="#ef4444", fg="white", padx=12, pady=6
        )
        self.reset_button.grid(row=0, column=1, padx=6)

        self.timer_label = Label(
            self.controls_frame, text="Time: 02:00",
            font=("Segoe UI", 12, "bold"), bg="#f0f4ff", fg="#1f2937"
        )
        self.timer_label.grid(row=0, column=2, padx=12)

        # result area (styled card)
        self.result_card = Frame(self.master, bg="#ffffff", bd=2, relief=RIDGE)
        self.result_card.pack(pady=(12, 12), padx=40, fill=X)

        self.result_labels = {
            "wpm": Label(self.result_card, text="", font=("Segoe UI", 18, "bold"),
                         bg="#ffffff", fg="#1d4ed8"),
            "net_wpm": Label(self.result_card, text="", font=("Segoe UI", 16, "bold"),
                             bg="#ffffff", fg="#059669"),
            "accuracy": Label(self.result_card, text="", font=("Segoe UI", 14),
                              bg="#ffffff", fg="#111827"),
            "correct": Label(self.result_card, text="", font=("Segoe UI", 14),
                             bg="#ffffff", fg="#111827"),
            "total": Label(self.result_card, text="", font=("Segoe UI", 14),
                           bg="#ffffff", fg="#111827"),
        }

        # arrange results in 2 columns inside card
        self.result_labels["wpm"].grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.result_labels["net_wpm"].grid(row=0, column=1, padx=20, pady=10, sticky="w")
        self.result_labels["accuracy"].grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.result_labels["correct"].grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.result_labels["total"].grid(row=2, column=0, padx=20, pady=10, sticky="w")

        # bind typing events
        self.input_entry.bind("<KeyRelease>", self.check_input)

    def start_test(self):
        if self.start_time is not None:
            return

        self.start_time = time.time()
        self.end_time = self.start_time + self.time_limit
        self.input_entry.config(state=NORMAL)
        self.input_entry.delete("1.0", END)
        self.input_entry.focus_set()
        self.update_timer()

    def update_timer(self):
        remaining = int(self.end_time - time.time())
        if remaining < 0:
            remaining = 0

        mins, secs = divmod(remaining, 60)
        self.timer_label.config(text=f"Time: {mins:02d}:{secs:02d}")

        if remaining == 0:
            self.finish_test()
            return

        self.timer_id = self.master.after(1000, self.update_timer)

    def check_input(self, event=None):
        if self.start_time is None:
            return

        self.user_input = self.input_entry.get("1.0", END).strip()
        original_words = self.text_to_type.split()
        user_words = self.user_input.split()

        if len(user_words) >= max(0, len(original_words) - 30):
            additional = utils.generate_text(120, source=self.text_source.get())
            self.text_to_type += " " + additional
            self.text_display.config(state=NORMAL)
            self.text_display.insert(END, " " + additional)
            self.text_display.config(state=DISABLED)

    def finish_test(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

        self.input_entry.config(state=DISABLED)
        end_time = time.time()
        elapsed = min(end_time - self.start_time, self.time_limit)

        original_words = self.text_to_type.split()
        user_words = self.user_input.split()

        correct_words = sum(1 for o, u in zip(original_words, user_words) if o == u)
        total_typed = len(user_words)
        accuracy = (correct_words / total_typed) * 100 if total_typed else 0.0

        gross_wpm = logic.calculate_typing_speed(self.start_time, self.start_time + elapsed, total_typed)
        net_wpm = logic.calculate_typing_speed(self.start_time, self.start_time + elapsed, correct_words)

        # update result labels
        self.result_labels["wpm"].config(text=f"Gross WPM: {gross_wpm:.2f}")
        self.result_labels["net_wpm"].config(text=f"Net WPM: {net_wpm:.2f}")
        self.result_labels["accuracy"].config(text=f"Accuracy: {accuracy:.2f}%")
        self.result_labels["correct"].config(text=f"Correct words: {correct_words}")
        self.result_labels["total"].config(text=f"Total typed: {total_typed}")

    def reset(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

        self.start_time = None
        self.user_input = ""
        self.text_to_type = utils.generate_text(300, source=self.text_source.get())
        self.text_display.config(state=NORMAL)
        self.text_display.delete("1.0", END)
        self.text_display.insert(END, self.text_to_type)
        self.text_display.config(state=DISABLED)

        self.input_entry.config(state=DISABLED)
        self.input_entry.delete("1.0", END)
        self.timer_label.config(text="Time: 02:00")

        for lbl in self.result_labels.values():
            lbl.config(text="")
