import random
import math
import os

from pygame import mixer
import pygame

from entities.player import Player
from entities.alien import Alien
from entities.bullet import Bullet

current_dir = os.path.dirname(os.path.realpath(__file__))

# Initialize pygame
pygame.init()

# Create a screen
screen = pygame.display.set_mode((800, 600))

# Set background
# TODO: Set dynamic background
background = pygame.image.load(os.path.join(current_dir, 'icons/background-2.jpg'))

# Load background sound
mixer.music.load(os.path.join(current_dir, 'sounds/background.wav'))
mixer.music.play(-1)

# Set the score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

score_board_x = 760
score_board_y = 10

# Set title and icon
pygame.display.set_caption('Spacevader')
icon = pygame.image.load(os.path.join(current_dir, 'icons/ufo.png'))
pygame.display.set_icon(icon)

# Player
player = Player(screen)

# Alien
aliens = []

# Bullet
bullet = Bullet(screen)

def show_score(x, y):
    score_value = font.render(f'{score}', True, (255, 255, 255))
    screen.blit(score_value, (x, y))

def run():
    global player
    global aliens
    global bullet
    global score

    running = True
    while running:
        
        # Fill screen with black
        screen.fill((0, 0, 0))

        # Persist background image
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False

            if event.type is pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player.x_change = player.delta(event.type, event.key)
                if event.key == pygame.K_SPACE and bullet.state == 'READY':
                    bullet.x = player.x
                    bullet.fire(sound=True)

            if event.type is pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player.x_change = player.delta(event.type, event.key)

        player.x += player.x_change

        for i in range(score + 1):

            alien = Alien(x=random.randint(0, 736), y=random.randint(50, 150), x_change=random.choice([-5, 5]), y_change=40, screen=screen)
            aliens.append(alien)

            aliens[i].x += aliens[i].x_change

            # Collision
            collision = aliens[i].has_collided(bullet)
            if collision:
                aliens[i].explode(bullet)
                score += 1

            # Invasion
            if aliens[i].invaded:
                Alien.dispose(aliens)
                Alien.game_over(screen)
                break

            aliens[i].render()
            

        # Bullet movement
        if bullet.y <= 0:
            bullet.y = 480
            bullet.state = 'READY'
        if bullet.state == 'FIRE':
            bullet.fire()
            bullet.y -= bullet._y_change

        player.render()
        show_score(score_board_x, score_board_y)
        pygame.display.update()

if __name__ == '__main__':
    run()