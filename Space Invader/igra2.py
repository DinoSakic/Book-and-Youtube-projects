import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((1024, 700), pygame.RESIZABLE)

NUM_OF_ENEMY = 20
default_size = (1024, 700)
# counter = 0
resize = False
background = pygame.image.load('background.png')
enemy_slika = pygame.image.load('mouse.png')

def window():
    pygame.display.set_caption('Kvisling')
    icon = pygame.image.load('ufo.png')
    pygame.display.set_icon(icon)

def back(back, x):
    background = pygame.transform.scale(back, x)  # (1024, 700))
    return background

def Collision(bulletx, bullety, enemyx, enemyy):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow((enemyy+16) - bullety, 2)))
    if distance < 29:
        return True
    else:
        return False

class Player:
    def __init__(self, x_coord, y_coord, x_change, y_change, SPEED):
        self.x = x_coord
        self.y = y_coord
        self.x_change = x_change
        self.y_change = y_change
        self.speed = SPEED
        self.slika = pygame.image.load('battleship.png')

    def img(self):
        screen.blit(player.slika, (self.x, self.y))

class Bullet:
    def __init__(self, x_coord, y_coord, SPEED):
        self.slika = pygame.image.load('bullet.png')
        self.x = x_coord
        self.y = y_coord
        self.state = 'ready'
        self.speed = SPEED

    def fire(self, x, y):
        self.state = 'fire'
        screen.blit(self.slika, (x + 24, y - 16))

class Enemy:
    def __init__(self, x_change, y_change, SPEED, CHANGE):
        self.slika = enemy_slika
        self.x = random.randint(0, default_size[0] - 65)
        self.y = random.randint(0, 200)
        self.x_change = x_change
        self.y_change = y_change
        self.speed = SPEED
        self.speed_change = CHANGE

    def img(self):
        screen.blit(enemy_slika, (self.x, self.y))

class Tekts:
    def __init__(self):
        # score
        self.score = 0
        self.x_score = 10
        self.y_score = 10
        self.font_score = pygame.font.Font('freesansbold.ttf', 32)

        # game over
        self.x_game = 255
        self.y_game = 255
        self.font_game = pygame.font.Font('freesansbold.ttf', 64)
        self.over_text1 = ''
        self.over_text2 = ''

    def show_score(self):
        score = self.font_score.render('Score: ' + str(self.score), True, (255, 255, 255))
        screen.blit(score, (self.x_score, self.y_score))

    def game_over_text(self):
        self.over_text1 = self.font_game.render('GAME OVER ', True, (255, 255, 255))
        self.over_text2 = self.font_game.render('Score: ' + str(self.score), True, (255, 255, 255))
        screen.blit(self.over_text1, (self.x_game, self.y_game))
        screen.blit(self.over_text2, (self.x_game + 40, self.y_game + 55))

# sound
pygame.mixer.music.load('TrialCore - Living In Cybercity.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
ex_sound = pygame.mixer.Sound('explosion.wav')
bullet_sound = pygame.mixer.Sound('laser.wav')

score = Tekts()

enemies = []
for enemy in range(NUM_OF_ENEMY):
    enemies.append(Enemy(x_change=1, y_change=40, SPEED=1, CHANGE=0.5))

player = Player(x_coord=default_size[0]/2 -32, y_coord=default_size[1] - 128, x_change=0, y_change=0, SPEED=2.5)
bullet1 = Bullet(x_coord=player.x, y_coord=player.y, SPEED=2.5)
bullet2 = Bullet(x_coord=player.x, y_coord=player.y, SPEED=2.5)

# TODO: omoguciti pucanje drugog metka

window()
screen.blit(back(background, default_size), (0, 0))
pygame.display.update()

run = True
while run:
    for event in pygame.event.get():
        # kontrola prozora
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(background, event.dict['size']), (0, 0))
            resize = True
            width_height = (pygame.display.get_surface().get_size()) # vraca 2 vrijednosti: width & height

            # kontrole za igraca
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -player.speed
            if event.key == pygame.K_RIGHT:
                player.x_change = player.speed
            if event.key == pygame.K_UP:
                player.y_change = -player.speed
            if event.key == pygame.K_DOWN:
                player.y_change = player.speed

            # fizika metka
            if event.key == pygame.K_SPACE:
                if bullet1.state == 'ready':
                    # counter = 1
                    bullet1.fire(player.x, bullet1.y)
                    bullet1.x = player.x
                    bullet1.y = player.y
                    bullet_sound.play()
            # if event.key == pygame.K_SPACE and counter == 1:
            #     if bullet2.state == 'ready':
            #         counter = 1
            #         bullet2.fire(player.x, bullet2.y)
            #         bullet2.x = player.x
            #         bullet2.y = player.y
            #         bullet_sound.play()

                # TODO treba naci bolje rijesenje za KEYUP

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.y_change = 0

    # granice za player
    #   -velicina slike je 64x64
    if not resize:
        if player.x <= 0:
            player.x = 0
        if player.x >= default_size[0] - 64:
            player.x = default_size[0] - 64
        if player.y <= 0:
            player.y = 0
        if player.y >= default_size[1] - 64:
            player.y = default_size[1] - 64
    elif resize:
        if player.x <= 0:
            player.x = 0
        if player.x >= width_height[0] - 64:
            player.x = width_height[0] - 64
        if player.y <= 0:
            player.y = 0
        if player.y >= width_height[1] - 64:
            player.y = width_height[1] - 64

    # background
    if not resize:
        background = back(background, default_size) # neka default vrijednost velicine prozora
    elif resize:
        background = back(background, width_height)
    screen.blit(background, (0, 0))

    if bullet1.state == 'fire':
        bullet1.y -= bullet1.speed
        bullet1.fire(bullet1.x, bullet1.y)
    if bullet1.y <= 0:
        bullet1.state = 'ready'
    # if bullet2.state == 'fire':
    #     bullet2.y -= bullet2.speed
    #     bullet2.fire(bullet2.x, bullet2.y)
    # if bullet2.y <= 0:
    #     bullet2.state = 'ready'

    # enemy
    if not resize:
        for enemy in enemies:
            enemy.x += enemy.x_change
            # granice za enemy
            if enemy.x <= 0:
                enemy.x_change = enemy.speed
                enemy.speed += enemy.speed_change
                if enemy.x_change >= 3:
                    enemy.x_change = 3

                enemy.y += enemy.y_change

            if enemy.x >= default_size[0] - 64:
                enemy.x_change = -enemy.speed

                enemy.y += enemy.y_change

            if enemy.y >= default_size[1] - 128:
                for j in range(len(enemies)):
                    enemies[j].y = 2000

                Tekts.game_over_text(score)
                break

            # collision
            col = Collision(bullet1.x, bullet1.y, enemy.x, enemy.y)
            if col:
                bullet_state = 'ready'
                score.score += 1
                enemy.x = random.randint(0, default_size[0] - 65)
                enemy.y = random.randint(50, 150)
                enemy.speed = 1
                enemy.x_change = 1
                ex_sound.play()

            Enemy.img(enemy)

    elif resize:
        for enemy in enemies:
            enemy.x += enemy.x_change
            if enemy.x <= 0:
                enemy.x_change = enemy.speed
                enemy.speed += enemy.speed_change
                if enemy.x_change >= 3:
                    enemy.x_change = 3

                enemy.y += enemy.y_change

            if enemy.x >= width_height[0] - 64:
                enemy.x_change = -enemy.speed
                enemy.y += enemy.y_change

            if enemy.y >= width_height[1] - 128:
                for j in range(len(enemies)):
                    enemies[j].y = 2000

                Tekts.game_over_text(score)
                break
                
            # collision
            col = Collision(bullet1.x, bullet1.y, enemy.x, enemy.y)
            if col:
                bullet1.state = 'ready'
                score.score += 1
                enemy.x = random.randint(0, width_height[0] - 65)
                enemy.y = random.randint(50, 150)
                enemy.speed = 1
                enemy.x_change = 1
                ex_sound.play()
            # Enemy.img(enemy)

            Enemy.img(enemy)
    # kretanje playera
    player.x += player.x_change
    player.y += player.y_change
    Player.img(player)
    Tekts.show_score(score)

    pygame.display.update()
print(player.x, player.y, bullet1.x, bullet1.y)
