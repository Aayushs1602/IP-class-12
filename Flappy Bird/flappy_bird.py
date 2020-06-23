import pygame
import os
import time
import random

pygame.font.init()
SCORE_LI = []
FPS = 30
# -------------------------------------------- vars for scaling ------------------------------------------------------

# factor for scaling of images
SCALE_FACTOR = 1.5

# window width abd height
WIN_WIDTH = 350
WIN_HEIGHT = 650

# Dist btw Top pipe and bottom pipe
GAP_PIPE = 180

GAME_OVER_FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont("comicsans", 40)
SCORE_FONT = pygame.font.SysFont('comicsans', 30)


# --------------------------------------------------------------------------------------------------------------------

# Loading Assets
BIRD_IMG_S = []
for z in range(1, 4):
    n = "bird" + str(z) + '.png'
    i = pygame.image.load(os.path.join('imgs', n))
    BIRD_IMG_S.append(pygame.transform.scale(i, (int(i.get_width() * SCALE_FACTOR),
                                                 int(i.get_height() * SCALE_FACTOR))))

i = pygame.image.load(r'imgs\pipe.png')
PIPE_IMG = pygame.transform.scale(i, (int(i.get_width() * SCALE_FACTOR), int(i.get_height() * SCALE_FACTOR)))

i = pygame.image.load(r'imgs\base.png')
BASE_IMG = pygame.transform.scale(i, (int(i.get_width() * SCALE_FACTOR), int(i.get_height() * SCALE_FACTOR)))
BG_IMG = pygame.transform.scale(pygame.image.load(r'imgs\bg.png'), (WIN_WIDTH, WIN_HEIGHT))


# Bird class for rendering and actions related to players character
class Bird:
    IMG_S = BIRD_IMG_S
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMG_S[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count**2
        if d >= 16:
            d = 16
        elif d < 0:
            d -= 2

        self.y += d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMG_S[0]

        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMG_S[1]

        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMG_S[2]

        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMG_S[1]

        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMG_S[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMG_S[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


# Pipe Class for rendering and actions related to pipes
class Pipe:
    GAP = GAP_PIPE
    VEL = 5

    def __init__(self, x=WIN_WIDTH+100):
        self.x = x
        self.height = None

        self.top = None
        self.bottom = None
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.past = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, WIN_HEIGHT//2 + 50)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_pipe_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_pipe_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_pipe_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_pipe_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_pipe_mask, bottom_pipe_offset)
        t_point = bird_mask.overlap(top_pipe_mask, top_pipe_offset)
        return b_point or t_point


# Base Class to load the ground and make it move
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x_1 = 0
        self.x_2 = self.WIDTH

    def move(self):
        self.x_1 -= self.VEL
        self.x_2 -= self.VEL

        if self.x_1 + self.WIDTH < 0:
            self.x_1 = self.x_2 + self.WIDTH

        if self.x_2 + self.WIDTH < 0:
            self.x_2 = self.x_1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x_1, self.y))
        win.blit(self.IMG, (self.x_2, self.y))


# Function that refreshes the window every frame
def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))
    score_label = SCORE_FONT.render(f'Score: {score}', 1, (255, 255, 255))
    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)

    bird.draw(win)
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 10, 10))
    pygame.display.update()


def game_over_scr(win, score):
    SCORE_LI.append(score)
    win.blit(BG_IMG, (0, 0))

    game_over_label = GAME_OVER_FONT.render(f'Game Over', 1, (255, 255, 255))
    win.blit(game_over_label, (WIN_WIDTH // 2 - game_over_label.get_width() // 2, WIN_HEIGHT//2 - 70))
    game_over_label = GAME_OVER_FONT.render(f'Score: {score}', 1, (255, 255, 255))
    win.blit(game_over_label, (WIN_WIDTH // 2 - game_over_label.get_width() // 2, WIN_HEIGHT//2 - 30))
    pygame.display.update()
    time.sleep(1)


# mainloop
def main(win):
    bird = Bird(WIN_WIDTH//2 - 20, WIN_HEIGHT//2 - 50)
    base = Base(WIN_HEIGHT-70)
    pipes = [Pipe()]
    clock = pygame.time.Clock()
    score = 0
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.move()
        add_pipe = False
        for pipe in pipes:

            if pipe.collide(bird):
                game_over_scr(win, score)
                run = False
                break

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes.remove(pipe)

            if not pipe.past and pipe.x < bird.x:
                pipe.past = True
                add_pipe = True
            pipe.move()
        if not run:
            break
        if add_pipe:
            score += 1
            pipes.append(Pipe())

        if bird.y + bird.img.get_height() >= WIN_HEIGHT-70:
            game_over_scr(win, score)
            break

        base.move()
        draw_window(win, bird, pipes, base, score)


def main_menu():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    r = True
    while r:
        try:
            win.blit(BG_IMG, (0, 0))
            title_label = TITLE_FONT.render("Press space to begin...", 1, (255, 255, 255))
            win.blit(title_label, (WIN_WIDTH // 2 - title_label.get_width() // 2, WIN_HEIGHT//2 - 50))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    r = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main(win)
        except pygame.error:
            break
    pygame.quit()


if __name__ == '__main__':
    main_menu()
    print(SCORE_LI)
