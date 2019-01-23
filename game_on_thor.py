import pygame
import numpy as np


def obratno(col):
    if col == 'black':
        return 'green'
    else:
        return 'black'


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros((width * height), dtype=np.int8).reshape(height, width)
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        leftt = self.left
        topp = self.top
        size_cell = self.cell_size
        for i in range(self.height):
            for j in range(self.width):
                col = self.board[i, j]
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (leftt + size_cell * j, topp + size_cell * i, size_cell,
                                  size_cell), 1)
                if col:
                    pygame.draw.rect(screen, pygame.Color('green'),
                                     (leftt + size_cell * j + 1, topp + size_cell * i + 1,
                                      size_cell - 2,
                                      size_cell - 2))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, pos):
        leftt = self.left
        topp = self.top
        size_cell = self.cell_size
        if pos[0] >= leftt and pos[1] >= topp:
            x_num = int((pos[0] - leftt) / size_cell)
            y_num = int((pos[1] - topp) / size_cell)
            if x_num < self.width and y_num < self.height:
                return x_num, y_num

    def on_click(self, cell_coords):
        coord = cell_coords
        self.board[coord[1], coord[0]] = int(not self.board[coord[1], coord[0]])

    def update(self):
        population = self.board
        neighbors = sum([
            np.roll(np.roll(population, -1, 1), 1, 0),
            np.roll(np.roll(population, 1, 1), -1, 0),
            np.roll(np.roll(population, 1, 1), 1, 0),
            np.roll(np.roll(population, -1, 1), -1, 0),
            np.roll(population, 1, 1),
            np.roll(population, -1, 1),
            np.roll(population, 1, 0),
            np.roll(population, -1, 0)
        ])
        self.board = (neighbors == 3) | (population & (neighbors == 2))


pygame.init()
screen = pygame.display.set_mode((400, 400))
board = Board(20, 20)
board.set_view(0, 0, 20)
running = True
editing = True
fps = 3
clock = pygame.time.Clock()
while running:
    if editing:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.get_click(event.pos)
            elif event.button == 5 and fps > 2:
                fps -= 2
            elif event.button == 4:
                fps += 2
            elif event.button == 3:
                editing = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5 and fps > 2:
                    fps -= 2
                elif event.button == 4:
                    fps += 2
                elif event.button == 3:
                    editing = True
        board.update()
        clock.tick(fps)
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
pygame.quit()