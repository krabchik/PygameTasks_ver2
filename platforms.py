import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 255))
        self.rect = pygame.Rect(*pos, 20, 20)

    def update(self, event):
        if not event:
            self.fall()
        else:
            self.move(event)

    def fall(self):
        if not pygame.sprite.spritecollideany(self.image, platforms):
            self.rect.y += 50

    def move(self, left=False):
        if left:
            self.rect.x -= 10
        else:
            self.rect.x += 10


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((50, 10))
        self.image.fill((128, 128, 128))
        self.rect = pygame.Rect(*pos, 50, 10)


running = True
players = pygame.sprite.Group()
platforms = pygame.sprite.Group()

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            platform = Platform(event.pos, platforms)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            player = Player(event.pos, players)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                players.update(1, True)
            elif event.key == pygame.K_RIGHT:
                players.update(1)
    players.update(0)

    players.draw(screen)
    platforms.draw(screen)
    pygame.display.flip()
pygame.quit()
