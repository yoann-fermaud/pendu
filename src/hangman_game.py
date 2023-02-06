import sys
import random
from src.game_settings import *

BACKGROUND = pygame.image.load("assets/background/background_win_lost.png")

HANGMAN_STATUS = 0
WORD = ""
GUESSED = []
TYPING_LIST_LETTERS = ""

FPS = 59
CLOCK = pygame.time.Clock()

IMAGES = []
for element in range(8):
    image = pygame.image.load(f"assets/hangman_pictures/hangman{element}.png")
    IMAGES.append(image)


# -------------------------------|RANDOM WORD|------------------------------- #
# Takes a word from the level list corresponding to the player's choice

def random_word(level):
    if level == "hard":
        with open("data_files/word_hard.txt", "r") as file:
            data = file.read()
            words = data.split()
            return random.choice(words)

    elif level == "medium":
        with open("data_files/word_medium.txt", "r") as file:
            data = file.read()
            words = data.split()
            return random.choice(words)

    elif level == "easy":
        with open("data_files/word_easy.txt", "r") as file:
            data = file.read()
            words = data.split()
            return random.choice(words)

    else:
        with open("data_files/word_custom.txt", "r") as file:
            data = file.read()
            words = data.split()
            return random.choice(words)


# -------------------------------|HANGMAN DRAW|------------------------------- #
# draws the hangman and displays the correct letters as well as all the letters typed by the player

def draw():
    global TYPING_LIST_LETTERS, WORD

    display_word = ""

    for letter in WORD.upper():
        if letter in GUESSED:
            display_word += letter + ""
        else:
            display_word += "_"

    guessed_text = get_font(60).render(display_word, True, "white")
    typing_text = get_font(20).render(TYPING_LIST_LETTERS, True, "white")

    SCREEN.blit(IMAGES[HANGMAN_STATUS], (0, 0))
    SCREEN.blit(guessed_text, (WIDTH / 2 - guessed_text.get_width() / 2, 80))
    SCREEN.blit(typing_text, (WIDTH / 2 - typing_text.get_width() / 2, 700))

    pygame.display.update()


# -------------------------------|SAVE SCORE|------------------------------- #
# Saves the score in case of victory of the player with points adapted to the difficulty

def save_score(level):
    with open("data_files/score.json", "r") as file:
        data = json.load(file)

    username = data["Current username"]

    if username in (i for i in data["Users and Scores"]) and level == "hard":
        data["Users and Scores"][username] += 15
    if username in (i for i in data["Users and Scores"]) and level == "medium":
        data["Users and Scores"][username] += 10
    else:
        data["Users and Scores"][username] += 5

    save_in_json(data)


# -------------------------------|MESSAGE WIN OR LOST|------------------------------- #


def display_message(message):
    global HANGMAN_STATUS, TYPING_LIST_LETTERS
    GUESSED.clear()
    HANGMAN_STATUS = 0
    TYPING_LIST_LETTERS = ""

    text = get_font(100).render(message, True, "white")

    SCREEN.fill("black")
    SCREEN.blit(BACKGROUND, (0, 0))
    SCREEN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

    pygame.display.update()
    pygame.time.delay(1000)


# -------------------------------|MAIN FUNCTION|------------------------------- #


def play_game(level):
    global WORD
    WORD = random_word(level)

    while True:
        global HANGMAN_STATUS, TYPING_LIST_LETTERS

        CLOCK.tick(FPS)
        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    letter_upper = event.unicode.upper()
                    # list of letters typed by the player that will be compared in the draw() function
                    GUESSED.append(letter_upper)
                    if letter_upper not in TYPING_LIST_LETTERS:
                        # List of letters typed by the player
                        TYPING_LIST_LETTERS += letter_upper + ", "
                    if letter_upper not in WORD.upper():
                        HANGMAN_STATUS += 1
        # Win condition
        word_complete = True
        for letter_upper in WORD.upper():
            if letter_upper not in GUESSED:
                word_complete = False
                break
        # Player victory
        if word_complete:
            save_score(level)
            display_message("YOU WON !")
            break
        # Player defeat
        if HANGMAN_STATUS == 8:
            display_message("YOU LOST !")
            break
