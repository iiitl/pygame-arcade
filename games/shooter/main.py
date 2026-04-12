import pygame
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common")))

from colors import *
from constants import *

def run_shooter(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None,30)

    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/shooter"))

    bg = pygame.image.load(os.path.join(base,"bg.png"))
    bg = pygame.transform.scale(bg,(width,height))

    player_img = pygame.image.load(os.path.join(base,"player.png"))
    player_img = pygame.transform.scale(player_img,(40,40))

    bullet_img = pygame.image.load(os.path.join(base,"bullet.png"))
    bullet_img = pygame.transform.scale(bullet_img,(10,20))

    enemy1 = pygame.image.load(os.path.join(base,"enemy1.png"))
    enemy1 = pygame.transform.scale(enemy1,(40,40))

    enemy2 = pygame.image.load(os.path.join(base,"enemy2.png"))
    enemy2 = pygame.transform.scale(enemy2,(40,40))

    player_x = width//2
    player_y = height - 40

    bullets = []
    enemies = []

    speed = 0.8
    timer = 0
    score = 0
    started = False
    paused = False

    while len(enemies) < 2:
        img = enemy1 if random.randint(0,1)==0 else enemy2
        enemies.append([random.randint(0,width-40),0,img])

    running = True
    while running:
        screen.blit(bg,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                started = True
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_ESCAPE:
                    return "menu" 
                if event.key == pygame.K_SPACE and not paused:
                    bullets.append([player_x+15,player_y])

        if paused:
            paused_text = font.render("PAUSED", True, white)
            screen.blit(paused_text, (width//2 - 50,height//2 - 15))

        if started and not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_x -= 5
            if keys[pygame.K_RIGHT]:
                player_x += 5
            if keys[pygame.K_UP]:
                player_y -= 5
            if keys[pygame.K_DOWN]:
                player_y += 5

            if player_x > width - 40:
                player_x = width - 40
            elif player_x < 0:
                player_x = 0

            if player_y > height - 40:
                player_y = height - 40
            elif player_y < 0:
                player_y = 0

            timer += 1
            if timer % 60 == 0:
                speed += 0.03

            while len(enemies) < 2:
                img = enemy1 if random.randint(0,1)==0 else enemy2
                enemies.append([random.randint(0,width-40),0,img])

        player_rect = pygame.Rect(player_x,player_y,40,40)
        screen.blit(player_img,(player_x,player_y))

        for bullet in bullets[:]:
            if started and not paused:
                bullet[1] -= 7
            screen.blit(bullet_img,(bullet[0],bullet[1]))
            if bullet[1] < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            if started and not paused:
                enemy[1] += speed
            screen.blit(enemy[2],(enemy[0],enemy[1]))

            enemy_rect = pygame.Rect(enemy[0],enemy[1],40,40)

            if started and (enemy_rect.colliderect(player_rect) or enemy[1] > height):
                return "menu"

            for bullet in bullets[:]:
                bullet_rect = pygame.Rect(bullet[0],bullet[1],10,20)
                if bullet_rect.colliderect(enemy_rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

        text = font.render(f"Score: {score}", True, white)
        screen.blit(text,(width-120,10))

        if not started:
            msg = font.render("Press any key to start", True, white)
            screen.blit(msg,(180,180))

        pygame.display.update()
        clock.tick(fps)
