import json
import pygame

pygame.init()

pygame.display.set_caption("HANGMAN GAME")
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


# -------------------------------|COMMON FUNCTION|------------------------------- #


def get_font(size):
    return pygame.font.Font("assets/font/font.ttf", size)


def save_in_json(data):
    with open("data_files/score.json", "w") as file:
        json.dump(data, file, indent=4)
