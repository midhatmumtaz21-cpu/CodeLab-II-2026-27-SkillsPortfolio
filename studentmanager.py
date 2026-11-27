import os
import glob
import tkinter as tk
from tkinter import ttk, messagebox

SIDEBAR = "#6B2A22"
BG = "#EAD7C6"
DARK = "#3B1F1A"
CREAM = "#F6E7DC"
SOFT = "#D9B8A6"
BTN = "#8C3B2E"
BTN_HOVER = "#A8503F"
COPPER = "#B5651D"
BOX = "#F3E6DA"

class Student:  # stores student marks and computes grades

    def __init__(self, code, name, mark1, mark2, mark3, exam):
        self.code = code
        self.name = name
        self.marks = [mark1, mark2, mark3]
        self.exam = exam

    def coursework_total(self):  # sum coursework marks out of 60
        return sum(self.marks)

    def percentage(self):  # calculate overall percentage out of 160 total points
        return (self.coursework_total() + self.exam) / 160 * 100

    def grade(self):  # convert percentage into letter grade
        pct = self.percentage()
        if pct >= 70:
            return "A"
        elif pct >= 60:
            return "B"
        elif pct >= 50:
            return "C"
        elif pct >= 40:
            return "D"
        else:
            return "F"

    def summary(self):  # format full student record string
        return (f"Student name:      {self.name}\n"
                f"Student number:    {self.code}\n"
                f"Coursework total:  {self.coursework_total()} / 60\n"
                f"Exam mark:         {self.exam} / 100\n"
                f"Overall:           {self.percentage():.1f}%\n"
                f"Grade:             {self.grade()}\n")

def load_students(path):  # parse csv marks file into Student objects
    students = []
    with open(path, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    for line in lines[1:]:
        if line.strip() == "":
            continue
        parts = line.split(",")
        students.append(Student(parts[0].strip(), parts[1].strip(),
                                int(parts[2]), int(parts[3]),
                                int(parts[4]), int(parts[5])))
    return students
base_folder = os.path.dirname(os.path.abspath(__file__))
found = glob.glob(os.path.join(base_folder, "**", "studentMarks.txt"), recursive=True)
marks_path = found[0] if found else os.path.join(base_folder, "studentMarks.txt")

window = tk.Tk()
window.title("Student Manager")
window.geometry("920x640")
window.configure(bg=BG)

try:  # load dataset on startup or exit on missing file
    students = load_students(marks_path)
except FileNotFoundError:
    messagebox.showerror("Missing file", "Couldn't find studentMarks.txt")
    window.destroy()
    raise SystemExit

style = ttk.Style()
style.theme_use("clam")
style.configure("Side.TButton", background=BTN, foreground=CREAM,
                font=("Arial", 13, "bold"), padding=10, borderwidth=0,
                focuscolor=BTN, anchor="w")
style.map("Side.TButton", background=[("active", BTN_HOVER)])
style.configure("Find.TButton", background=COPPER, foreground="white",
                font=("Arial", 12, "bold"), padding=8, borderwidth=0,
                focuscolor=COPPER)
style.map("Find.TButton", background=[("active", "#CF7A2E")])

sidebar = tk.Frame(window, bg=SIDEBAR, width=270)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(sidebar, text="STUDENT\nMANAGER", font=("Arial", 24, "bold"),
         bg=SIDEBAR, fg=CREAM, justify="left").pack(anchor="w", padx=24, pady=(30, 2))
tk.Label(sidebar, text="class marks overview", font=("Arial", 11),
         bg=SIDEBAR, fg=SOFT).pack(anchor="w", padx=24, pady=(0, 22))

mainArea = tk.Frame(window, bg=BG)
mainArea.pack(side="right", fill="both", expand=True)

tk.Label(mainArea, text="Results", font=("Arial", 20, "bold"), bg=BG,
         fg=SIDEBAR).pack(anchor="w", padx=25, pady=(24, 8))

output_frame = tk.Frame(mainArea, bg=BG)
output_frame.pack(fill="both", expand=True, padx=(25, 25), pady=(0, 25))
scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")
output_box = tk.Text(output_frame, font=("Courier", 12), bg=BOX, fg=DARK,
                     relief="flat", padx=16, pady=12, state="disabled",
                     yscrollcommand=scrollbar.set)
output_box.pack(side="left", fill="both", expand=True)
scrollbar.config(command=output_box.yview)

output_box.tag_config("name", font=("Courier", 12, "bold"), foreground=SIDEBAR)
output_box.tag_config("summary", font=("Courier", 12, "bold"), foreground=COPPER)

def show_text(text):  # write text to read only output box and highlight headers
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)

    lines = text.split("\n")
    for number in range(len(lines)):
        line = lines[number]
        position = str(number + 1)
        if line.startswith("Student name:"):
            output_box.tag_add("name", position + ".0", position + ".end")
        elif (line.startswith("HIGHEST") or line.startswith("LOWEST") or
              line.startswith("Number of students") or line.startswith("Average")):
            output_box.tag_add("summary", position + ".0", position + ".end")
    output_box.config(state="disabled")

show_text("Pick an option on the left to see the results.")
def view_all():  # render every student record plus class average stats
    text = ""
    for student in students:
        text += student.summary() + "\n"
    average = sum(s.percentage() for s in students) / len(students)
    text += f"Number of students in class: {len(students)}\n"
    text += f"Average percentage mark:     {average:.1f}%\n"
    show_text(text)

ttk.Button(sidebar, text="1   View all students", style="Side.TButton",
           command=view_all).pack(fill="x", padx=20, pady=4)

def view_one():  # filter students by exact code or partial name match
    search = search_entry.get().strip().lower()
    if search == "":
        messagebox.showwarning("Search", "Enter a student name or number first.")
        return
    matches = [s for s in students
               if search == s.code or search in s.name.lower()]
    if not matches:
        show_text("No student found.")
    else:
        show_text("\n".join(s.summary() for s in matches))

tk.Frame(sidebar, bg="#8C4A3E", height=1).pack(fill="x", padx=20, pady=14)

tk.Label(sidebar, text="2   VIEW ONE STUDENT", font=("Arial", 10, "bold"),
         bg=SIDEBAR, fg=SOFT).pack(anchor="w", padx=24)
tk.Label(sidebar, text="name or student number", font=("Arial", 11),
         bg=SIDEBAR, fg=SOFT).pack(anchor="w", padx=24, pady=(4, 2))
search_entry = tk.Entry(sidebar, font=("Arial", 13), bg=BOX, fg=DARK,
                        relief="flat", insertbackground=DARK)
search_entry.pack(fill="x", padx=24, pady=4, ipady=5)
search_entry.bind("<Return>", lambda event: view_one())
ttk.Button(sidebar, text="Search", style="Find.TButton",
           command=view_one).pack(fill="x", padx=20, pady=(6, 4))

def view_highest():  # find and display student with max percentage
    best = max(students, key=lambda s: s.percentage())
    show_text("HIGHEST SCORE\n\n" + best.summary())


def view_lowest():  # find and display student with min percentage
    worst = min(students, key=lambda s: s.percentage())
    show_text("LOWEST SCORE\n\n" + worst.summary())

tk.Frame(sidebar, bg="#8C4A3E", height=1).pack(fill="x", padx=20, pady=14)

ttk.Button(sidebar, text="3   Highest score", style="Side.TButton",
           command=view_highest).pack(fill="x", padx=20, pady=4)
ttk.Button(sidebar, text="4   Lowest score", style="Side.TButton",
           command=view_lowest).pack(fill="x", padx=20, pady=4)

window.mainloop()