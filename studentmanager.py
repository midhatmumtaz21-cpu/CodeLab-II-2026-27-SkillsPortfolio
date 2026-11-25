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