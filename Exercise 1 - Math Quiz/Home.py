from tkinter import *
from tkinter import messagebox
import random
import pygame 

root = Tk()
root.title("Math Quiz")
root.geometry("1200x700")
root.config(bg="#A2D729") #main background colour

pygame.mixer.init()
pygame.mixer.music.load("Exercise 1 - Math Quiz/Animal Crossing_ New Horizons Soundtrack - 7AM.mp3")
pygame.mixer.music.play(-1) #loops music
pygame.mixer.music.set_volume(0.5) #volume 0-1

header = 40 #font size for header text
subheader = 20 #font size for subheader text
button_size = 15 #font size for buttons

Question_difficulty = {             #difficulty levels
    "Easy": {"label": "Easy"},
    "Normal": {"label": "Normal"},
    "Hard": {"label": "Hard"}
}

def new_window():   #function to remove all widgets and clear window
    for widget in root.winfo_children():
        widget.destroy()

def Main_Menu():  #displays the main menu with the buttons
    new_window()
    Label(root, text="Math Quiz", font=("Arial", header, "bold"), bg="#A2D729", fg="#FFFFFF").pack(pady=30)
    Label(root, text="Choose your difficulty:", font=("Arial", subheader, "bold"), bg="#A2D729").pack(pady=30)

    for i, (level, text) in enumerate(Question_difficulty.items(), start=1): #buttons for each difficulty
        Button(root, text=f"{i}. {text['label']}", command=lambda l=level: startQuiz(l),
               font=("Arial", button_size, "bold"), bg="#FA824C", fg="white", width=20, height=2).pack(pady=20)
        
    Button(root, text="Instructions", font=("Arial", button_size, "bold"), #button for instructions
        bg="#3C91E6", fg="black", width=20, height=2, command=Instructions_page).pack(pady=20)
    
def Instructions_page():  #instructions page 
    new_window()
    instructions = (
        "• Choose a difficulty level to start the quiz.\n\n"
        "• You will get 10 questions.\n\n"
        "• You have 2 tries to answer each question.\n\n"
        "• You will get 10 points if you answer correctly on your first try.\n\n"
        "• On the second try, you get 5 points.\n\n"
        "• If both attempts are wrong, you earn 0 points.\n\n"
        "• You will see your final score at the end and you may try again."
    )

    Label(root, text=instructions, font=("Arial", 18), bg="#A2D729", fg="black", justify="left").pack(padx=50, pady=20)

    #button to return to menu
    Button(root, text="Back to Main Menu", font=("Arial", button_size, "bold"), bg="#7d0aca", fg="white", width=20, height=2, command=Main_Menu).pack(pady=40)

def Number_range(level): #random number generator with the range separated by difficulty level
    if level == "Easy":
        return random.randint(1, 100)
    elif level == "Normal":
        return random.randint(100, 1000)
    elif level == "Hard":
        return random.randint(1000, 10000)

def random_BIDMAS(level): #random math operation generator based on difficulty level
    if level == "Easy":
        return random.choice(["+", "-"])
    elif level == "Normal":
        return random.choice(["+", "-", "*", "/"])
    elif level == "Hard":
        return random.choice(["+", "-", "*", "/", "^"])

def startQuiz(level): #fumction to start the quiz and set variables to keep track of
    global current_level, score, question_number, correct_answer
    current_level = level
    score = 0
    question_number = 1
    correct_answer = 0
    displayProblem()

def displayProblem(): #function to show users the questions
    new_window()

    global num1, num2, BIDMAS, Answer, question, attempt, answer_entry
    num1 = Number_range(current_level)
    num2 = Number_range(current_level)
    BIDMAS = random_BIDMAS(current_level)
    attempt = 1

    #template for questions and the answers
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

    #displays the question number and question text
    Label(root, text=f"Question {question_number}/10", font=("Arial", subheader, "bold"), bg="#A2D729", fg="#FFFFFF").pack(pady=20)
    Label(root, text=question, font=("Arial", subheader, "bold"), bg="#A2D729", fg="black").pack(pady=10)

    #entry box for answers
    answer_entry = Entry(root, font=("Arial", subheader), justify="center")
    answer_entry.pack(pady=20)
    answer_entry.focus()

    #submit button
    Button(root, text="Submit", font=("Arial", button_size), bg="#5a189a", fg="white", command=checkAnswer).pack(pady=20)

def checkAnswer(): #checks answers for if they are correct, incorrect or invalid and assigns score 
    global score, question_number, attempt, correct_answer

    user_input = answer_entry.get()
    try:
        user_answer = float(user_input)
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a number!")
        return

    if user_answer == Answer: #allows for 2 tries
        correct_answer += 1
        if attempt == 1:
            score += 10
        else:
            score += 5
        messagebox.showinfo("Correct!")
        nextQuestion()
    else:
        if attempt == 1:
            attempt += 1
            messagebox.showwarning("Incorrect", "Try again!")
        else:
            messagebox.showinfo("Game Over", f" Maybe this is not for you. The correct answer was {Answer}")
            nextQuestion()

def nextQuestion(): #func to increase question number and show next question
    global question_number
    question_number += 1
    if question_number > 10:
        showResults()
    else:
        displayProblem()

def showResults(): #shows the final results and has buttons to go back to the main menu or leave
    new_window()   

    Label(root, text=f"You got {correct_answer}/10 questions correct!", font=("Arial", subheader, "bold"), bg="#A2D729", fg="#FFFFFF").pack(pady=40)

    Label(root, text=f"You earned {score} points!", font=("Arial", subheader, "bold"), bg="#A2D729", fg="black").pack(pady=20)

    Button(root, text="Main Menu", font=("Arial", button_size), bg="#7d0aca", fg="white", command=Main_Menu).pack(pady=20)

    Button(root, text="Exit", font=("Arial", button_size), bg="red", fg="white", command=root.quit).pack(pady=10)

Main_Menu()
root.mainloop()
