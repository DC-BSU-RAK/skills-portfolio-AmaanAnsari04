from tkinter import *
import random
import pygame
import pyttsx3
import threading

main = Tk()
main.geometry("800x600") #window size
main['bg'] = "#66b3da"
main.title("Alexa Joke Teller")

pygame.mixer.init()
#setting up background music
pygame.mixer.music.load("Exercise 2 - Alexa/SV- Cloud Country.mp3")
pygame.mixer.music.play(-1)  #loops music
pygame.mixer.music.set_volume(0.3)  #volume 0-1

#loads the jokes from text file
def Joker(filename="Exercise 2 - Alexa/randomJokes.txt"):
    jokes = [] #empty list to store the jokes
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:  #skip empty lines
                    continue
                if "?" in line: #splits after question mark
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup + "?", punchline.strip()))
    except FileNotFoundError:
        jokes.append(("Joke file not found!", "Please check randomJokes.txt"))
    if not jokes:
        jokes.append(("No jokes loaded!", "Check your jokes file format."))
    return jokes

jokes = Joker()
currentJoke = None #variable for currently displayed joke

# adds text to speech, uses threading to stop tkinter from bugging
def speak(text):
    def _speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 150) #speed speed (wps)
            engine.setProperty("volume", 0.7) # volume 0-1
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"Speech error: {e}")

    #runs in separate thread to stop tts audio freezing
    thread = threading.Thread(target=_speak, daemon=True)
    thread.start()

#switch screens
def showFrame(frame):
    frame.tkraise()

#creates 3 screens for main menu, jokes and instructions
mainmenu = Frame(main, bg="#66b3da")
jokeScreen = Frame(main, bg="#66b3da")
instructionsScreen = Frame(main, bg="#66b3da")

for frame in (mainmenu, jokeScreen, instructionsScreen): #makes frames fit whole screen
    frame.place(relwidth=1, relheight=1)

#Creating title screen text and buttons
Label(mainmenu, text="Alexa's Dad Joke Collection", font=("Arial", 38, "bold"), fg="#034465", bg="#66b3da").pack(pady=80)

Button(mainmenu, text="Start", font=("Arial", 20), fg="#034465",bg="#B9DDF0", command=lambda: showFrame(jokeScreen)).pack(pady=20)

Button(mainmenu, text="Instructions", font=("Arial", 20), fg="#FBFBFB", bg="#07146B", command=lambda: showFrame(instructionsScreen)).pack(pady=20)

#function to show joke screen
def showJoke():
    global currentJoke
    if not jokes:
        setupLabel.config(text="No jokes available!")
        return
    currentJoke = random.choice(jokes)
    setupLabel.config(text=currentJoke[0])
    punchlineLabel.config(text="")
    
    #shows button for tts
    speakButton.pack(side="right", padx=10)
    #hides speak button until the button is pressed and text appears
    punchlineSpeak.pack_forget()

#function to show the punchline
def showPunchline():
    if currentJoke:
        punchlineLabel.config(text=currentJoke[1]) #displays the bunchline
        try:
            pygame.mixer.Sound("Exercise 2 - Alexa/Bamboohit.mp3").play() #sound effect when you press button
        except pygame.error:
            print("Sound effect not found")
        punchlineSpeak.pack(side="right", padx=10) # Show punchline speak button

Label(jokeScreen, text="Alexa's Jokes", font=("Arial", 28, "bold"), fg="#034465", bg="#66b3da").pack(pady=20)

#adds setup and speak button next to each other
setupRow = Frame(jokeScreen, bg="#66b3da")
setupRow.pack(pady=10)

#displays joke setup
setupLabel = Label(setupRow, text="", font=("Arial", 16), wraplength=500, bg="#66b3da", fg="#000022")
setupLabel.pack(side="left") #button on the left side

speakButton = Button(setupRow, text="Speak", font=("Arial", 10), bg="#DBE162", command=lambda: speak(currentJoke[0]) if currentJoke else None)
speakButton.pack_forget() #is hidden

#adds punchline and speak button next to each other
punchlineRow = Frame(jokeScreen, bg="#66b3da")
punchlineRow.pack(pady=10)

#displays joke punchline
punchlineLabel = Label(punchlineRow, text="", font=("Arial", 16, "italic"), wraplength=500, bg="#66b3da", fg="#034465")
punchlineLabel.pack(side="left")

punchlineSpeak = Button(punchlineRow, text="Speak", font=("Arial", 10), bg="#DBE162", command=lambda: speak(currentJoke[1]) if currentJoke else None)
punchlineSpeak.pack_forget() #ishidden

#buttons to navigate joke screen
Button(jokeScreen, text="Alexa tell me a Joke", font=("Arial", 14), bg="#00293D", fg="#64c5ee", command=showJoke).pack(pady=10) #displays joke
Button(jokeScreen, text="Show Punchline", font=("Arial", 14), bg="#64c5ee", fg="#00293D", command=showPunchline).pack(pady=10)  #shows the punchline
Button(jokeScreen, text="Next Joke", font=("Arial", 14), bg="#00293D", fg="#64c5ee", command=showJoke).pack(pady=10) #shows new joke
Button(jokeScreen, text="Back to Menu", font=("Arial", 14), bg="#64c5ee", fg="#00293D", command=lambda: showFrame(mainmenu)).pack(pady=20) #returns back to menu

#instructions screen
Label(instructionsScreen, text="Instructions", font=("Arial", 32, "bold"), fg="#034465", bg="#66b3da").pack(pady=40)

Label(
    instructionsScreen,
    text=(                                                          #instructions to be shown
        "• Click 'Alexa tell me a Joke' to see a setup.\n\n"
        "• Click the 'Speak' button to hear it read out loud.\n\n"
        "• Click 'Show Punchline' to reveal the joke.\n\n"
        "• Click 'Next Joke' to get another one.\n\n"
        "• Use 'Back to Menu' to return to the home screen."),
        font=("Arial", 16), bg="#66b3da", fg="#034465", justify="left").pack(pady=20)

Button(instructionsScreen, text="Back", font=("Arial", 18), command=lambda: showFrame(mainmenu)).pack(pady=30) #return to menu 

showFrame(mainmenu) #start on title screen

main.mainloop()