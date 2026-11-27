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
    def startQuiz(chosenLevel):
     global level, questionNum, score
    level = chosenLevel
    questionNum = 0
    score = 0
    nextQuestion()


def nextQuestion():
    global questionNum, tries
    if questionNum == 10:
        displayResults()
    else:
        questionNum += 1
        tries = 1
        displayProblem()

def displayProblem():
    global correctAnswer, answerBox
    clearScreen()

    num1 = randomInt(level)
    num2 = randomInt(level)
    operation = decideOperation()

    if operation == "+":
        correctAnswer = num1 + num2
    else:
        correctAnswer = num1 - num2

    tk.Label(window, text="Question " + str(questionNum) + " of 10",
             font=("Arial", 14), bg=BG, fg=DARK).pack(pady=(25, 0))
    tk.Label(window, text="Score: " + str(score),
             font=("Arial", 14, "bold"), bg=BG, fg=DARK).pack(pady=(0, 15))

    card = tk.Frame(window, bg=CARD, padx=30, pady=20)
    card.pack(pady=10)
    tk.Label(card, text=str(num1) + " " + operation + " " + str(num2) + " =",
             font=("Arial", 32, "bold"), bg=CARD, fg=DARK).pack()

    answerBox = tk.Entry(window, font=("Arial", 20), width=10, justify="center",
                         bg=ENTRY_BG, fg=DARK, relief="flat")
    answerBox.pack(pady=15, ipady=6)
    answerBox.focus()
    answerBox.bind("<Return>", lambda event: checkAnswer())

    ttk.Button(window, text="Submit", style="Sage.TButton",
               command=checkAnswer).pack(pady=5)

    ttk.Button(window, text="Back to Menu", style="Sage.TButton",
               command=displayMenu).pack(pady=5)

def isCorrect(userAnswer, correct, attempt):
    if userAnswer == correct:
        messagebox.showinfo("Correct!", "Well done, that's right!")
        return True
    if attempt == 1:
        messagebox.showinfo("Not quite", "That's wrong, but you get one more try.")
    else:
        messagebox.showinfo("Wrong", "Sorry, the right answer was " + str(correct) + ".")
    return False


def checkAnswer():
    global score, tries

    try:
        userAnswer = int(answerBox.get())
    except ValueError:
        messagebox.showwarning("Hold on", "Please type a whole number.")
        return

    if isCorrect(userAnswer, correctAnswer, tries):
        if tries == 1:
            score += 10
        else:
            score += 5
        nextQuestion()
    elif tries == 1:
        tries = 2
        answerBox.delete(0, tk.END)
    else:
        nextQuestion()
def displayResults():
    clearScreen()

    if score > 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    tk.Label(window, text="Quiz finished!", font=("Arial", 26, "bold"),
             bg=BG, fg=DARK).pack(pady=(40, 15))
    tk.Label(window, text="Your score: " + str(score) + " out of 100",
             font=("Arial", 18), bg=BG, fg=DARK).pack(pady=5)
    tk.Label(window, text="Your grade: " + grade,
             font=("Arial", 18, "bold"), bg=BG, fg=DARK).pack(pady=5)
    tk.Label(window, text="Do you want to play again?",
             font=("Arial", 13), bg=BG, fg=DARK).pack(pady=(25, 10))

    ttk.Button(window, text="Play Again", style="Sage.TButton", width=16,
               command=displayMenu).pack(pady=5)
    ttk.Button(window, text="Quit", style="Sage.TButton", width=16,
               command=window.destroy).pack(pady=5)

displayMenu()
window.mainloop()