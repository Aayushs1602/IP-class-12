from settings import *
from copy import deepcopy
import pygame
import random
import time

pygame.font.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')
pygame.display.set_icon(pygame.image.load('2048_logo.png'))
TILE_FONT = pygame.font.SysFont(FONT, FONT_SIZE)
START_MENU_FONT = pygame.font.SysFont(FONT, FONT_SIZE)
SCORE_FONT = pygame.font.SysFont(FONT, 30)
POINTS = 0
GRID = ['' for _ in range(16)]
SCORE_LI = [0]
# x = index_in_grid//4, y = index_in_grid % 4


class Tile:
    def __init__(self, pos, num):
        self.pos = pos
        self.num = num
        self.color = TILE_COLORS[num]


    def draw_tile(self):
        pos = self.pos
        txt = str(self.num)
        try:
            color = TILE_COLORS[self.num]
        except KeyError:
            color = TILE_COLORS[1024]

        pygame.draw.rect(WIN, color, ((LINE_THICKNESS*(pos[0]+1))+(TILE_WIDTH*pos[0]),
                                      100 + (LINE_THICKNESS*(pos[1]+1))+(TILE_HEIGHT*pos[1]),
                                      TILE_WIDTH, TILE_HEIGHT))
        font_label = TILE_FONT.render(txt, 1, BLACK if txt in '24' else WHITE)
        WIN.blit(font_label, ((LINE_THICKNESS*(pos[0]+1))+(TILE_WIDTH*pos[0])
                              + TILE_WIDTH//2 - font_label.get_width()//2,
                              100 + (LINE_THICKNESS*(pos[1]+1))+(TILE_HEIGHT*pos[1])
                              + TILE_HEIGHT//2 - font_label.get_height()//2))




def random_tile(GRID):
    k = random.randrange(1, 10)
    if k==10:
        num=4
    else:
        num=2

    choice_li = [z for z in range(16) if GRID[z] == '']
    t = random.choice(choice_li)
    # print(t)
    if len(choice_li)==16:
        num = 2
    # print([t//4, t%4][::-1])
    return Tile([t//4, t%4][::-1], num)


def move_tiles(d):
    global GRID, POINTS
    if d == 'L':
        row1 = GRID[:4]
        row2 = GRID[4:8]
        row3 = GRID[8:12]
        row4 = GRID[12:16]
        # print(row1, row2, row3, row4, sep='\n')
        # print()

        for z in range(4):
            for z in range(3):
                if row1[z]!='' and row1[z+1]!='':
                    if row1[z].num == row1[z + 1].num:
                        row1[z].num += row1[z+1].num
                        POINTS += row1[z].num*POINTS_SCALE_FACTOR
                        # print(POINTS)
                        # print('hm')
                        del row1[z+1]
                        row1.append('')
                        break
            for z in range(3):
                if row2[z] == row2[z+1] != '':
                    if row2[z].num == row2[z + 1].num:
                        row2[z].num += row2[z+1].num
                        POINTS += row2[z].num*POINTS_SCALE_FACTOR
                        del row2[z+1]
                        row2.append('')
                        break
            for z in range(3):
                if row3[z] == row3[z+1] != '':
                    if row3[z].num == row3[z+1].num:
                        row3[z].num += row3[z+1].num
                        POINTS += row3[z].num*POINTS_SCALE_FACTOR
                        del row3[z+1]
                        row3.append('')
                        break
            for z in range(3):
                if row4[z] == row4[z+1] != '':
                    if row4[z].num == row4[z + 1].num:
                        row4[z].num += row4[z+1].num
                        POINTS += row4[z].num*POINTS_SCALE_FACTOR
                        del row4[z+1]
                        row4.append('')
                        break

        for z in range(3):
            if '' in row1:
                row1.remove('')
                row1.append('')
            if '' in row2:
                row2.remove('')
                row2.append('')
            if '' in row3:
                row3.remove('')
                row3.append('')
            if '' in row4:
                row4.remove('')
                row4.append('')

        for z in range(4):
            for z in range(3):
                if row1[z]!='' and row1[z+1]!='':
                    if row1[z].num == row1[z + 1].num:
                        row1[z].num += row1[z+1].num
                        POINTS += row1[z].num * POINTS_SCALE_FACTOR
                        # print('hm')
                        del row1[z+1]
                        row1.append('')
                        break
            for z in range(3):
                if row2[z] != '' and row2[z+1] != '':
                    if row2[z].num == row2[z + 1].num:
                        row2[z].num += row2[z+1].num
                        POINTS += row2[z].num * POINTS_SCALE_FACTOR
                        del row2[z+1]
                        row2.append('')
                        break
            for z in range(3):
                if row3[z]!='' and row3[z+1] != '':
                    if row3[z].num == row3[z+1].num:
                        row3[z].num += row3[z+1].num
                        POINTS += row3[z].num * POINTS_SCALE_FACTOR
                        del row3[z+1]
                        row3.append('')
                        break
            for z in range(3):
                if row4[z]!=0 and row4[z+1] != '':
                    if row4[z].num == row4[z + 1].num:
                        row4[z].num += row4[z+1].num
                        POINTS += row4[z].num * POINTS_SCALE_FACTOR
                        del row4[z+1]
                        row4.append('')
                        break

        for ind, z in enumerate(row1):
            if z!='':
                z.pos = [ind, 0]
        for ind, z in enumerate(row2):
            if z!='':
                z.pos = [ind, 1]
        for ind, z in enumerate(row3):
            if z!='':
                z.pos = [ind, 2]
        for ind, z in enumerate(row4):
            if z!='':
                z.pos = [ind, 3]

        # print(row1, row2, row3, row4, sep='\n')


        GRID = row1+row2+row3+row4

    elif d == 'R':
        row1 = GRID[:4]
        row2 = GRID[4:8]
        row3 = GRID[8:12]
        row4 = GRID[12:16]
        # print(row1, row2, row3, row4, sep='\n')
        # print()
        for z in range(4):
            for z in range(2,-1,-1):
                if row1[z] != '' and row1[z + 1] != '':
                    if row1[z].num == row1[z + 1].num:
                        row1[z + 1].num += row1[z].num
                        POINTS += row1[z+1].num * POINTS_SCALE_FACTOR
                        # print('hm')
                        del row1[z]
                        row1 = [''] + row1
                        break
            for z in range(2,-1,-1):
                if row2[z] != '' and row2[z + 1] != '':
                    if row2[z].num == row2[z + 1].num:
                        row2[z + 1].num += row2[z].num
                        POINTS += row2[z + 1].num * POINTS_SCALE_FACTOR
                        del row2[z]
                        row2 = [''] + row2
                        break
            for z in range(2,-1,-1):
                if row3[z] != '' and row3[z + 1] != '':
                    if row3[z].num == row3[z + 1].num:
                        row3[z + 1].num += row3[z].num
                        POINTS += row3[z + 1].num * POINTS_SCALE_FACTOR
                        del row3[z]
                        row3 = [''] + row3
                        break
            for z in range(2,-1,-1):
                if row4[z] != '' and row4[z + 1] != '':
                    if row4[z].num == row4[z + 1].num:
                        row4[z + 1].num += row4[z].num
                        POINTS += row4[z + 1].num * POINTS_SCALE_FACTOR
                        del row4[z]
                        row4 = [''] + row4
                        break
        for z in range(3):
            if '' in row1:
                row1.remove('')
                row1.append('')
            if '' in row2:
                row2.remove('')
                row2.append('')
            if '' in row3:
                row3.remove('')
                row3.append('')
            if '' in row4:
                row4.remove('')
                row4.append('')
        if '' in row1:
            row1 = row1[row1.index(''):]+row1[:row1.index('')]
        if '' in row2:
            row2 = row2[row2.index(''):]+row2[:row2.index('')]
        if '' in row3:
            row3 = row3[row3.index(''):]+row3[:row3.index('')]
        if '' in row4:
            row4 = row4[row4.index(''):]+row4[:row4.index('')]
        # print(row1, row2, row3, row4, sep='\n')

        for z in range(4):
            for z in range(2,-1,-1):
                if row1[z]!='' and row1[z+1]!='':
                    if row1[z].num == row1[z + 1].num:
                        row1[z+1].num += row1[z].num
                        POINTS += row1[z + 1].num * POINTS_SCALE_FACTOR
                        # print('hm')
                        del row1[z]
                        row1 = [''] + row1
                        break
            for z in range(2,-1,-1):
                if row2[z] != '' and row2[z + 1] != '':
                    if row2[z].num == row2[z + 1].num:
                        row2[z + 1].num += row2[z].num
                        POINTS += row2[z + 1].num * POINTS_SCALE_FACTOR
                        del row2[z]
                        row2 = [''] + row2
                        break
            for z in range(2,-1,-1):
                if row3[z] != '' and row3[z + 1] != '':
                    if row3[z].num == row3[z + 1].num:
                        row3[z + 1].num += row3[z].num
                        POINTS += row3[z + 1].num * POINTS_SCALE_FACTOR
                        del row3[z]
                        row3 = [''] + row3
                        break
            for z in range(2,-1,-1):
                if row4[z] != '' and row4[z + 1] != '':
                    if row4[z].num == row4[z + 1].num:
                        row4[z + 1].num += row4[z].num
                        POINTS += row4[z + 1].num * POINTS_SCALE_FACTOR
                        del row4[z]
                        row4 = [''] + row4
                        break

        for ind, z in enumerate(row1):
            if z!='':
                z.pos = [ind, 0]
        for ind, z in enumerate(row2):
            if z!='':
                z.pos = [ind, 1]
        for ind, z in enumerate(row3):
            if z!='':
                z.pos = [ind, 2]
        for ind, z in enumerate(row4):
            if z!='':
                z.pos = [ind, 3]
        GRID = row1 + row2 + row3 + row4




    elif d == 'U':
        row1 = [GRID[0] , GRID[4] , GRID[8] , GRID[12]]
        row2 = [GRID[1] , GRID[5] , GRID[9] , GRID[13]]
        row3 = [GRID[2] , GRID[6] , GRID[10] , GRID[14]]
        row4 = [GRID[3] , GRID[7] , GRID[11] , GRID[15]]
        # print(row1, row2, row3, row4, sep='\n')
        # print()

        for z in range(4):
            for z in range(3):
                if row1[z] != '' and row1[z + 1] != '':
                    if row1[z].num == row1[z + 1].num:
                        row1[z].num += row1[z + 1].num
                        POINTS += row1[z].num  * POINTS_SCALE_FACTOR
                        # print('hm')
                        del row1[z + 1]
                        row1.append('')
                        break
            for z in range(3):
                if row2[z] == row2[z + 1] != '':
                    if row2[z].num == row2[z + 1].num:
                        row2[z].num += row2[z + 1].num
                        POINTS += row2[z].num * POINTS_SCALE_FACTOR
                        del row2[z + 1]
                        row2.append('')
                        break
            for z in range(3):
                if row3[z] == row3[z + 1] != '':
                    if row3[z].num == row3[z + 1].num:
                        row3[z].num += row3[z + 1].num
                        POINTS += row3[z].num * POINTS_SCALE_FACTOR
                        del row3[z + 1]
                        row3.append('')
                        break
            for z in range(3):
                if row4[z] == row4[z + 1] != '':
                    if row4[z].num == row4[z + 1].num:
                        row4[z].num += row4[z + 1].num
                        POINTS += row4[z].num  * POINTS_SCALE_FACTOR
                        del row4[z + 1]
                        row4.append('')
                        break

        for z in range(3):
            if '' in row1:
                row1.remove('')
                row1.append('')
            if '' in row2:
                row2.remove('')
                row2.append('')
            if '' in row3:
                row3.remove('')
                row3.append('')
            if '' in row4:
                row4.remove('')
                row4.append('')

        for z in range(4):
            for z in range(3):
                if row1[z] != '' and row1[z + 1] != '':
                    if row1[z].num == row1[z + 1].num:
                        row1[z].num += row1[z + 1].num
                        # print('hm')
                        POINTS += row1[z].num * POINTS_SCALE_FACTOR
                        del row1[z + 1]
                        row1.append('')
                        break
            for z in range(3):
                if row2[z] != '' and row2[z + 1] != '':
                    if row2[z].num == row2[z + 1].num:
                        row2[z].num += row2[z + 1].num
                        POINTS += row2[z].num * POINTS_SCALE_FACTOR
                        del row2[z + 1]
                        row2.append('')
                        break
            for z in range(3):
                if row3[z] != '' and row3[z + 1] != '':
                    if row3[z].num == row3[z + 1].num:
                        row3[z].num += row3[z + 1].num
                        POINTS += row3[z].num * POINTS_SCALE_FACTOR
                        del row3[z + 1]
                        row3.append('')
                        break
            for z in range(3):
                if row4[z] != 0 and row4[z + 1] != '':
                    if row4[z].num == row4[z + 1].num:
                        row4[z].num += row4[z + 1].num
                        POINTS += row4[z].num * POINTS_SCALE_FACTOR
                        del row4[z + 1]
                        row4.append('')
                        break
        # print(row1, row2, row3, row4, sep='\n')

        GRID = []
        for r1, r2, r3, r4 in zip(row1,row2,row3,row4):
            GRID.append(r1)
            GRID.append(r2)
            GRID.append(r3)
            GRID.append(r4)

        row1 = GRID[:4]
        row2 = GRID[4:8]
        row3 = GRID[8:12]
        row4 = GRID[12:16]

        for ind, z in enumerate(row1):
            if z != '':
                z.pos = [ind, 0]
        for ind, z in enumerate(row2):
            if z != '':
                z.pos = [ind, 1]
        for ind, z in enumerate(row3):
            if z != '':
                z.pos = [ind, 2]
        for ind, z in enumerate(row4):
            if z != '':
                z.pos = [ind, 3]

    elif d == 'D':
        row1 = [GRID[0], GRID[4], GRID[8], GRID[12]]
        row2 = [GRID[1], GRID[5], GRID[9], GRID[13]]
        row3 = [GRID[2], GRID[6], GRID[10], GRID[14]]
        row4 = [GRID[3], GRID[7], GRID[11], GRID[15]]
        # print(row1, row2, row3, row4, sep='\n')
        # print()
        for z in range(4):
            for z in range(2,-1,-1):
                if row1[z] != '' and row1[z + 1] != '':
                    if row1[z].num == row1[z + 1].num:
                        row1[z + 1].num += row1[z].num
                        # print('hm')
                        POINTS += row1[z+1].num * POINTS_SCALE_FACTOR
                        del row1[z]
                        row1 = [''] + row1
                        break
            for z in range(2,-1,-1):
                if row2[z] != '' and row2[z + 1] != '':
                    if row2[z].num == row2[z + 1].num:
                        row2[z + 1].num += row2[z].num
                        POINTS += row2[z+1].num * POINTS_SCALE_FACTOR
                        del row2[z]
                        row2 = [''] + row2
                        break
            for z in range(2,-1,-1):
                if row3[z] != '' and row3[z + 1] != '':
                    if row3[z].num == row3[z + 1].num:
                        row3[z + 1].num += row3[z].num
                        POINTS += row3[z+1].num * POINTS_SCALE_FACTOR
                        del row3[z]
                        row3 = [''] + row3
                        break
            for z in range(2,-1,-1):
                if row4[z] != '' and row4[z + 1] != '':
                    if row4[z].num == row4[z + 1].num:
                        row4[z + 1].num += row4[z].num
                        POINTS += row4[z+1].num * POINTS_SCALE_FACTOR
                        del row4[z]
                        row4 = [''] + row4
                        break
        for z in range(3):
            if '' in row1:
                row1.remove('')
                row1.append('')
            if '' in row2:
                row2.remove('')
                row2.append('')
            if '' in row3:
                row3.remove('')
                row3.append('')
            if '' in row4:
                row4.remove('')
                row4.append('')
        if '' in row1:
            row1 = row1[row1.index(''):] + row1[:row1.index('')]
        if '' in row2:
            row2 = row2[row2.index(''):] + row2[:row2.index('')]
        if '' in row3:
            row3 = row3[row3.index(''):] + row3[:row3.index('')]
        if '' in row4:
            row4 = row4[row4.index(''):] + row4[:row4.index('')]
        # print(row1, row2, row3, row4, sep='\n')

        for z in range(4):
            for z in range(2,-1,-1):
                if row1[z] != '' and row1[z + 1] != '':
                    if row1[z].num == row1[z + 1].num:
                        row1[z + 1].num += row1[z].num
                        # print('hm')
                        POINTS += row1[z + 1].num * POINTS_SCALE_FACTOR
                        del row1[z]
                        row1 = [''] + row1
                        break
            for z in range(2,-1,-1):
                if row2[z] != '' and row2[z + 1] != '':
                    if row2[z].num == row2[z + 1].num:
                        row2[z + 1].num += row2[z].num
                        POINTS += row2[z + 1].num * POINTS_SCALE_FACTOR
                        del row2[z]
                        row2 = [''] + row2
                        break
            for z in range(2,-1,-1):
                if row3[z] != '' and row3[z + 1] != '':
                    if row3[z].num == row3[z + 1].num:
                        row3[z + 1].num += row3[z].num
                        POINTS += row3[z + 1].num * POINTS_SCALE_FACTOR
                        del row3[z]
                        row3 = [''] + row3
                        break
            for z in range(2,-1,-1):
                if row4[z] != '' and row4[z + 1] != '':
                    if row4[z].num == row4[z + 1].num:
                        row4[z + 1].num += row4[z].num
                        POINTS += row4[z + 1].num * POINTS_SCALE_FACTOR
                        del row4[z]
                        row4 = [''] + row4
                        break
        GRID = []
        for r1, r2, r3, r4 in zip(row1, row2, row3, row4):
            GRID.append(r1)
            GRID.append(r2)
            GRID.append(r3)
            GRID.append(r4)

        row1 = GRID[:4]
        row2 = GRID[4:8]
        row3 = GRID[8:12]
        row4 = GRID[12:16]


        for ind, z in enumerate(row1):
            if z != '':
                z.pos = [ind, 0]
        for ind, z in enumerate(row2):
            if z != '':
                z.pos = [ind, 1]
        for ind, z in enumerate(row3):
            if z != '':
                z.pos = [ind, 2]
        for ind, z in enumerate(row4):
            if z != '':
                z.pos = [ind, 3]


def draw_grid():
    for z in range(5):
        pygame.draw.line(WIN, LINE_COLOR, ((TILE_WIDTH+LINE_THICKNESS)*z+4, 100+4),
                         ((TILE_WIDTH+LINE_THICKNESS)*z+4, (TILE_WIDTH+LINE_THICKNESS)*5), LINE_THICKNESS)

        pygame.draw.line(WIN, LINE_COLOR, (0, (100+(TILE_WIDTH+LINE_THICKNESS)*z+4)),
                         (WIDTH+4, (100+(TILE_WIDTH+LINE_THICKNESS)*z+4)), LINE_THICKNESS)


def game_over():
    # game_over_label = START_MENU_FONT.render('Game Over...', 1, BLACK)
    # WIN.blit(game_over_label,(WIDTH//2 - game_over_label.get_width()//2, WIDTH//2 - game_over_label.get_height()//2))
    time.sleep(2)
    WIN.fill(BLACK)
    im = pygame.image.load('GAME OVER.png')
    WIN.blit(im, (WIDTH//2 - im.get_width()//2, HEIGHT//2 - im.get_height()//2))
    pygame.display.update()
    time.sleep(2)


def check_game_over():
    k = [[], [], [], []]
    for ind, z in enumerate(GRID):
        k[ind//4].append(z)
    for i in range(4):
        for j in range(4):
            cur = k[i][j]
            if i != 0:
                up = k[i-1][j]
                if up.num == cur.num:
                    return False
            if i != 3:
                down = k[i+1][j]
                if down.num == cur.num:
                    return False
            if j != 0:
                left = k[i][j-1]
                if left.num == cur.num:
                    return False
            if j != 3:
                right = k[i][j+1]
                if right.num==cur.num:
                    return False
    return True



def main():
    global GRID, POINTS
    run = True
    POINTS = 0
    clock = pygame.time.Clock()
    GRID = ['' for _ in range(16)]
    tiles = [random_tile(GRID)]
    GRID[tiles[0].pos[1] * 4 + tiles[0].pos[0]] = tiles[0]

    # Draw Func
    def draw_win(tiles):
        WIN.fill(BG_COLOR)
        WIN.blit(score_label, (WIDTH//2 -score_label.get_width()//2, 50-score_label.get_height()//2 + 20))
        WIN.blit(high_score_label, (WIDTH // 2 - high_score_label.get_width() // 2,
                                    50 - high_score_label.get_height() // 2 - 20))

        draw_grid()
        for tile in tiles:
            tile.draw_tile()
        pygame.display.update()

    # main loop
    while run:
        clock.tick(60)
        try:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        prev = GRID
                        move_tiles('L')
                        if prev != GRID:
                            t = random_tile(GRID)
                            tiles.append(t)
                            GRID[t.pos[1] * 4 + t.pos[0]] = t
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        prev = GRID
                        move_tiles('R')
                        if prev != GRID:
                            t = random_tile(GRID)
                            tiles.append(t)
                            GRID[t.pos[1] * 4 + t.pos[0]] = t
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        prev = GRID
                        move_tiles('U')
                        if prev != GRID:
                            t = random_tile(GRID)
                            tiles.append(t)
                            GRID[t.pos[1] * 4 + t.pos[0]] = t
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        prev = GRID
                        move_tiles('D')
                        if prev != GRID:
                            t = random_tile(GRID)
                            tiles.append(t)
                            GRID[t.pos[1] * 4 + t.pos[0]] = t
        except pygame.error:
            pass
        try:
            tiles = [z for z in GRID if z != '']
            score_label = SCORE_FONT.render(f'SCORE: {POINTS}', 1, BLACK)
            high_score_label = SCORE_FONT.render(f'HIGH SCORE: {max(SCORE_LI)}', 1, BLACK)
            draw_win(tiles)
            if '' not in GRID:
                d = check_game_over()
                print(d)
                if d:
                    game_over()
                    run = False

        except pygame.error:
            pass


def main_menu():
    run = True
    while run:
        WIN.fill(BLACK)
        start_menu_label = START_MENU_FONT.render('Press any button to start......', 1, WHITE)
        WIN.blit(start_menu_label, (WIDTH//2 - start_menu_label.get_width()//2,
                                    HEIGHT//2 - start_menu_label.get_height()//2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
                SCORE_LI.append(POINTS)
        try:
            pygame.display.update()
        except pygame.error:
            run = False


main_menu()
print(max(SCORE_LI))