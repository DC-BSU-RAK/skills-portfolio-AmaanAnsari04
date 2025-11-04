from tkinter import *
from tkinter import messagebox
import random

root = Tk()
root.title("Math Quiz")
root.geometry("1200x700")
root.config(bg="#17A00B")

header_size = 25
question_size = 20
button_size = 15
entry_size = 20

Question_difficulty = {
    "Easy": {"label": "Easy"},
    "Normal": {"label": "Normal"},
    "Hard": {"label": "Hard"}
}

def new_window():
    for widget in root.winfo_children():
        widget.destroy()

def Main_Menu():
    new_window()
    Label(root, text="DIFFICULTY LEVEL", font=("Arial", header_size, "bold"), bg="#17A00B").pack(pady=30)
    for i, (level, text) in enumerate(Question_difficulty.items(), start=1):
        Button(root, text=f"{i}. {text['label']}",
               command=lambda l=level: startQuiz(l),
               font=("Arial", button_size, "bold"),
               bg="#7d0aca", fg="white", width=20, height=2).pack(pady=20)

def Number_range(level):
    if level == "Easy":
        return random.randint(1, 100)
    elif level == "Normal":
        return random.randint(100, 1000)
    elif level == "Hard":
        return random.randint(1000, 10000)

def random_BIDMAS(level):
    if level == "Easy":
        return random.choice(["+", "-"])
    elif level == "Normal":
        return random.choice(["+", "-", "*", "/"])
    elif level == "Hard":
        return random.choice(["+", "-", "*", "/", "^"])

def startQuiz(level):
    global current_level, score, question_number
    current_level = level
    score = 0
    question_number = 1
    displayProblem()

def displayProblem():
    new_window()

    global num1, num2, BIDMAS, Answer, question, attempt, answer_entry

    num1 = Number_range(current_level)
    num2 = Number_range(current_level)
    BIDMAS = random_BIDMAS(current_level)
    attempt = 1

    # Generate question and answer
    if BIDMAS == "^":
        exponent = random.randint(0, 5)
        question = f"{num1} ^ {exponent} = "
        Answer = num1 ** exponent
    elif BIDMAS == "+":
        question = f"{num1} + {num2} = "
        Answer = num1 + num2
    elif BIDMAS == "-":
        question = f"{num1} - {num2} = "
        Answer = num1 - num2
    elif BIDMAS == "/":
        if num2 == 0:
            num2 = 1
        question = f"{num1} / {num2} = "
        Answer = round(num1 / num2, 2)
    elif BIDMAS == "*":
        question = f"{num1} * {num2} = "
        Answer = num1 * num2

    # Display question
    Label(root, text=f"Question {question_number}/10", font=("Arial", question_size, "bold"), bg="#17A00B", fg="#FFFFFF").pack(pady=20)
    Label(root, text=question, font=("Arial", header_size, "bold"), bg="#17A00B", fg="black").pack(pady=10)

    # Entry field
    answer_entry = Entry(root, font=("Arial", entry_size), justify="center")
    answer_entry.pack(pady=20)
    answer_entry.focus()

    # Submit button
    Button(root, text="Submit", font=("Arial", button_size), bg="#5a189a", fg="white", command=checkAnswer).pack(pady=20)

def checkAnswer():
    global score, question_number, attempt

    user_input = answer_entry.get()
    try:
        user_answer = float(user_input)
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a number!")
        return

    if user_answer == Answer:
        if attempt == 1:
            score += 10
        else:
            score += 5
        messagebox.showinfo("Correct!", "Good job!")
        nextQuestion()
    else:
        if attempt == 1:
            attempt += 1
            messagebox.showwarning("Incorrect", "Try again!")
        else:
            messagebox.showinfo("Wrong!", f"The correct answer was {Answer}")
            nextQuestion()

def nextQuestion():
    global question_number
    question_number += 1
    if question_number > 10:
        showResults()
    else:
        displayProblem()

def showResults():
    new_window()


# Start app
Main_Menu()
root.mainloop()
