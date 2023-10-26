from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
dic = {}

window = Tk()
window.title("FLASHY")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=10)

canvas = Canvas(width=800, height=526)
front_img = PhotoImage(file="./images/card_front.png")
back_img = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0,column=0, columnspan=2)

# --------------------------------- Get the words using PANDAS ------------------------
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    dic = original_data.to_dict(orient="records")
else:
    dic = data.to_dict(orient="records")


def generate_word():
    global current_card
    global timer
    window.after_cancel(timer)
    current_card = random.choice(dic)
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(canvas_image, image=front_img)
    timer = window.after(5000, func=show_back)

def is_known():
    dic.remove(current_card)
    data = pandas.DataFrame(dic)
    data.to_csv("data/words_to_learn.csv", index=False)
    generate_word()

def show_back():
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
timer = window.after(5000, func=show_back)
generate_word()


correct = PhotoImage(file="./images/right.png")
c_button = Button(image=correct, highlightthickness=0, command=is_known)
c_button.grid(row=1, column=0)

wrong = PhotoImage(file="./images/wrong.png")
w_button = Button(image=wrong, highlightthickness=0, command=generate_word)
w_button.grid(row=1, column=1)



window.mainloop()