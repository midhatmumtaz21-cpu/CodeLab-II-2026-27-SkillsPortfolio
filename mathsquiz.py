import random
import tkinter as tk
from tkinter import ttk, messagebox

BG = "#DCE5D2"
DARK = "#2F4A2B"
BTN = "#6F8F5F"
BTN_HOVER = "#587A49"
CARD = "#C2D2B5"
ENTRY_BG = "#EEF3E8"

level = 1
questionNum = 0
score = 0
tries = 1
correctAnswer = 0
answerBox = None

window = tk.Tk()
window.title("Maths Quiz")
window.geometry("520x480")
window.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("Sage.TButton", background=BTN, foreground="white",
                font=("Arial", 13, "bold"), padding=8, borderwidth=0,
                focuscolor=BTN)
style.map("Sage.TButton", background=[("active", BTN_HOVER)])


def clearScreen():  # destroy active widgets before rendering next view
    for widget in window.winfo_children():
        widget.destroy()


def displayMenu():  # render difficulty selection screen
    clearScreen()
    tk.Label(window, text="MATHS QUIZ", font=("Arial", 28, "bold"),
             bg=BG, fg=DARK).pack(pady=(35, 5))
    tk.Label(window, text="DIFFICULTY LEVEL", font=("Arial", 14),
             bg=BG, fg=DARK).pack(pady=(0, 25))

    ttk.Button(window, text="1. Easy (1 digit)", style="Sage.TButton", width=24,
               command=lambda: startQuiz(1)).pack(pady=7)
    ttk.Button(window, text="2. Moderate (2 digits)", style="Sage.TButton", width=24,
               command=lambda: startQuiz(2)).pack(pady=7)
    ttk.Button(window, text="3. Advanced (4 digits)", style="Sage.TButton", width=24,
               command=lambda: startQuiz(3)).pack(pady=7)


def randomInt(chosenLevel):  # generate random int within digit tier bounds
    if chosenLevel == 1:
        return random.randint(1, 9)
    elif chosenLevel == 2:
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)


def decideOperation():  # pick addition or subtraction at random
    if random.randint(1, 2) == 1:
        return "+"
    else:
        return "-"