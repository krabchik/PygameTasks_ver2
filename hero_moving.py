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
screen = pygame.display.set_mode((300, 300))
img = load_image('hero.png')
pygame.mouse.set_visible(False)
running = True
size = img.get_size()
pos = [150 - size[1] // 2, 150 - size[0] // 2]
while running:
    screen.fill((255, 255, 255))
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            pos[1] -= 10
        elif event.key == pygame.K_DOWN:
            pos[1] += 10
        elif event.key == pygame.K_LEFT:
            pos[0] -= 10
        elif event.key == pygame.K_RIGHT:
            pos[0] += 10
    screen.blit(img, pos)
    pygame.display.flip()
pygame.quit()
