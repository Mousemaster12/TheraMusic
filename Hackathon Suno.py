import pygame
import bases

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750
SCREEN_BG_COLOR = (255, 255, 255)
FONT = "Calibri"


def initialize_program():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Hello!')
    return screen


def open_screen(screen):
    mouse = pygame.mouse.get_pos()
    screen.fill(SCREEN_BG_COLOR)
    greeting = bases.TextBox(650, 150, 300, 150, SCREEN_BG_COLOR, False, "שלום!")
    greeting.size = 90
    greeting2 = bases.TextBox(500, 350, 700, 100,
                              SCREEN_BG_COLOR, False, "איך אתם מרגישים היום?")
    continue_button = bases.Button(600, 500, "להתחיל")
    continue_button.method = continue_button_method
    running = True
    while running:
        blit_input_boxes(screen, [greeting, greeting2])
        bases.show_buttons(screen, [continue_button], mouse, pygame.font.SysFont(FONT, continue_button.size))
        for event in pygame.event.get():
            return handle_events(screen, event, [continue_button], [greeting, greeting2], mouse)
        pygame.display.flip()
    return True


def blit_input_boxes(screen, boxes):
    for box in boxes:
        bases.blit_input_box(screen, box, pygame.font.SysFont(FONT, box.size))


def input_screen(screen):
    screen.fill(SCREEN_BG_COLOR)
    question = bases.TextBox(300, 50, 1100, 100, SCREEN_BG_COLOR, False,
                             "ספרו לנו איך מצבכם היום בעקבות המלחמה:")
    input_box = bases.TextBox(200, 150, 1100, 400, (200, 200, 200), True)
    send_button = bases.Button(600, 600, "סיימתי")
    send_button.method = send_to_api
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        blit_input_boxes(screen, [question, input_box])
        bases.show_buttons(screen, [send_button], mouse, pygame.font.SysFont(FONT, send_button.size))
        for event in pygame.event.get():
            running = handle_events(screen, event, [send_button], [question, input_box], mouse)
            # return running
        pygame.display.flip()
    return True


def handle_events(screen, event, buttons, text_boxes, mouse):
    if event.type == pygame.QUIT:
        return False
    elif event.type == pygame.KEYDOWN:
        for box in text_boxes:
            if box.is_input_box:
                bases.update_input_box(event, box)
        if event.key == pygame.K_ESCAPE:
            return False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        for button in buttons:
            if (button.x <= mouse[0] <= button.x + button.width and
                    button.y <= mouse[1] <= button.y + button.height):
                prompt = return_prompt(text_boxes)
                return button.method(screen, prompt, button)
    return True


def return_prompt(text_boxes):
    for box in text_boxes:
        if box.is_input_box:
            return box.text
    return ''


def continue_button_method(screen, prompt, sender):
    return input_screen(screen)


def send_to_api(screen, prompt, sender):
    link_button_1 = bases.Button(800, 300, "להפעיל את א")
    link_button_2 = bases.Button(400, 300, "להפעיל את ב")
    link_to_suno = bases.Button(600, 500, "קישור ל־Suno")
    link_button_1.link_for_send_buttons = "1"  # Fill with link #1 (str).
    link_button_1.link_for_send_buttons = "2"  # Fill with link #2 (str).
    link_button_1.method = link_button_2.method = link_to_suno.method = play_stop_song
    done_message = bases.TextBox(500, 100, 600, 100, SCREEN_BG_COLOR, False,
                                 "האזינו לשירים שלכם: ")
    buttons = [link_button_1, link_button_2, link_to_suno]
    screen.fill(SCREEN_BG_COLOR)
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        blit_input_boxes(screen, [done_message])
        bases.show_buttons(screen, buttons, mouse,
                           pygame.font.SysFont(FONT, link_button_1.size))
        for event in pygame.event.get():
            running = handle_events(screen, event, buttons,
                                    [done_message], mouse)
        pygame.display.flip()


def play_stop_song(screen, links, sender):
    return True


def main():
    screen = initialize_program()
    running = True
    # if running:
    #     running = input_screen(screen)
    while running:
        running = open_screen(screen)
    pygame.quit()


main()
