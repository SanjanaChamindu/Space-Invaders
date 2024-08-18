import pygame
import random
from pygame import mixer

# Initialise pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption('Space invader')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load('spaceship.png')
player_x = 380
player_y = 536
player_x_change = 0
player_angel = 0
player_angel_change = 0

# Enemy
enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('alien.png'))
    enemy_x.append(random.randint(0, 768))
    enemy_y.append(random.randint(32, 150))
    enemy_x_change.append(1)
    enemy_y_change.append(30)

# Bullet
bullet_image = pygame.image.load('bullet.png')
bullet_y_change = 10
bullet_status = True
bullet_x = player_x - 8
bullet_y = player_y + 16

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 5
text_y = 5

over_font = pygame.font.Font('freesansbold.ttf', 50)

def show_text(x, y):
    score = font.render(f'Score : {str(score_value)}', True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(a, x, y):
    image_copy = pygame.transform.rotate(player_image, a)
    screen.blit(image_copy, (x - int(image_copy.get_width() / 2), y - int(image_copy.get_height() / 2)))


def enemy(n, x, y):
    screen.blit(enemy_image[n], (x, y))


def fire(x, y):
    global bullet_status
    bullet_status = False
    screen.blit(bullet_image, (x, y))


def is_collision(ex, ey, bx, by):
    if ey - 32 <= by <= ey and ex - 16 <= bx <= ex + 16:
        return True
    else:
        return False


def game_over():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # If keystroke is pressed check whether it is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_status:
                    bullet_sound = mixer.Sound('shoot.wav')
                    bullet_sound.play()
                    bullet_x = player_x - 8
                    bullet_y = player_y + 16
                    fire(bullet_x, bullet_y)
            if event.key == pygame.K_a:
                player_angel_change += 5
            if event.key == pygame.K_d:
                player_angel_change -= 5
            if event.key == pygame.K_w:
                player_angel = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w:
                player_angel_change = 0

    if not bullet_status:
        bullet_y -= bullet_y_change
        fire(bullet_x, bullet_y)

        if bullet_y <= 0:
            bullet_status = True

    player_x += player_x_change
    player_angel = (player_angel + player_angel_change) % 360
    if player_x < 0:
        player_x = 0
    elif player_x > 736:
        player_x = 736

    for i in range(num_of_enemies):
        if enemy_y[i] > 530:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000

            game_over()
            break

        if enemy_x[i] < 0 or enemy_x[i] > 768:
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change[i]

        if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            bullet_status = True

            collision_sound = mixer.Sound('invaderkilled.wav')
            collision_sound.play()

            bullet_x = player_x + 24
            bullet_y = player_y + 48

            enemy_x[i] = random.randint(0, 768)
            enemy_y[i] = random.randint(32, 150)

            score_value += 1

        enemy_x[i] += enemy_x_change[i]
        enemy(i, enemy_x[i], enemy_y[i])

    player(player_angel, player_x, player_y)
    show_text(text_x, text_y)
    pygame.display.update()
