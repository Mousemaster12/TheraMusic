import pygame
from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, KEYDOWN, KEYUP, QUIT, K_BACKSPACE, K_DELETE)

BUTTONS_IN_LINE = 3
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
OPTIONS = ["Relaxing", "Cheering", "Distressing", "Hopeful", "Inspiring", "Exciting", "Touching"]
SCREEN_BG_COLOR = (255, 255, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surface = pygame.image.load("image.png").convert()
        self.surface.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surface.get_rect()


class Button:
    def __init__(self, x, y, text):
        super(Button, self).__init__()
        self.x = x
        self.y = y
        self.width = 300
        self.height = 100
        self.text = text
        self.text_color = (0, 0, 0)
        self.color = (100, 200, 225)
        self.hoverColor = (150, 250, 255)
        self.size = 60
        self.method = click_on_buttons([self], (0, 0))
        self.link_for_send_buttons = ''


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
        self.text_color = (0, 0, 0)
        self.size = 60
        self.is_input_box = is_input_box


def create_buttons():
    buttons = []
    for button_num in range(len(OPTIONS)):
        button = Button(button_num % BUTTONS_IN_LINE * 225 + 60, button_num // BUTTONS_IN_LINE * 100 + 50,
                        OPTIONS[button_num])
        buttons.append(button)
    return buttons


def show_buttons(screen, buttons, mouse, font):
    for button in buttons:
        if (button.x <= mouse[0] <= button.x + button.width and
                button.y <= mouse[1] <= button.y + button.height):
            pygame.draw.rect(screen, button.hoverColor, [button.x, button.y, button.width, button.height])
        else:
            pygame.draw.rect(screen, button.color, [button.x, button.y, button.width, button.height])
        text = font.render(correct_rtl(button.text), True, button.text_color)
        screen.blit(text, (button.x + (button.width - text.get_width()) / 2,
                           button.y + (button.height - text.get_height()) / 2))


def click_on_buttons(buttons, mouse):
    text = ""
    for button in buttons:
        if (button.x <= mouse[0] <= button.x + button.width and
                button.y <= mouse[1] <= button.y + button.height):
            text += button.text + " "
    return text


def update_input_box(event, box):
    if event.type == KEYDOWN:
        if event.key == K_BACKSPACE or event.key == K_DELETE:
            box.text = box.text[:-1]
        elif event.key == pygame.K_KP_ENTER:
            box.text += "\n"
        else:
            box.text += event.unicode


def split_long_text_lines(text, box, font):
    surface_width, _ = font.size(text)

    if surface_width > box.width:
        text_split = text.split(' ')
        new_text = ' '.join(text_split[:-1])
        text_3 = split_long_text_lines(new_text, box, font)
        return text_3
    return text


def make_text_surfaces(text, font):
    text_split = text.split('\n')
    your_new_surfaces = []
    for sentence in text_split:
        new_surface_that_was_rendered = font.render(sentence, True, 'white')
        your_new_surfaces.append(new_surface_that_was_rendered)
    return your_new_surfaces


def auto_newline(text, box, font):
    lines_that_fit = []
    while text:
        if "\n" in text:
            perfect_line_after_split = make_text_surfaces(text, font)
        else:
            perfect_line_after_split = split_long_text_lines(text, box, font)
        lines_that_fit.append(perfect_line_after_split)
        text = text.replace(perfect_line_after_split, '')

    text_surfaces_from_split = []
    for line in lines_that_fit:
        text_surfaces_from_split.append(font.render(line, True, box.text_color))
    return text_surfaces_from_split


def blit_input_box(screen, box, font):
    text_surface = auto_newline(correct_rtl(box.text), box, font)
    # box.rect.w = max(box.width, text_surface.get_width() + 10)
    if box.color != SCREEN_BG_COLOR:
        pygame.draw.rect(screen, box.color, box.rect)
    text_surface = text_surface[::-1]
    for line_index in range(len(text_surface)):
        # screen.blit(text_surface[line_index], (box.x, (box.y + ((box.height - get_list_heights(text_surface)) +
        #                                                (text_surface[line_index].get_height() * line_index) / 2)
        #                                        // len(text_surface))))
        screen.blit(text_surface[line_index], (box.x, box.y + text_surface[line_index].get_height() * (line_index)))


def get_list_heights(surfaces):
    height = 0
    for surface in surfaces:
        height += surface.get_height()
    return height


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
                new_text += text[index - 1:rtl_start - 1:-1]
    if is_rtl:
        new_text += text[rtl_start:][::-1]
    elif is_ltr:
        new_text += text[ltr_start:]
    return new_text


def move_player(event, move_x, move_y):
    if event.type == KEYDOWN:
        if event.key == K_LEFT:
            move_x = -0.3
        elif event.key == K_RIGHT:
            move_x = +0.3
        elif event.key == K_UP:
            move_y = -0.3
        elif event.key == K_DOWN:
            move_y = +0.3
    elif event.type == KEYUP:
        if event.key == K_LEFT:
            move_x = 0
        elif event.key == K_RIGHT:
            move_x = 0
        elif event.key == K_UP:
            move_y = 0
        elif event.key == K_DOWN:
            move_y = 0
    return move_x, move_y


pygame.init()
pygame.mixer.init()
pygame.font.init()


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Make a song')
    font = pygame.font.SysFont('Calibri', 45)
    buttons = create_buttons()
    player = Player()
    input_box = TextBox(60, 350, 300, 75, (100, 100, 255), True)
    input_box.is_input_box = True
    text = TextBox(60, 425, 300, 75, SCREEN_BG_COLOR, False)
    x, y = 0, 0
    move_x, move_y = 0, 0
    prompt = ""
    running = True
    boxes = [input_box, text]
    while running:
        screen.fill((255, 255, 255))
        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        player.update(keys)
        show_buttons(screen, buttons, mouse, font)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                prompt += click_on_buttons(buttons, mouse)
                x += 50
            for box in boxes:
                if box.is_input_box:
                    update_input_box(event, input_box)
            move_x, move_y = move_player(event, move_x, move_y)
        x += move_x
        y += move_y
        text.text = prompt + input_box.text
        screen.blit(player.surface, (x, y))
        for box in boxes:
            blit_input_box(screen, box, font)
        pygame.display.flip()


if __name__ == '__main__':
    main()
