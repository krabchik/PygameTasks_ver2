import pygame, sys, os, math

# ----------------------------------- You need to enter level name --------------------------------
# Levels names: lvl.txt, lvl1.txt, lvl2.txt
level_name = sys.argv[-1]
pygame.init()
screen = pygame.display.set_mode((500, 500))


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


FPS = 20
tile_images = {
    'wall': pygame.transform.scale(load_image('box.png'), (50, 50)),
    'empty': pygame.transform.scale(load_image('grass1.png'), (50, 50)),
    'water': pygame.transform.scale(load_image('water.png'), (50, 50)),
    'water_tile': pygame.transform.scale(load_image('water.png'), (10, 10)),
    'enemy50': pygame.transform.scale(load_image('enemy50.png'), (50, 50)),
    'bullet20': pygame.transform.scale(load_image('bullet20.png'), (50, 50))}
player_image = load_image('mario.png')
tile_width = tile_height = 50
clock = pygame.time.Clock()

speeds = {
    20: 10,
    30: 5
}

all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
side_water_group = pygame.sprite.Group()
enemy_proj = pygame.sprite.Group()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map)), \
           (max_width * 50, len(level_map) * 50)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'w':
                Tile('water', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '5':
                Enemy(x, y, 50)
    return new_player, x, y


def load_side_water():
    for y in range(-10, int(screen_size[1]) + 10, 10):
        SideWater(-10, y)
        SideWater(screen_size[0], y)
    for x in range(-10, int(screen_size[0]) + 10, 10):
        SideWater(x, -10)
        SideWater(x, screen_size[1])


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(size_of_screen):
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (500, 500))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, water=False):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, x, y):
        self.rect = self.image.get_rect().move(self.rect.x + x, self.rect.y + y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

        self.hp = 100
        self.mana = 120

    def update(self, x, y):
        self.rect = self.image.get_rect().move(self.rect.x + x, self.rect.y + y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, hp):
        Tile('empty', x, y)
        super().__init__(enemy_group, all_sprites)
        self.image = tile_images['enemy' + str(hp)]
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height)

        self.hp = hp
        if hp == 50:
            self.att = 20
        else:
            self.att = 30

    def update(self, x, y):
        self.rect = self.image.get_rect().move(self.rect.x + x, self.rect.y + y)

        # ПОЛОСКА С ХП

    def fire(self):
        if abs(new_player.rect.center[0] - self.rect.center[0]) < 500 and \
                abs(new_player.rect.center[1] - self.rect.center[1]) < 500:
            EnemyBullet((self.rect.x, self.rect.y), (new_player.rect.x, new_player.rect.y), 20)


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, hero_pos, dmg):
        super().__init__(enemy_proj, all_sprites)
        self.image = tile_images['bullet' + str(dmg)]
        self.rect = self.image.get_rect().move(start_pos[0], start_pos[1])
        self.dmg = dmg
        self.st_x, self.st_y = start_pos
        self.hero_x, self.hero_y = hero_pos
        self.v_x = (hero_pos[0] - start_pos[0]) * speeds[dmg] \
                   // math.sqrt((start_pos[1] - hero_pos[1])**2 + (start_pos[0] - hero_pos[0])**2)
        self.v_y = (hero_pos[1] - start_pos[1]) * speeds[dmg] \
                   // math.sqrt((start_pos[1] - hero_pos[1])**2 + (start_pos[0] - hero_pos[0])**2)

    def update(self, x, y):
        if abs(self.rect.x - self.st_x) > 500 or abs(self.rect.y - self.st_y) > 500:
            self.kill()

        self.rect = self.rect.move(self.v_x, self.v_y)

        self.rect = self.image.get_rect().move(self.rect.x + x, self.rect.y + y)
        print(self.rect.x, self.rect.y)


class SideWater(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(side_water_group, all_sprites)
        self.image = tile_images['water_tile']
        self.rect = self.image.get_rect().move(x, y)

    def update(self, x, y):
        self.rect = self.image.get_rect().move(self.rect.x + x, self.rect.y + y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self):
        return self.dx, self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w - 235)
        self.dy = -(target.rect.y + target.rect.h - 245)


running = True
level, screen_size = load_level(level_name)

load_side_water()
new_player, x, y = generate_level(level)
start_screen(screen_size)
screen.fill((0, 0, 0))
camera = Camera()

enemy_shoot = 0

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_group.update(0, -10)
    if keys[pygame.K_DOWN]:
        player_group.update(0, 10)
    if keys[pygame.K_LEFT]:
        player_group.update(-10, 0)
    if keys[pygame.K_RIGHT]:
        player_group.update(10, 0)

    if enemy_shoot == 20:
        for i in enemy_group:
            i.fire()
        enemy_shoot = 0

    camera.update(new_player)
    all_sprites.update(camera.dx, camera.dy)
    tiles_group.draw(screen)
    side_water_group.draw(screen)
    enemy_group.draw(screen)
    enemy_proj.draw(screen)
    player_group.draw(screen)

    enemy_shoot += 1

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
