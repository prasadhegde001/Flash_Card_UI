from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
to_learn = {}
# Reading the Data From CSV file using pandas
try:
    data = pd.read_csv("data/new_record.csv")
except FileNotFoundError:
    old_data = pd.read_csv("data/french_words.csv")
    to_learn = old_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def new_word():
    global current_word, flip_after
    window.after_cancel(flip_after)
    current_word = random.choice(to_learn)
    canvas.itemconfig(canvas_title, text="French", fill="black")
    canvas.itemconfig(canvas_word, text=current_word['French'], fill="black")
    canvas.itemconfig(card_image, image=front_image)
    flip_after = window.after(3000, func=flip_card)


def flip_card():
    global current_word
    canvas.itemconfig(canvas_title, text="English", fill="white")
    canvas.itemconfig(canvas_word, text=current_word["English"], fill="white")
    canvas.itemconfig(card_image, image=back_image)


def words_to_learn():
    to_learn.remove(current_word)
    new_data = pd.DataFrame(to_learn)
    new_data.to_csv("data/new_record")
    new_word()


# UI Element creation
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_after = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=front_image)
canvas.grid(row=0, column=0, columnspan=2)
canvas_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=new_word)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=words_to_learn)
right_button.grid(row=1, column=1)

new_word()
window.mainloop()
