import sys
from src.game_settings import *
from src.button import Button
from src.hangman_game import play_game

BACKGROUND = pygame.image.load("assets/background/background_menu.png")


# -------------------------------|FUNCTION : BACK|------------------------------- #


def save_word(word):
    with open("data_files/word_custom.txt", "r") as file:
        data = file.read()

    if word not in data:
        data += "\n" + word

    with open("data_files/word_custom.txt", "w") as file:
        file.write(data)


def save_username(username):
    try:
        with open("data_files/score.json", "r") as file:
            data = json.load(file)

    except ValueError:
        data = {
            "Current username": "",
            "Users and Scores": {}
        }

    data["Current username"] = username

    if username not in [i for i in data["Users and Scores"]]:
        data["Users and Scores"][username] = 0

    save_in_json(data)


def clear_current_username():
    with open("data_files/score.json", "r") as file:
        data = json.load(file)

    data["Current username"] = ""

    save_in_json(data)


def sort_score():
    try:
        with open("data_files/score.json", "r") as file:
            data = json.load(file)
    except ValueError:
        data = {
            "Current username": "",
            "Users and Scores": {}
        }

    sorted_scores = dict(sorted(data["Users and Scores"].items(), key=lambda item: item[1], reverse=True))
    data["Users and Scores"] = sorted_scores
    save_in_json(data)


def print_score():
    try:
        with open("data_files/score.json", "r") as file:
            data = json.load(file)
    except ValueError:
        data = {
            "Current username": "",
            "Users and Scores": {}
        }

    increment_blit = 0
    dict_value = 0

    for key, value in data["Users and Scores"].items():
        if dict_value < 6:
            # Display key and value on separate lines
            text = f"{key}: {value}"
            label = get_font(25).render(text, True, "white")
            SCREEN.blit(label, (WIDTH / 2 - label.get_width() / 2, 200 + increment_blit))
            increment_blit += 50
            dict_value += 1
        else:
            break


# -------------------------------|DESIGN : PLAY AND CUSTOM MENU|------------------------------- #


def play_custom_menu():
    list_username = ""
    under_username = ""
    under_after_username = ""
    under_before_username = "Type your name"
    flag_enter_game = False

    while True:
        play_custom_menu_mouse_pos = pygame.mouse.get_pos()

        standard_game         = Button(image=pygame.image.load("assets/button_pictures/large_rect.png"), pos=(WIDTH / 2, 270),
                                       text_input="STANDARD", font=get_font(65), base_color="#d7fcd4",
                                       hovering_color="White")
        custom_game           = Button(image=pygame.image.load("assets/button_pictures/large_rect.png"), pos=(WIDTH / 2, 420),
                                       text_input="CUSTOM", font=get_font(65), base_color="#d7fcd4",
                                       hovering_color="White")
        play_custom_menu_back = Button(image=None, pos=(WIDTH / 2, 620),
                                       text_input="BACK", font=get_font(70), base_color="white",
                                       hovering_color="#b68f40")

        username         = get_font(60).render(list_username, True, "#b68f40")
        text_before      = get_font(20).render(under_before_username, True, "#b68f40")
        text_under       = get_font(20).render(under_username, True, "#b68f40")
        text_under_after = get_font(20).render(under_after_username, True, "#b68f40")

        SCREEN.blit(BACKGROUND, (0, 0))
        SCREEN.blit(text_before,      (WIDTH / 2 - text_before.get_width() / 2, 150))
        SCREEN.blit(username,         (WIDTH / 2 - username.get_width() / 2, 80))
        SCREEN.blit(text_under,       (WIDTH / 2 - text_under.get_width() / 2, 150))
        SCREEN.blit(text_under_after, (WIDTH / 2 - text_under_after.get_width() / 2, 150))

        for button in [standard_game, custom_game, play_custom_menu_back]:
            button.changeColor(play_custom_menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if standard_game.checkForInput(play_custom_menu_mouse_pos) and list_username != "" and flag_enter_game:
                    list_username = ""
                    play()
                elif custom_game.checkForInput(play_custom_menu_mouse_pos) and list_username != "" and flag_enter_game:
                    list_username = ""
                    custom()
                elif play_custom_menu_back.checkForInput(play_custom_menu_mouse_pos):
                    main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    list_username = list_username[:-1]
                elif event.key == pygame.K_RETURN and list_username != "":
                    flag_enter_game = True
                    under_username = ""
                    under_before_username = ""
                    under_after_username = "is current player"
                    save_username(list_username)
                else:
                    flag_enter_game = False
                    under_before_username = ""
                    under_after_username = ""
                    under_username = "Press enter"
                    list_username += event.unicode

        pygame.display.update()


# -------------------------------|DESIGN : PLAY MENU|------------------------------- #


def play():
    while True:
        play_mouse_pos = pygame.mouse.get_pos()

        easy_button   = Button(image=pygame.image.load("assets/button_pictures/medium_rect.png"), pos=(WIDTH / 2, 150),
                               text_input="EASY", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
        medium_button = Button(image=pygame.image.load("assets/button_pictures/large_rect.png"), pos=(WIDTH / 2, 300),
                               text_input="MEDIUM", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
        hard_button   = Button(image=pygame.image.load("assets/button_pictures/medium_rect.png"), pos=(WIDTH / 2, 450),
                               text_input="HARD", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
        play_back     = Button(image=None, pos=(WIDTH / 2, 620),
                               text_input="BACK", font=get_font(70), base_color="white", hovering_color="#b68f40")

        SCREEN.blit(BACKGROUND, (0, 0))

        for button in [easy_button, medium_button, hard_button, play_back]:
            button.changeColor(play_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hard_button.checkForInput(play_mouse_pos):
                    play_game("hard")
                elif medium_button.checkForInput(play_mouse_pos):
                    play_game("medium")
                elif easy_button.checkForInput(play_mouse_pos):
                    play_game("easy")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_back.checkForInput(play_mouse_pos):
                    play_custom_menu()

        pygame.display.update()


# -------------------------------|DESIGN : CUSTOM MENU|------------------------------- #


def custom():
    list_word = ""
    under_word = ""
    under_after_username = ""
    under_before_word = "Type your word"

    while True:
        custom_mouse_pos = pygame.mouse.get_pos()

        custom_button = Button(image=pygame.image.load("assets/button_pictures/large_rect.png"), pos=(WIDTH / 2, HEIGHT / 2),
                               text_input="PLAY", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
        custom_back   = Button(image=None, pos=(WIDTH / 2, 620),
                               text_input="BACK", font=get_font(70), base_color="white", hovering_color="#b68f40")

        text_word   = get_font(60).render(list_word, True, "#b68f40")
        text_before = get_font(20).render(under_before_word, True, "#b68f40")
        text_after  = get_font(20).render(under_word, True, "#b68f40")
        text_under  = get_font(20).render(under_after_username, True, "#b68f40")

        SCREEN.blit(BACKGROUND, (0, 0))
        SCREEN.blit(text_word,   (WIDTH / 2 - text_word.get_width() / 2, 100))
        SCREEN.blit(text_before, (WIDTH / 2 - text_before.get_width() / 2, 170))
        SCREEN.blit(text_under,  (WIDTH / 2 - text_under.get_width() / 2, 170))
        SCREEN.blit(text_after,  (WIDTH / 2 - text_after.get_width() / 2, 170))

        for button in [custom_button, custom_back]:
            button.changeColor(custom_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if custom_button.checkForInput(custom_mouse_pos):
                    list_word = ""
                    under_word = ""
                    under_after_username = ""
                    under_before_word = "Type your word"
                    play_game("custom")
                elif custom_back.checkForInput(custom_mouse_pos):
                    play_custom_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    list_word = list_word[:-1]
                elif event.key == pygame.K_RETURN and list_word != "":
                    under_word = ""
                    under_after_username = "word added"
                    save_word(list_word)
                else:
                    under_before_word = ""
                    under_after_username = ""
                    under_word = "Press enter"
                    list_word += event.unicode

        pygame.display.update()


# -------------------------------|DESIGN : SCORE|------------------------------- #


def score():
    sort_score()
    while True:
        score_mouse_pos = pygame.mouse.get_pos()

        score_back = Button(image=None, pos=(WIDTH / 2, 620),
                            text_input="BACK", font=get_font(70), base_color="white", hovering_color="#b68f40")

        score_text = get_font(70).render("Scores", True, "#b68f40")

        SCREEN.blit(BACKGROUND, (0, 0))
        SCREEN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 80))
        print_score()

        for button in [score_back]:
            button.changeColor(score_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if score_back.checkForInput(score_mouse_pos):
                    main_menu()

        pygame.display.update()


# -------------------------------|DESIGN : MENU|------------------------------- #


def main_menu():
    while True:
        menu_mouse_pos = pygame.mouse.get_pos()

        play_button = Button(image=pygame.image.load("assets/button_pictures/medium_rect.png"), pos=(WIDTH / 2, 250),
                             text_input="PLAY", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
        score_button = Button(image=pygame.image.load("assets/button_pictures/large_rect.png"), pos=(WIDTH / 2, 400),
                              text_input="SCORE", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/button_pictures/small_rect.png"), pos=(WIDTH / 2, 550),
                             text_input="QUIT", font=get_font(70), base_color="#d7fcd4", hovering_color="White")

        menu_text = get_font(90).render("HANGMAN GAME", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(WIDTH / 2, 100))

        SCREEN.blit(BACKGROUND, (0, 0))
        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button, score_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play_custom_menu()
                elif score_button.checkForInput(menu_mouse_pos):
                    score()
                elif quit_button.checkForInput(menu_mouse_pos):
                    clear_current_username()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    main_menu()
