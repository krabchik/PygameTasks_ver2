import pygame, os, random


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


class Bomb(pygame.sprite.Sprite):
    img = load_image("bomb.png", -1)
    img_boom = load_image("boom.png", -1)
    razn = (img.get_rect()[0] - img_boom.get_rect()[0], img.get_rect()[1] - img_boom.get_rect()[1])

    def __init__(self, group):
        super().__init__(group)
        self.image = Bomb.img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(500)
        self.rect.y = random.randrange(500)

    def update(self, event):
        rectangle = self.rect
        if rectangle.collidepoint(event.pos) and self.image == self.img:
            size1 = self.image.get_rect()
            self.image = self.img_boom
            x, y = rectangle[0], rectangle[1]
            size2 = self.image.get_rect()
            self.rect = size2
            self.rect.x = x - 0.5 * (size2[2] - size1[2])
            self.rect.y = y - 0.5 * (size2[3] - size1[3])


running = True
all_sprites = pygame.sprite.Group()
for _ in range(10):
    while 1:
        bomb = Bomb(all_sprites)
        rect = bomb.rect
        x = rect.x
        y = rect.y
        in_1 = 0 <= x <= 500 and 0 <= y <= 500
        in_2 = 0 <= x + rect[2] <= 500 and 0 <= y + rect[3] <= 500
        if pygame.sprite.spritecollideany(bomb, all_sprites) == bomb and in_1 and in_2:
            break
        all_sprites.remove(bomb)

all_sprites.draw(screen)

while running:
    screen.fill((0, 0, 0))
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        all_sprites.update(event)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
