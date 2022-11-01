import pygame
import random
import math
from pygame import mixer

# Init pygame
pygame.init()

# Create a screem
screen = pygame.display.set_mode((800, 600))
# Background
background_img = pygame.image.load("space.jpg")
# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("launch.png")
pygame.display.set_icon(icon)  # it doesn't seem to work on linux mint

# Player
player_img = pygame.image.load("player.png")
# Left top corner is our 0, 0 for x,y
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemy_img.append(pygame.image.load("alien.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.2)
    enemy_y_change.append(40)

# Missile
missile_img = pygame.image.load("missile.png")
missile_x = 0
missile_y = 480
missile_y_change = 0.5
# Ready state is not visible, fired is visible
missile_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
font_game_over = pygame.font.Font("freesansbold.ttf", 64)
text_x = 10
text_y = 10


def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    game_over = font_game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, position):
    screen.blit(enemy_img[position], (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fired"
    screen.blit(missile_img, (x + 16, y + 10))


def is_collision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    return distance < 27


# Infinite loop (game loop) until cross of popup window is pressed
running = True

while running:

    # RGB This print all the screen, so always first
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check key has been pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.3
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.3
            if event.key == pygame.K_SPACE and missile_state == "ready":
                blast_sound = mixer.Sound('blaster.wav')
                blast_sound.play()
                missile_x = player_x
                fire_missile(missile_x, missile_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # change position of player
    player_x += player_x_change
    # set boundaries for player
    if player_x <= 0:
        player_x = 0
    if player_x >= 736:
        player_x = 736
    # print the player
    player(player_x, player_y)
    # change position of enemies
    for i in range(number_of_enemies):
        # Game over
        if enemy_y[i] >= 440:
            for j in range(number_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break
        # Update enemies positions
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.2
            enemy_y[i] += enemy_y_change[i]
        if enemy_x[i] >= 736:
            enemy_x_change[i] = -0.2
            enemy_y[i] += enemy_y_change[i]
        # Render enemy
        enemy(enemy_x[i], enemy_y[i], i)
        # Collision detection
        collision = is_collision(enemy_x[i], enemy_y[i], missile_x, missile_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            missile_y = 480
            missile_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
    # Missile movement
    if missile_state == "fired":
        fire_missile(missile_x, missile_y)
        missile_y -= missile_y_change
    if missile_y <= 0:
        missile_y = 480
        missile_state = "ready"
    # Show score
    show_score(text_x, text_y)
    pygame.display.update()  # This updates the changes in the screen
