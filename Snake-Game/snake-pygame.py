import random
import pygame
import tkinter as tk
from tkinter import messagebox

score_all = []
flag = True


class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, color=(255, 0, 0)):
        self.pos = start
        self.dir_n_x = 1
        self.dir_n_y = 0
        self.color = color

    def move(self, dir_n_x, dir_n_y):
        self.dir_n_x = dir_n_x
        self.dir_n_y = dir_n_y
        self.pos = (self.pos[0] + self.dir_n_x, self.pos[1] + self.dir_n_y)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle = (i * dis + centre - radius, j * dis + 8)
            circle_middle_2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle_2, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dir_n_x = 0
        self.dir_n_y = 1

    def move(self):
        global flag
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    flag = False
                keys = pygame.key.get_pressed()

                for _ in keys:
                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        self.dir_n_x = -1
                        self.dir_n_y = 0
                        self.turns[self.head.pos[:]] = [self.dir_n_x, self.dir_n_y]

                    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        self.dir_n_x = 1
                        self.dir_n_y = 0
                        self.turns[self.head.pos[:]] = [self.dir_n_x, self.dir_n_y]

                    elif keys[pygame.K_UP] or keys[pygame.K_w]:
                        self.dir_n_x = 0
                        self.dir_n_y = -1
                        self.turns[self.head.pos[:]] = [self.dir_n_x, self.dir_n_y]

                    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                        self.dir_n_x = 0
                        self.dir_n_y = 1
                        self.turns[self.head.pos[:]] = [self.dir_n_x, self.dir_n_y]
        except pygame.error:
            pass

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dir_n_x == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dir_n_x == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dir_n_y == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dir_n_y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dir_n_x, c.dir_n_y)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dir_n_x = 0
        self.dir_n_y = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dir_n_x, tail.dir_n_y

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dir_n_x = dx
        self.body[-1].dir_n_y = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(w, surface):
    size_btwn = w // rows

    x = 0
    y = 0
    for _ in range(rows):
        x = x + size_btwn
        y = y + size_btwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redraw_window(surface):
    global rows, width, s, snack
    try:
        surface.fill((0, 0, 0))
        s.draw(surface)
        snack.draw(surface)
        # draw_grid(width, surface)
        pygame.display.update()
    except pygame.error:
        pass


def random_snack(item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    root.destroy()


def main():
    global snack
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_snack(s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                score_all.append(len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10, 10))
                break

        redraw_window(win)


width = 500
rows = 20
win = pygame.display.set_mode((width, width))
s = Snake((255, 0, 0), (10, 10))
snack = Cube(random_snack(s), color=(0, 255, 0))
pygame.display.set_caption("Snake Game")
main()
print(score_all)
