import requests
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import time
import random
import html
import time
import pygame
import webbrowser

# Fetching categories from API
def fetch_data():
    global difficulty
    global categorys
    global menu
    global question_amount
    global response

    type_of_game = game_type_list.get(game_type.get())

    # Fetching category from menu for the API
    category = categorys.get(menu.get())
    if category is None:
        messagebox.showerror("Error", "Please select a category.")
        # You can choose to return or exit the function here to prevent further execution
        return

    # Fetching difficulty from menu for the API
    if difficulty.get() == "Easy":
        difficulty_url = "&difficulty=easy"
    elif difficulty.get() == "Medium":
        difficulty_url = "&difficulty=medium"
    elif difficulty.get() == "Hard":
        difficulty_url = "&difficulty=hard"
    else:
        difficulty_url = ""

    # Fetching question amount from menu for the API
    question_amount = question_amounts.get()
    if question_amount == "5":
        question_amount = 5
    elif question_amount == "10":
        question_amount = 10
    elif question_amount == "20":
        question_amount = 20
    elif question_amount == "25":
        question_amount = 25
    else:
        messagebox.showerror("Error", "Please select an amount from the list.")
        # You can choose to return or exit the function here to prevent further execution
        return

    # Fetching quiz questions from API
    request = requests.get(f"https://opentdb.com/api.php?amount={question_amount}&category={category}{difficulty_url}&type={type_of_game}")
    response = request.json()

    response_code = response.get('response_code', 5)

    if response_code != 0:
        messagebox.showerror("Error", "An error occured while fetching the questions. Please restart the program.")
        # You can choose to return or exit the function here to prevent further execution
        return
    
    # Start the game
    start_game()

def start_game():
    # clearing the window
    title.pack_forget()
    menu.pack_forget()
    difficulty.pack_forget()
    question_amounts.pack_forget()
    game_type.pack_forget()
    menu_continue.pack_forget()
    timer_checkbox.pack_forget()

    # Game window setup

    # Game index
    global game_index
    global score
    game_index = 0
    score = 0
    timer = 15 # Timer in seconds

    # Function calulated the score
    def score_points():
        global score
        if question_amount == 5:
            score += 20
        elif question_amount == 10:
            score += 10
        elif question_amount == 20:
            score += 5
        elif question_amount == 25:
            score += 4

    # Function to check if the selected answer is correct
    def check_answer(selected_answer):
        # audio for the correct and incorrect answer
        def play_sound(file_path):
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

        
        global game_index
        global score

        correct_answer = html.unescape(response.get("results")[game_index].get("correct_answer"))

        # Check if the selected answer is correct
        if selected_answer == correct_answer:
            # if your on windows you will need to add a r"path-to-audio"
            play_sound("path-to-audio-file-correct")
            messagebox.showinfo("Correct", "Congratulations! You got the question right.")
            score_points()
        else:
            play_sound("path-to-audio-file-incorrect")
            messagebox.showinfo("Incorrect", "Incorrect answer. The correct answer is: " + correct_answer)


        game_index += 1
        # Check if there are more questions left

        if game_index < len(response.get("results")):
            show_next_question()
        else:
            # if your on windows you will need to add a r"path-to-audio"
            play_sound("path-to-audio-file-game-over")
            messagebox.showinfo("Game Over", "You have answered all the questions. Your score is " + str(score) + ".")
            # Clear the window
            for widget in window.winfo_children():
                widget.pack_forget()

            # Cancel the timer that is still running in the background
            global game_over
            game_over = True

            main()

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
                timer_label = tk.Label(window, text=f"Timer: {timer}", font=("Arial", 15))
                timer_label.pack(pady=5)
                countdown(timer, timer_label)

            # Display the progress bar
            progress_bar = ttk.Progressbar(window, length=300, mode='determinate')
            progress_bar.pack(pady=4)

            progress = (game_index + 1) / len(response.get("results")) * 100
            progress_bar['value'] = progress

            score_label = tk.Label(window, text="Score: " + str(score) + "%", font=("Arial", 12))
            score_label.pack(pady=5)


            answers = response.get("results")[game_index].get("incorrect_answers")
            answers.append(correct_answer)
            random.shuffle(answers)

            # Display the question and answers
            question_label = tk.Label(window, text=html.unescape(question), font=("Arial", 20), wraplength=400)
            question_label.pack(pady=20)

            for answer in answers:
                button = tk.Button(window, text=html.unescape(answer), font=("Arial", 13), command=lambda ans=answer: check_answer(ans))
                button.pack(pady=2)

        # True/False game type
        elif game_type == "boolean":

            # Display the timer countdown
            if timer_var.get() == 1:
                timer_label = tk.Label(window, text=f"Timer: {timer}", font=("Arial", 15))
                timer_label.pack(pady=5)
                countdown(timer, timer_label)

            progress_bar = ttk.Progressbar(window, length=300, mode='determinate')
            progress_bar.pack(pady=5)

            progress = (game_index + 1) / len(response.get("results")) * 100
            progress_bar['value'] = progress

            score_label = tk.Label(window, text="Score: " + str(score) + "%", font=("Arial", 12))
            score_label.pack(pady=5)

            # Display the question
            question_label = tk.Label(window, text=html.unescape(question), font=("Arial", 20), wraplength=400)
            question_label.pack(pady=20)

            # Display the true/false buttons
            true_button = tk.Button(window, text="True", font=("Arial", 13), command=lambda: check_answer("True"))
            true_button.pack(pady=2)

            false_button = tk.Button(window, text="False", font=("Arial", 13), command=lambda: check_answer("False"))
            false_button.pack(pady=2)
    
    # These variables are used to tell the timer that the game ins't over yet 
    global game_over
    game_over = False    

    # Timer function that runs in the background and updates the timer label    
    def countdown(seconds, label):
        global update_timer

        def update_timer():
            elapsed_time = time.time() - start_time
            remaining_seconds = max(0, int(seconds - elapsed_time))
            label.config(text=f"Timer: {remaining_seconds}")

            if remaining_seconds > 0 and game_over == False:
                window.after(1000, update_timer)
            elif game_over == True:
                # Stop the timer that is running in the background when the game is over
                return
            else:
                label.config(text="Time's up!")
                messagebox.showinfo("Time's Up", "Sorry, time's up!")
                check_answer("")
        
        update_timer()
    show_next_question()


# Window setup
window = tk.Tk()
window.title("Quiz")

window_width = 500
window_height = 500

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Main menu
def main():
    # Global variables
    global title
    global category_label
    global menu
    global difficulty_label
    global difficulty
    global question_amount_label
    global question_amounts
    global game_type_label
    global game_type
    global menu_continue
    global timer_checkbox
    global timer_var
    global game_type_list
    global categorys

    # Main window content

    title = tk.Label(window, text="Trivia Game", font=("Arial", 30))
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
    category_label = tk.Label(window, text="Category:")
    category_label.pack()

    menu = ttk.Combobox(window, values=list(categorys.keys()))
    menu.set("Select a Category")  # Placeholder text
    menu.pack(pady=4)

    # Difficulty
    difficulty_label = tk.Label(window, text="Difficulty:")
    difficulty_label.pack()

    difficultys = ["Any","Easy", "Medium", "Hard"]
    difficulty = ttk.Combobox(window, values=difficultys)
    difficulty.set(difficultys[0]) # Set the first item as the placeholder text
    difficulty.pack(pady=4)


    # Question amount
    question_amount_label = tk.Label(window, text="Amount of Questions:")
    question_amount_label.pack()

    question_amount_list = ["5", "10", "20", "25"]
    question_amounts = ttk.Combobox(window, values=question_amount_list)
    question_amounts.set(question_amount_list[1]) 
    question_amounts.pack(pady=4)


    # Game type
    game_type_list = {
        "Multiple Choice": "multiple",
        "True/False": "boolean"
    }

    game_type_label = tk.Label(window, text="Game type:")
    game_type_label.pack()

    game_type = ttk.Combobox(window, values=list(game_type_list.keys()))
    game_type.set(list(game_type_list.keys())[0])  # Placeholder text
    game_type.pack(pady=4)

    # Timer checkbox
    timer_var = tk.IntVar()

    timer_checkbox = tk.Checkbutton(window, text="Timer", variable=timer_var)
    timer_checkbox.pack(pady=4)


    menu_continue = tk.Button(window, text="Continue", command=fetch_data)
    menu_continue.pack()

    # Credits
    def open_link(event):
        webbrowser.open("https://opentdb.com/")

    credits = tk.Label(window, text="Q&A from the Open Trivia API", font=("Arial", 12), fg="white", cursor="hand2")
    credits.pack(pady=50)
    credits.bind("<Button-1>", open_link)
    credits.pack(pady=50)

main()
window.mainloop()
