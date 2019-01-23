import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


pygame.init()
screen = pygame.display.set_mode((500, 500))
img = load_image('arrow.png')
pygame.mouse.set_visible(False)
running = True
while running:
    screen.fill((0, 0, 0))
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    elif pygame.mouse.get_focused():
        screen.blit(img, pygame.mouse.get_pos())
    pygame.display.flip()
pygame.quit()
