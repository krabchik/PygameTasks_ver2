import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 255))
        self.rect = pygame.Rect(0, 0, 20, 20)
        self.rect.center = pos

    def update(self, event, left=False):
        if not event:
            self.fall()
        else:
            self.move(left)

    def fall(self):
        if not pygame.sprite.spritecollideany(self, platforms):
            self.rect.y += 2

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
        self.rect = pygame.Rect(0, 0, 50, 10)
        self.rect.center = pos


running = True
players = pygame.sprite.Group()
platforms = pygame.sprite.Group()
fps = 25
clock = pygame.time.Clock()
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            platform = Platform(event.pos, platforms)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            players.remove(players)
            player = Player(event.pos, players)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                players.update(1, 3)
            elif event.mod == 64 and event.key == pygame.K_UP:
                players.update(1, 4)
            elif event.mod == 64 and event.key == pygame.K_DOWN:
                players.update(1, 2)
            elif event.key == pygame.K_RIGHT:
                players.update(1, 1)
    players.update(0)
    players.draw(screen)
    platforms.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
