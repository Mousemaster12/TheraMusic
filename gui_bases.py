import pygame
from pygame.locals import (KEYDOWN, K_BACKSPACE, K_DELETE)

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750
SCREEN_BG_COLOR = (255, 255, 255)
FONT = "Calibri"


# Buttons that could be clicked and activate functions.
class Button:
    def __init__(self, x, y, text):
        super(Button, self).__init__()
        self.x = x
        self.y = y
        self.width = 300
        self.height = 100
        self.text = text
        self.text_color = (255, 255, 255)  # White text color
        self.color = (200, 125, 200)
        self.hoverColor = (250, 175, 250)
        self.size = 60
        self.round = 10
        self.method = 0
        self.info_included = ''


# Textboxes that can be either fixed text boxes or input boxes.
class TextBox:
    def __init__(self, x, y, width, height, color, is_input_box, text=""):
        super(TextBox, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.text = text
        self.text_color = (255, 255, 255)  # White text color
        self.size = 60
        self.is_input_box = is_input_box


# Blit every Button and handle hovering.
def show_buttons(screen, buttons, mouse):
    for button in buttons:
        if (button.x <= mouse[0] <= button.x + button.width and
                button.y <= mouse[1] <= button.y + button.height):
            pygame.draw.rect(screen, button.hoverColor, [button.x, button.y, button.width, button.height],
                             border_radius=button.round)
        else:
            pygame.draw.rect(screen, button.color, [button.x, button.y, button.width, button.height],
                             border_radius=button.round)
        font = pygame.font.SysFont(FONT, button.size, bold=True)  # Use bold font
        text = font.render(correct_rtl(button.text), True, button.text_color)  # Use button's text color
        screen.blit(text, (button.x + (button.width - text.get_width()) / 2,
                           button.y + (button.height - text.get_height()) / 2))


# Enters the keyboard input into an input box.
def update_input_box(event, box):
    if event.type == KEYDOWN:
        if event.key == K_BACKSPACE or event.key == K_DELETE:
            box.text = box.text[:-1]
        elif event.key == pygame.K_KP_ENTER:
            box.text += "\n"
        else:
            box.text += event.unicode


# Splits long text to several lines by width.
def split_text_by_width(text, box, font):
    split_text = text.split(' ')
    surfaces = []
    line_beginning = len(split_text)
    for word_index in range(len(split_text) - 1, -1, -1):
        line = ' '.join(split_text[word_index:line_beginning])
        surface_width = font.size(line)[0]
        if surface_width > box.width:
            line = ' '.join(split_text[word_index + 1:line_beginning])
            surfaces.append(font.render(line, True, box.text_color))
            line_beginning = word_index + 1
    line = ' '.join(split_text[:line_beginning])
    surfaces.append(font.render(line, True, box.text_color))
    return surfaces


# Splits long text to several lines.
def auto_newline(text, box, font):
    newline_parts = text.split('\n')
    surfaces = []
    for line in newline_parts:
        surfaces += split_text_by_width(line, box, font)
    return surfaces


# Blit every text box.
def blit_text_boxes(screen, boxes):
    for box in boxes:
        font = pygame.font.SysFont(FONT, box.size, bold=True)  # Use bold font
        text_surface = auto_newline(correct_rtl(box.text), box, font)
        if box.color != SCREEN_BG_COLOR:
            pygame.draw.rect(screen, box.color, box.rect)
        for line_index in range(len(text_surface)):
            screen.blit(text_surface[line_index], (box.x, box.y + text_surface[line_index].get_height() * line_index))


# PyGame flips rtl text (such as "םולש"), this fixes it.
def correct_rtl(text):
    ltr_start = rtl_start = 0
    is_ltr = is_rtl = False
    new_text = ''
    for index in range(len(text)):
        unicode = ord(text[index])
        if 1424 <= unicode < 1920 or 4608 <= unicode < 4928 or 64336 <= unicode < 65024 or 65136 <= unicode < 65280:
            is_rtl = True
            if is_ltr:
                rtl_start = index
                is_ltr = False
                new_text += text[ltr_start:index]
        elif not (8192 <= unicode < 11952 or 32 <= unicode < 48 or 58 <= unicode <= 64 or
                  91 <= unicode <= 96 or 122 < unicode <= 126):
            is_ltr = True
            if is_rtl:
                ltr_start = index
                is_rtl = False
                new_text += text[rtl_start:index][::-1]
    if is_rtl:
        new_text += text[rtl_start:][::-1]
    elif is_ltr:
        new_text += text[ltr_start:]
    return new_text


# correct_rtl(input("Enter Text: "))
