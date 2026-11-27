import os
import glob
import math
import random
import tkinter as tk
from tkinter import ttk

BG = "#E3E2BE"
DARK = "#3D3D12"
BTN = "#6E7326"
BTN_HOVER = "#565A1B"
CARD = "#CFCE97"
PUNCH = "#7A3E10"

window = tk.Tk()
window.title("Alexa Joke Assistant")
window.geometry("560x420")
window.configure(bg=BG)

folder = os.path.dirname(os.path.abspath(__file__))
matches = glob.glob(os.path.join(folder, "**", "randomJokes.txt"), recursive=True)
jokesFile = matches[0]

jokes = []
with open(jokesFile, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if "?" in line:
            parts = line.split("?", 1)
            jokes.append([parts[0] + "?", parts[1]])

currentJoke = None
animJobs = []


def blend(c1, c2, t):  # linear rgb interpolation between two hex colors
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    mixed = [round(a[i] + (b[i] - a[i]) * t) for i in range(3)]
    return "#%02x%02x%02x" % tuple(mixed)


def later(ms, func, *args):  # schedule callback and track after() timer id
    animJobs.append(window.after(ms, func, *args))


def stopAnimations():  # cancel pending after() callbacks and clear queue
    for job in animJobs:
        window.after_cancel(job)
    animJobs.clear()


def thinking(step=0):  # animate loading dots then start setup typewriter
    if step < 8:
        setupLabel.config(text="Alexa is thinking" + "." * (step % 4))
        later(220, thinking, step + 1)
    else:
        typewriter(currentJoke[0])


def typewriter(text, i=0):  # slice string prefix recursively on timer ticks
    setupLabel.config(text=text[:i])
    if i < len(text):
        later(35, typewriter, text, i + 1)


def fadeIn(step=0, steps=12):  # step punchline foreground color toward target hex
    punchlineLabel.config(fg=blend(CARD, PUNCH, step / steps))
    if step < steps:
        later(45, fadeIn, step + 1, steps)


def pulseTitle(step=0):  # drive continuous sine wave color oscillation
    t = (math.sin(step / 8) + 1) / 2
    titleLabel.config(fg=blend(DARK, BTN, t))
    window.after(60, pulseTitle, step + 1)