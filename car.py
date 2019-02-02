import pygame, os

pygame.init()
screen = pygame.display.set_mode((600, 95))


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


car_sprite = pygame.sprite.Group()


class Car(pygame.sprite.Sprite):
    img = load_image('car.png')
    img_rev = pygame.transform.flip(img, True, False)
    def __init__(self):
        super().__init__(car_sprite)
        self.image = Car.img
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 0
        self.v = 10

    def update(self):
        if self.rect.x + self.rect.width == 600 or not self.rect.x:
            self.v = -self.v
            if self.image == Car.img:
                self.image = Car.img_rev
            else:
                self.image = Car.img
        self.rect.x += self.v

Car()
running = True
clock = pygame.time.Clock()
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if pygame.QUIT == event.type:
            running = False
    car_sprite.update()
    car_sprite.draw(screen)
    pygame.display.flip()
    clock.tick(20)
pygame.quit()
