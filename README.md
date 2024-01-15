# Trivia Game

Welcome to the Trivia Game! This simple quiz game utilizes the Open Trivia API to fetch and present questions across various categories and difficulty levels. Test your knowledge in multiple-choice or true/false formats and see how many questions you can answer correctly.

## Requirements
- Python 3.x
- Required Python packages: `requests`, `tkinter`, `pygame`

## How to Run
1. Clone the repository to your local machine.
2. Install the required packages using the following command:
    ```bash
    pip install requests pygame
    ```
3. Run the game using the following command:
    ```bash
    python trivia_game.py
    ```

## Game Instructions
1. Select a category from the dropdown menu.
2. Choose the difficulty level: Easy, Medium, or Hard.
3. Specify the number of questions you want to answer (5, 10, 20, or 25).
4. Choose the game type: Multiple Choice or True/False.
5. Optionally, enable the timer checkbox to add a time limit to each question.
6. Click "Continue" to start the game.

## Gameplay
- For each question, read the prompt and select your answer.
- If the timer is enabled, you have a limited time to answer each question.
- After answering all questions, the game will display your final score.

## Credits
- Q&A provided by the [Open Trivia API](https://opentdb.com/).

## Acknowledgments
- The game utilizes the `requests` library for API communication and `pygame` for playing sound.
- Special thanks to the Open Trivia API for providing the trivia questions.

Feel free to contribute to the project or report any issues. Enjoy playing!

