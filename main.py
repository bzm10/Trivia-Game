import requests
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import random
import html
import time
import pygame
import webbrowser
import os

# Constants for file paths
AUDIO_PATH = r"/Volumes/Benjamin/Coding/Python/GUI/trivia-game/audio/"
CORRECT_SOUND_PATH = os.path.join(AUDIO_PATH, "correct.wav")
INCORRECT_SOUND_PATH = os.path.join(AUDIO_PATH, "incorrect.wav")
GAME_OVER_SOUND_PATH = os.path.join(AUDIO_PATH, "game_over.wav")

# this function fetches the data from the API and starts the game
def fetch_data():
    global difficulty_var
    global category_var
    global question_amount_var
    global game_type_var
    global response

    # Fetching game type from menu for the API
    type_of_game = game_type_list.get(game_type_var.get())

    # Fetching category from menu for the API
    category = categorys.get(category_var.get())
    if category is None:
        messagebox.showerror("Error", "Please select a category.")
        # You can choose to return or exit the function here to prevent further execution
        return

    # Fetching difficulty from menu for the API
    if difficulty_var.get() == "Easy":
        difficulties = "&difficulty=easy"
    elif difficulty_var.get() == "Medium":
        difficulties = "&difficulty=medium"
    elif difficulty_var.get() == "Hard":
        difficulties = "&difficulty=hard"
    else:
        difficulties = ""

    # Fetching question amount from menu for the API
    question_amount = question_amount_var.get()
    if question_amount == "5":
        question_amount = 5
    elif question_amount == "10":
        question_amount = 10
    elif question_amount == "20":
        question_amount = 20
    elif question_amount == "25":
        question_amount = 25
    else:
        # Display an error message if the question amount is not selected
        messagebox.showerror("Error", "Please select an amount from the list.")
        # You can choose to return or exit the function here to prevent further execution
        return

    # Fetching quiz questions from API
    request = requests.get(f"https://opentdb.com/api.php?amount={question_amount}&category={category}{difficulties}&type={type_of_game}")
    response = request.json()

    # Get the response code from the API request
    response_code = response.get('response_code', 5)

    # Check if the API request was successful
    if response_code != 0:
        # Display an error message if the API request was unsuccessful
        messagebox.showerror("Error", "An error occured while fetching the questions. Please restart the program.")
        # You can choose to return or exit the function here to prevent further execution
        return
    
    # Start the game
    start_game()

# this function starts the game and run all the game logic
def start_game():
    # clearing the window
    title.pack_forget()
    category_menu.pack_forget()
    difficulty_optionmenu.pack_forget()
    question_amount_optionmenu.pack_forget()
    game_type_optionmenu.pack_forget()
    menu_continue.pack_forget()
    timer_checkbox.pack_forget()

    # Game window setup

    # Game index
    global game_index
    global score
    game_index = 0
    score = 0
    timer = 15 # Timer in seconds

    
    # this function is used to add points to the score
    def score_points():
        global score
        global question_amount_var
        # Get the selected question amount
        selected_question_amount = int(question_amount_var.get())

        # Score calculation
        if selected_question_amount == 5:
            score += 20
        elif selected_question_amount == 10:
            score += 10
        elif selected_question_amount == 20:
            score += 5
        elif selected_question_amount == 25:
            score += 4

    
    # this function checks if the selected answer is correct or not and displays the correct message accordingly
    def check_answer(selected_answer):
        global game_index
        global score
        
        # audio for the correct and incorrect answer
        def play_sound(file_path):
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

        # Get the correct answer from the API response
        correct_answer = html.unescape(response.get("results")[game_index].get("correct_answer"))

        # Check if the selected answer is correct
        if selected_answer == correct_answer:
            # Play the correct sound
            play_sound(CORRECT_SOUND_PATH)
            # Display the correct message if the selected answer is correct
            messagebox.showinfo("Correct", "Congratulations! You got the question right.")
            # Add points to the score
            score_points()
        else:
            # Play the incorrect sound
            play_sound(INCORRECT_SOUND_PATH)
            # Display the correct answer if the selected answer is incorrect
            messagebox.showinfo("Incorrect", "Incorrect answer. The correct answer is: " + correct_answer)


        game_index += 1
        # Check if there are more questions left

        if game_index < len(response.get("results")):
            show_next_question()
        else:
            # Cancel the timer that is still running in the background
            global game_over
            game_over = True
            
            # Display the game over message and play the game over sound
            play_sound(GAME_OVER_SOUND_PATH)
            messagebox.showinfo("Game Over", "You have answered all the questions. Your score is " + str(score) + ".")

            # Clear the window
            for widget in window.winfo_children():
                widget.pack_forget()

            # Go back to the main menu
            main()

    # this function displays all the questions and answers on the screen and also displays the timer, progress bar and score
    def show_next_question():
        # initializing the timer starting time
        global start_time
        start_time = time.time()
        
        # Clear the window
        for widget in window.winfo_children():
            widget.pack_forget()

        # Get the next question and answers
        question = response.get("results")[game_index].get("question")
        correct_answer = html.unescape(response.get("results")[game_index].get("correct_answer"))
        game_type = response.get("results")[game_index].get("type")

        # Multiple choice game type
        if game_type == "multiple":

            # Display the timer countdown
            if timer_var.get() == 1:
                timer_label = tk.Label(window, text=f"Timer: {timer}", font=("Arial", 15),bg=bg)
                timer_label.pack(pady=5)
                countdown(timer, timer_label)

            # Display the progress bar
            progress_bar = ttk.Progressbar(window, length=300, mode='determinate')
            progress_bar.pack(pady=4)

            progress = (game_index + 1) / len(response.get("results")) * 100
            progress_bar['value'] = progress

            # Display the score
            score_label = tk.Label(window, text="Score: " + str(score) + "%", font=("Arial", 12),bg=bg)
            score_label.pack(pady=5)

            # Get the answers and shuffle them
            answers = response.get("results")[game_index].get("incorrect_answers")
            answers.append(correct_answer)
            random.shuffle(answers)

            # Display the question and answers
            question_label = tk.Label(window, text=html.unescape(question), font=("Arial", 20), wraplength=400,bg=bg)
            question_label.pack(pady=20)

            # Display the buttons
            for answer in answers:
                button = tk.Button(window, text=html.unescape(answer), font=("Arial", 13), command=lambda ans=answer: check_answer(ans),highlightbackground=bg)
                button.pack(pady=2)

        # True/False game type
        elif game_type == "boolean":

            # Display the timer countdown
            if timer_var.get() == 1:
                timer_label = tk.Label(window, text=f"Timer: {timer}", font=("Arial", 15),bg=bg)
                timer_label.pack(pady=5)
                countdown(timer, timer_label)

            # Display the progress bar
            progress_bar = ttk.Progressbar(window, length=300, mode='determinate')
            progress_bar.pack(pady=5)

            progress = (game_index + 1) / len(response.get("results")) * 100
            progress_bar['value'] = progress

            # Display the score
            score_label = tk.Label(window, text="Score: " + str(score) + "%", font=("Arial", 12),bg=bg)
            score_label.pack(pady=5)

            # Display the question
            question_label = tk.Label(window, text=html.unescape(question), font=("Arial", 20), wraplength=400,bg=bg)
            question_label.pack(pady=20)

            # Display the true/false buttons
            true_button = tk.Button(window, text="True", font=("Arial", 13), command=lambda: check_answer("True"),highlightbackground=bg)
            true_button.pack(pady=2)

            false_button = tk.Button(window, text="False", font=("Arial", 13), command=lambda: check_answer("False"),highlightbackground=bg)
            false_button.pack(pady=2)
    
    # These variables are used to tell the timer that the game ins't over yet 
    global game_over
    game_over = False    

    # this function is used to display the timer countdown 
    def countdown(seconds, label):
        def update_timer():
            # Calculate the remaining time
            elapsed_time = time.time() - start_time
            remaining_seconds = max(0, int(seconds - elapsed_time))
            label.config(text=f"Timer: {remaining_seconds}")

            if remaining_seconds > 0 and game_over == False:
                window.after(1000, update_timer)
            elif game_over == True:
                # Stop the timer that is running in the background when the game is over
                return
            else:
                # Display a message box when the timer runs out
                label.config(text="Time's up!")
                messagebox.showinfo("Time's Up", "Sorry, time's up!")
                check_answer("")
        
        update_timer()
    show_next_question()


# Window setup
window = tk.Tk()
window.title("Quiz")

# Window size
window_width = 500
window_height = 500

# Window position
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Center the window
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Disable window resizing
window.resizable(False, False)

# Window background color
bg = "dark blue"
window.configure(bg=bg)

# this function is used to display all the content in the main window
def main():
    # Global variables
    global timer_checkbox
    global question_amount_optionmenu
    global game_type_var
    global game_type_optionmenu
    global title
    global category_menu
    global difficulty_optionmenu
    global menu_continue
    global timer_var
    global game_type_list
    global categorys
    global category_var
    global difficulty_var
    global question_amount_var

    # Main window content

    title = tk.Label(window, text="Trivia Game", font=("Arial", 30),bg=bg)
    title.pack(pady=15)

    # Category list for the API request 
    categorys = {
        "General Knowledge": 9,
        "Entertainment: Books": 10,
        "Entertainment: Film": 11,
        "Entertainment: Music": 12,
        "Entertainment: Musicals & Theatres": 13,
        "Entertainment: Television": 14,
        "Entertainment: Video Games": 15,
        "Entertainment: Board Games": 16,
        "Science & Nature": 17,
        "Science: Computers": 18,
        "Science: Mathematics": 19,
        "Mythology": 20,
        "Sports": 21,
        "Geography": 22,
        "History": 23,
        "Politics": 24,
        "Art": 25,
        "Celebrities": 26,
        "Animals": 27,
        "Vehicles": 28,
        "Entertainment: Comics": 29,
        "Science: Gadgets": 30,
        "Entertainment: Japanese Anime & Manga": 31,
        "Entertainment: Cartoon & Animations": 32
    }

    # Category
    category_label = tk.Label(window, text="Category:",bg=bg)
    category_label.pack()

    category_var = tk.StringVar()
    category_var.set("Select a Category")  # Placeholder text

    category_menu = tk.OptionMenu(window, category_var, *list(categorys.keys()))
    category_menu.config(bg=bg)
    category_menu.pack(pady=4)

    # Difficulty
    difficulty_label = tk.Label(window, text="Difficulty:",bg=bg)
    difficulty_label.pack()

    difficulties = ["Any","Easy", "Medium", "Hard"]
    difficulty_var = tk.StringVar()
    difficulty_var.set(difficulties[0]) # Set the first item as the placeholder text

    difficulty_optionmenu = tk.OptionMenu(window, difficulty_var, *difficulties)
    difficulty_optionmenu.config(bg=bg)
    difficulty_optionmenu.pack(pady=4)


    # Question amount
    question_amount_label = tk.Label(window, text="Amount of Questions:",bg=bg)
    question_amount_label.pack()

    question_amount_list = ["5", "10", "20", "25"]
    question_amount_var = tk.StringVar()
    question_amount_var.set(question_amount_list[1]) 

    question_amount_optionmenu = tk.OptionMenu(window, question_amount_var, *question_amount_list)
    question_amount_optionmenu.config(bg=bg)
    question_amount_optionmenu.pack(pady=4)


    # Game type
    game_type_list = {
        "Multiple Choice": "multiple",
        "True/False": "boolean"
    }

    game_type_label = tk.Label(window, text="Game type:",bg=bg)
    game_type_label.pack()

    game_type_var = tk.StringVar()
    game_type_optionmenu = tk.OptionMenu(window, game_type_var, *list(game_type_list.keys()))
    game_type_var.set(list(game_type_list.keys())[0])  # Placeholder text
    game_type_optionmenu.config(bg=bg)
    game_type_optionmenu.pack(pady=4)

    # Timer checkbox
    timer_var = tk.IntVar()

    timer_checkbox = tk.Checkbutton(window, text="Timer", variable=timer_var,borderwidth=0,background=bg)
    timer_checkbox.pack(pady=4)


    # Continue button in the main window
    menu_continue = tk.Button(window, text="Continue", command=fetch_data,highlightbackground=bg)
    menu_continue.pack(pady=5)

    # Credits
    def open_link(event): 
        webbrowser.open("https://opentdb.com/")

    credits = tk.Label(window, text="Q&A from the Open Trivia API", font=("Arial", 12), fg="white", cursor="hand2",bg=bg)
    credits.pack(pady=50)
    credits.bind("<Button-1>", open_link)
    credits.pack(pady=50)

# Display the main window
main()

# Run the GUI
window.mainloop()
