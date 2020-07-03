# importing req modules
import pygame
import random

pygame.font.init()

SCORE_LI = []

DMG_PER_SHOT = 10
MAX_HEALTH = 100

FPS = 60
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load(r'assets\space_invaders_logo.jpg'))

# LOADING THE ASSETS
RED_SPACE_SHIP = pygame.image.load(r'assets\pixel_ship_red_small.png')
GREEN_SPACE_SHIP = pygame.image.load(r'assets\pixel_ship_green_small.png')
BLUE_SPACE_SHIP = pygame.image.load(r'assets\pixel_ship_blue_small.png')

# Main Player Space Ship
YELLOW_SPACE_SHIP = pygame.image.load(r'assets\pixel_ship_yellow.png')

# Space Ship Lasers
RED_LASER = pygame.image.load(r'assets\pixel_laser_red.png')
GREEN_LASER = pygame.image.load(r'assets\pixel_laser_green.png')
BLUE_LASER = pygame.image.load(r'assets\pixel_laser_blue.png')
YELLOW_LASER = pygame.image.load(r'assets\pixel_laser_yellow.png')

# Background
BG = pygame.transform.scale(pygame.image.load(r'assets\background-black.png'), (WIDTH, HEIGHT))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self):
        return not (HEIGHT >= self.y > -30)

    def collision(self, obj):
        return collide(obj, self)


class Ship:
    COOL_DOWN = 30

    def __init__(self, x, y, health=MAX_HEALTH):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_laser(self, vel, obj):
        self.cool_down()

        for laser in self.lasers:
            laser.move(vel)

            if laser.off_screen():
                self.lasers.remove(laser)

            elif laser.collision(obj):
                obj.health -= DMG_PER_SHOT
                self.lasers.remove(laser)

    def cool_down(self):
        if self.cool_down_counter >= self.COOL_DOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=MAX_HEALTH):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_laser(self, vel, obj_s):
        self.cool_down()

        for laser in self.lasers:
            laser.move(vel)

            if laser.off_screen():
                try:
                    self.lasers.remove(laser)
                except ValueError:
                    pass
            else:
                for obj in obj_s:
                    if laser.collision(obj):
                        try:
                            obj_s.remove(obj)
                            self.lasers.remove(laser)
                        except ValueError:
                            pass

    def health_bar(self):
        pygame.draw.rect(WIN, (255, 0, 0), (self.x, self.y + self.get_height() + 10, self.get_width(), 10))
        pygame.draw.rect(WIN, (0, 255, 0), (self.x, self.y + self.get_height() + 10,
                                            self.get_width() * self.health / MAX_HEALTH, 10))

    def draw(self, window):
        super().draw(window)
        self.health_bar()


class Enemy(Ship):
    COLOR_MAP = {'r': (RED_SPACE_SHIP, RED_LASER),
                 'g': (GREEN_SPACE_SHIP, GREEN_LASER),
                 'b': (BLUE_SPACE_SHIP, BLUE_LASER)}

    def __init__(self, x, y, color, health=MAX_HEALTH):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj_1, obj_2):
    offset_x = obj_2.x - obj_1.x
    offset_y = obj_2.y - obj_1.y
    return obj_1.mask.overlap(obj_2.mask, (offset_x, offset_y)) is not None


def main():
    run = True
    level = 0
    lives = 5

    main_font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 60)
    clock = pygame.time.Clock()

    enemies = []
    wave_length = 5
    enemy_vel = 1

    laser_vel = 5

    player_vel = 5
    player = Player(300, 630)
    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))

        # Draw Text
        lives_label = main_font.render(f'Lives: {lives}', 1, (255, 255, 255))
        level_label = main_font.render(f'Level: {level}', 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for en in enemies:
            en.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH // 2 - lost_label.get_width() // 2, 350))

        player.draw(WIN)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives == 0 or player.health <= 0:
            lost = True
            lost_count += 1
        if lost:
            if lost_count > FPS * 3:
                run = False
                SCORE_LI.append(level)
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100),
                              random.randrange(-1500 * ((level // 5) + 1), -100),
                              random.choice(['r', 'g', 'b']))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SCORE_LI.append(level)
                pygame.quit()

        keys = pygame.key.get_pressed()
        # Left
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x - player_vel + 10 >= 0:
            player.x -= player_vel

        # Right
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + player_vel + player.get_width() - 10 < WIDTH:
            player.x += player_vel

        # Up
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y - player_vel + 10 >= 0:
            player.y -= player_vel

        # Down
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + player_vel + + player.get_height() + 15 < HEIGHT:
            player.y += player_vel

        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_laser(laser_vel, player)

            if not random.randrange(0, 2 * FPS):
                enemy.shoot()

            if collide(enemy, player):
                player.health -= DMG_PER_SHOT + 2
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_laser(-laser_vel, enemies)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        try:
            WIN.blit(BG, (0, 0))
            title_label = title_font.render("Press any key to begin...", 1, (255, 255, 255))
            WIN.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, 350))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    main()
        except pygame.error:
            break
    pygame.quit()


if __name__ == '__main__':
    main_menu()
    print(SCORE_LI)
