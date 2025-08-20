from tkinter import Tk
from src.gui import TypingSpeedTesterApp

def main():
    root = Tk()
    app = TypingSpeedTesterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()