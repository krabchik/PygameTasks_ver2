import pygame, sys, os, math

# ----------------------------------- You need to enter level name --------------------------------
# Levels names: lvl.txt, lvl1.txt, lvl2.txt
basic_level_name = 'lvl.txt'
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


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    ready_map = list(map(lambda x: x.ljust(max_width, '.'), level_map)), \
                (max_width * 50, len(level_map) * 50)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
    os.remove(path)
    with open('data/lvl.txt', 'w', encoding='utf-8') as f:
        file = f
        for i in ready_map[0]:
            file.write(''.join(list(map(str, i))) + '\n')
    return ready_map


new_player = None
tile_images = {
    'wall': pygame.transform.scale(load_image('box.png'), (50, 50)),
    'empty': pygame.transform.scale(load_image('grass1.png'), (50, 50)),
    'water': pygame.transform.scale(load_image('water.png'), (50, 50)),
    'water_tile': pygame.transform.scale(load_image('water.png'), (10, 10)),
    'enemy50': pygame.transform.scale(load_image('enemy50.png'), (50, 50)),
    'bullet10': pygame.transform.scale(load_image('bullet10.png'), (50, 50)),
    'hero_bullet': pygame.transform.scale(load_image('hero_bullet.png'), (50, 50))}
player_images = {
    'down':   pygame.transform.scale(load_image('mage4.png', colorkey=(255, 255, 255)), (50, 50)),
    'up':     pygame.transform.scale(load_image('mage3.png', colorkey=(255, 255, 255)), (50, 50)),
    'left':   pygame.transform.scale(load_image('mage2.png', colorkey=(255, 255, 255)), (50, 50)),
    'right':  pygame.transform.scale(load_image('mage1.png', colorkey=(255, 255, 255)), (50, 50)),
    'stepdown':   pygame.transform.scale(load_image('stepmage4.png', colorkey=(255, 255, 255)), (50, 50)),
    'stepup':     pygame.transform.scale(load_image('stepmage3.png', colorkey=(255, 255, 255)), (50, 50)),
    'stepleft':   pygame.transform.scale(load_image('stepmage2.png', colorkey=(255, 255, 255)), (50, 50)),
    'stepright':  pygame.transform.scale(load_image('stepmage1.png', colorkey=(255, 255, 255)), (50, 50))
}
tile_width = tile_height = 50
clock = pygame.time.Clock()
hero_damage = 10

speeds = {
    10: 15,
    30: 10
}

all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
side_water_group = pygame.sprite.Group()
enemy_proj = pygame.sprite.Group()
hero_proj = pygame.sprite.Group()
hp_bars = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, x, y):
        self.rect = self.image.get_rect().move(self.rect.x + x, self.rect.y + y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, hp_bar):
        super().__init__(player_group, all_sprites)
        self.image = player_images['down']
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

        self.image_name = 'down'
        self.die = False
        self.hp_bar = hp_bar
        self.hp = 100
        self.mana = 120

    def update(self, x, y):
        curr_rect = self.rect
        try:
            self.rect = self.image.get_rect().move(self.rect.x + x, self.rect.y + y)
            if pygame.sprite.groupcollide(player_group, side_water_group, False, False):
                raise ZeroDivisionError
        except ZeroDivisionError:
            self.rect = curr_rect
        if step > 10:
            self.image = player_images['step' + self.image_name]
            return
        self.image = player_images[self.image_name]

    def fire(self, cursor_pos):
        HeroBullet((self.rect.center[0] - 50, self.rect[1]), cursor_pos, 20)

    def hit(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()
            self.die = True

        self.hp_bar.low(dmg)

    def turn_to(self, direct):
        self.image_name = direct


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, hp, hp_bar):
        Tile('empty', x, y)
        super().__init__(enemy_group, all_sprites)
        self.image = tile_images['enemy' + str(hp)]
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height)

        self.hp_bar = hp_bar
        self.hp = hp
        if hp == 50:
            self.att = 10
        else:
            self.att = 20

    def update(self, x, y):
        self.rect = self.image.get_rect().move(self.rect.x + x, self.rect.y + y)

    def fire(self):
        a = abs(new_player.rect.center[0] - self.rect.center[0])
        b = abs(new_player.rect.center[1] - self.rect.center[1])
        if a < 400 and b < 400:
            EnemyBullet((self.rect.x, self.rect.y),
                        (new_player.rect.x, new_player.rect.y + 0.5 * new_player.rect.width), self.att)

    def hit(self, dmg):
        self.hp -= dmg
        if self.hp == 0:
            self.kill()

        self.hp_bar.low(dmg)


class HP_bar(pygame.sprite.Sprite):
    def __init__(self, hero,
                 pos=(200, 250), hp=100):
        super().__init__(all_sprites, hp_bars)
        self.image = pygame.Surface((50, 10))
        self.hero = hero
        if hero:
            self.col = (0, 255, 0)
        else:
            a, b = pos
            a -= 54
            pos = (a, b)
            self.col = (255, 0, 0)

        self.hp = hp
        self.rect = pygame.Rect(pos, (50, 10))
        self.image.fill(self.col)
        self.width = 50

    def low(self, dmg):
        self.width -= 50 * dmg // self.hp
        self.image = pygame.Surface((self.width, 10))
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 50 - dmg, 10)
        self.image.fill(self.col)

    def update(self, x, y):
        if not self.hero:
            self.rect = self.image.get_rect().move(self.rect.x + x, self.rect.y + y)


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
                new_player = Player(x, y, HP_bar(True))
            elif level[y][x] == '5':
                Enemy(x, y, 50, HP_bar(False, pos=((x + 1) * tile_width, (y + 1) * tile_height), hp=50))
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


def start_screen():
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


def end_screen():
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


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, hero_pos, dmg):
        super().__init__(enemy_proj, all_sprites)
        self.image = tile_images['bullet' + str(dmg)]
        self.rect = self.image.get_rect().move(start_pos[0], start_pos[1])
        self.dmg = dmg
        self.st_x, self.st_y = start_pos
        self.hero_x, self.hero_y = hero_pos

        self.v_x = (hero_pos[0] - start_pos[0]) * speeds[dmg] \
                   // math.sqrt((start_pos[1] - hero_pos[1]) ** 2 + (start_pos[0] - hero_pos[0]) ** 2)
        self.v_y = (hero_pos[1] - start_pos[1]) * speeds[dmg] \
                   // math.sqrt((start_pos[1] - hero_pos[1]) ** 2 + (start_pos[0] - hero_pos[0]) ** 2)

    def update(self, x, y):

        # Если попал в игрока
        if pygame.sprite.collide_rect(self, new_player):
            self.kill()
            new_player.hit(self.dmg)

        # Если улетел далеко от владельца
        if abs(self.rect.center[0] - self.st_x) > 300 or abs(self.rect.center[1] - self.st_y) > 300:
            self.kill()

        self.rect = self.image.get_rect().move(self.rect.x + x + self.v_x, self.rect.y + y + self.v_y)


class HeroBullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, cursor_pos, dmg):
        super().__init__(hero_proj, all_sprites)
        self.image = tile_images['hero_bullet']
        self.rect = self.image.get_rect().move(start_pos[0], start_pos[1])
        self.dmg = hero_damage
        self.st_x, self.st_y = start_pos
        self.hero_x, self.hero_y = cursor_pos
        try:
            self.v_x = (cursor_pos[0] - start_pos[0]) * 15 \
                       // math.sqrt((start_pos[1] - cursor_pos[1]) ** 2 + (start_pos[0] - cursor_pos[0]) ** 2)
            self.v_y = (cursor_pos[1] - start_pos[1]) * 15 \
                       // math.sqrt((start_pos[1] - cursor_pos[1]) ** 2 + (start_pos[0] - cursor_pos[0]) ** 2)
        except ZeroDivisionError:
            self.kill()

    def update(self, x, y):

        # Если попал во врага
        for i in enemy_group:
            if pygame.sprite.collide_rect(self, i):
                self.kill()
                i.hit(self.dmg)

        # Если улетел далеко от владельца
        if abs(self.rect.x - self.st_x) > 300 or abs(self.rect.y - self.st_y) > 300:
            self.kill()

        self.rect = self.image.get_rect().move(self.rect.x + x + self.v_x, self.rect.y + y + self.v_y)


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
        self.dx = -(target.rect.x + target.rect.w - 250)
        self.dy = -(target.rect.y + target.rect.h - 245)


# Possible statuses:
# 0 - start screen, 1 - menu, 2 - game preparings, 3 - game, 4 - end screen
status = 0
running = True
FPS = 10

while running:
    if not status:
        FPS = 10
        start_screen()
        status = 2
    elif status == 2:
        level, screen_size = load_level(basic_level_name)
        new_player, x, y = generate_level(level)
        load_side_water()
        screen.fill((0, 0, 0))
        camera = Camera()
        ch_x, ch_y = 0, 0

        enemy_shoot = 0
        hero_shoot = 10
        step = 0

        status = 3

    elif status == 3:
        if new_player.die:
            status = 4
            continue
        FPS = 20
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_group.update(0, -10)
            new_player.turn_to('up')
            ch_y -= 10
            step += 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_group.update(0, 10)
            new_player.turn_to('down')
            ch_y += 10
            step += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_group.update(-10, 0)
            new_player.turn_to('left')
            ch_x -= 10
            step += 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_group.update(10, 0)
            new_player.turn_to('right')
            ch_x += 10
            step += 1
        if pygame.mouse.get_pressed()[0]:
            if hero_shoot == 15:
                new_player.fire(pygame.mouse.get_pos())
                hero_shoot = 0

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
        hero_proj.draw(screen)
        hp_bars.draw(screen)

        if hero_shoot < 15:
            hero_shoot += 1
        enemy_shoot += 1

        pygame.display.flip()
        clock.tick(FPS)
        step %= 20
    elif status == 4:
        pass
        #  game_over()
terminate()
