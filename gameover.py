import pygame, os


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
screen = pygame.display.set_mode((600, 300))
text = load_image('gameover.png')
x, y = -600, 0
running = True
clock = pygame.time.Clock()
while running:
    screen.fill((0, 0, 255))
    for event in pygame.event.get():
        if pygame.QUIT == event.type:
            running = False
    screen.blit(text, (x, y))
    if x:
        x += 10
    pygame.display.flip()
    clock.tick(20)
pygame.quit()
