import pygame
import random
import math
from pygame import mixer


# inicijalizacija pygamea
pygame.init()

# pravljenje prozora
screen = pygame.display.set_mode((800,600))

# title i icon i background 32px
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
background = pygame.image.load('background.png')

# background sound
mixer.music.load('TrialCore - Living In Cybercity.mp3')
mixer.music.set_volume(0.4)
mixer.music.play(-1)

# varijable
n = [0, 0, 0, 0, 0, 0] ; k = [0, 0, 0, 0, 0, 0]
over_text = ['','']

# player
slika_player = pygame.image.load('battleship.png')
playerx, playery = 370, 480
X_change,Y_change = 0, 0
score_val = 0
SPEED = 3.5

# enemy
slika_enemy = []
enemyx = []
enemyy = []
enemy_change_x = []
enemy_change_y = []
num_of_enemy = 6

# inicijalizacija enemy-ja
for i in range(num_of_enemy):

    slika_enemy.append(pygame.image.load('mouse.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemy_change_x.append(1)
    enemy_change_y.append(40)

# bullet
slika_bullet = pygame.image.load('bullet.png')
bulletx, bullety = 0, 800
bullet_change_y = 2.5
bullet_state = 'ready' # ready - you cant see bullet on screen
                       # fire - bullet moving

# score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx, texty = 10, 10

# game over text
over = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render('Score: ' + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text[0] = over.render('GAME OVER ' ,True, (255, 255, 255))
    over_text[1] = over.render('Score: ' + str(score_val),True, (255, 255, 255))
    screen.blit(over_text[0], (200, 235))
    screen.blit(over_text[1], (240, 290))

def Collision(bulletx, bullety, enemyx, enemyy):
    distance = math.sqrt((math.pow((enemyx) - bulletx, 2)) + (math.pow((enemyy+16) - bullety, 2)))
    if distance < 29:
        return True
    else:
        return False

def player(x ,y):
    screen.blit(slika_player, (x, y))

def enemy(x, y):
    screen.blit(slika_enemy[i], (x, y))

def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(slika_bullet, (x + 24, y - 16))

# game loop
running = True
while running:
    screen.fill((148, 145, 227))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                X_change = -SPEED

            if event.key == pygame.K_RIGHT:
                X_change = SPEED

            if event.key == pygame.K_UP:
                Y_change = -SPEED

            if event.key == pygame.K_DOWN:
                Y_change = SPEED

            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet(playerx, bullety)
                    bulletx = playerx
                    bullety = playery
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                X_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                Y_change = 0


    playerx += X_change

    for i in range(num_of_enemy):
        enemyx[i] += enemy_change_x[i]
        # granice za enemy
        if enemyx[i] <= 0:
            enemy_change_x[i] = 1 + n[i]
            n[i] = n[i] + 1
            if enemy_change_x[i] >= 4:
                enemy_change_x[i] = 3

            enemyy[i] += enemy_change_y[i]

        if enemyx[i] >= 736:
            enemy_change_x[i] = -1 + k[i]
            k[i] = k[i] - 1
            if enemy_change_x[i] >= 4:
                enemy_change_x[i] = 3
            enemyy[i] += enemy_change_y[i]
        if enemyy[i] > 450 :
            for j in range(num_of_enemy):
                enemyy[j] = 2000

            game_over_text()
            break


        # collision
        col = Collision(bulletx, bullety, enemyx[i], enemyy[i])
        if col:
            bullety = playery
            bullet_state = 'ready'
            score_val += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)
            k[i], n[i] = 0, 0
            ex_sound = mixer.Sound('explosion.wav')
            ex_sound.play()
        enemy(enemyx[i], enemyy[i])

    # granice za player
    if playerx <= 0:
        playerx = 0
    if playerx >= 736:
        playerx = 736
    playery += Y_change
    if playery <= 0:
        playery = 0
    if playery >= 536:
        playery = 536


    # bullet movement
    if bullet_state == 'fire':
        bullet(bulletx,bullety)
        bullety -= bullet_change_y
    if bullety <= 0 :
        bullet_state = 'ready'
        bullety = playery


    show_score(textx, texty)
    player(playerx, playery)
    pygame.display.update()