import pygame
from pygame.locals import (KEYDOWN, QUIT, K_ESCAPE)
import webbrowser

import gui_bases
import sunoapi

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750
SCREEN_BG_COLOR = (255, 255, 255)
BG_IMAGE = pygame.transform.scale(pygame.image.load("background_image.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = "Calibri"


# Init pygame.
def initialize_program():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Theramusic')
    return screen


# Creates the opening screen.
def open_screen():
    greeting = gui_bases.TextBox(650, 150, 300, 150, SCREEN_BG_COLOR, False, "שלום!")
    greeting.size = 90
    greeting2 = gui_bases.TextBox(500, 350, 700, 100,
                                  SCREEN_BG_COLOR, False, "איך אתם מרגישים היום?")
    continue_button = gui_bases.Button(600, 500, "להתחיל")
    continue_button.method = input_screen
    text_boxes = [greeting, greeting2]
    buttons = [continue_button]
    return text_boxes, buttons


# Creates the screen where with the user input.
def input_screen(sender):
    if sender.text == "להתחיל":
        pass
    question = gui_bases.TextBox(300, 50, 1100, 100, SCREEN_BG_COLOR, False,
                                 "ספרו לנו איך מצבכם היום בעקבות המלחמה:")
    input_box = gui_bases.TextBox(200, 150, 1100, 400, (255, 225, 200), True)
    send_button = gui_bases.Button(600, 600, "סיימתי")
    send_button.method = send_to_api
    text_boxes = [question, input_box]
    buttons = [send_button]
    return text_boxes, buttons


# Creates the screen with the result.
def result_screen(link1, link2):
    done_message = gui_bases.TextBox(500, 100, 600, 100, SCREEN_BG_COLOR, False,
                                     "האזינו לשירים שלכם: ")
    link_button_1 = gui_bases.Button(800, 300, "קישור ל־1")
    link_button_2 = gui_bases.Button(400, 300, "לקישור ל־2")
    link_to_suno = gui_bases.Button(550, 500, "קישור לאתר Suno")
    link_to_suno.width = 400
    link_button_1.info_included = link1
    link_button_2.info_included = link2
    link_to_suno.info_included = "https://suno.com/"
    link_button_1.method = link_button_2.method = link_to_suno.method = open_song
    text_boxes = [done_message]
    buttons = [link_button_1, link_button_2, link_to_suno]
    return text_boxes, buttons


# The running loop that operates the gui_bases.
def run(screen, text_boxes, buttons):
    running = True
    while running:
        screen.blit(BG_IMAGE, (0, 0))
        mouse = pygame.mouse.get_pos()
        gui_bases.blit_text_boxes(screen, text_boxes)
        gui_bases.show_buttons(screen, buttons, mouse)
        for event in pygame.event.get():
            running, text_boxes, buttons = handle_events(event, buttons, text_boxes, mouse)
        pygame.display.flip()
    return running


# Handles all of pygame events.
def handle_events(event, buttons, text_boxes, mouse):
    if event.type == QUIT:
        return False, text_boxes, buttons
    elif event.type == KEYDOWN:
        for box in text_boxes:
            if box.is_input_box:
                gui_bases.update_input_box(event, box)
        if event.key == K_ESCAPE:
            return False, text_boxes, buttons
    elif event.type == pygame.MOUSEBUTTONDOWN:
        for button in buttons:
            if not button.info_included:
                button.info_included = get_prompt(text_boxes)
            if button.x <= mouse[0] <= button.x + button.width and button.y <= mouse[1] <= button.y + button.height:
                output = button.method(button)
                if output is not None:
                    text_boxes, buttons = output
    return True, text_boxes, buttons


def get_prompt(text_boxes):
    for box in text_boxes:
        if box.is_input_box:
            return box.text
    return ''


def send_to_api(button):
    link1, link2 = sunoapi.main(button.info_included)
    return result_screen(link1, link2)


def open_song(sender):
    webbrowser.open(sender.info_included)


def main():
    screen = initialize_program()
    text_boxes, buttons = open_screen()
    run(screen, text_boxes, buttons)


if __name__ == "__main__":
    main()
