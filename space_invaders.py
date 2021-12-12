import pygame
from pygame import mixer
import random
import math

# Initializing PyGame
pygame.init()

# Creating the game window
screen = pygame.display.set_mode((800, 600))

# Loading the Background Image
backgroundImg = pygame.image.load("background.png")

# Loading the Background Music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 20

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 460
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Scoring System
score_value = 0
font = pygame.font.Font("helloPirates.ttf", 64)
textX = 10
textY = 10

# Game Over!
game_over_font = pygame.font.Font("helloPirates.ttf", 96)

def drawPlayer(x, y):
    screen.blit(playerImg, (x, y))

def drawEnemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance <= 27:
        return True
    else:
        return False

def write_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over():
    game_over_text = game_over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(game_over_text, (150, 250))

# Main Game Loop
running = True
while running:

    # Looping through all the events that happened
    for event in pygame.event.get():

        # Exit-on-quit event
        if event.type == pygame.QUIT:
            running = False

        # Check for arrow key strokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 3

            if event.key == pygame.K_LEFT:
                playerX_change = -3

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()

        # Check for arrow key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # RGB Screen Coloring
    screen.fill((0, 0, 0))

    # Applying Background Image
    screen.blit(backgroundImg, (0, 0))

    # Place the player's icon
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    drawPlayer(playerX, playerY)

    # Place the enemies' icons & implement collisions
    for i in range(num_of_enemies):

        # Checking for Game Over
        if enemyY[i] >= 420:

            # Move out all the enemies
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            # Display the game over text
            game_over()
            break

        # Drawing the enemies
        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 736:
            enemyX[i] = 736
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = -2
        elif enemyX[i] <= 0:
            enemyX[i] = 0
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = 2

        # Bullet Collisions
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            explode = mixer.Sound("explosion.wav")
            explode.play()
            bullet_state = "ready"
            bulletY = 460
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        drawEnemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bullet_state == "fire":
        bulletY -= bulletY_change
        fire_bullet(bulletX, bulletY)

        # Bullet Motion Range
        if bulletY <= 0:
            bullet_state = "ready"
            bulletY = 460

    # Write the Score before updating
    write_score(textX, textY)

    # Update the display after all changes have been done
    pygame.display.update()
