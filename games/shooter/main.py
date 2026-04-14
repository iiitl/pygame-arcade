import pygame
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common")))
from colors import *
from constants import *
import leaderboard

def run_shooter(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None,30)
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/shooter"))

    bg = pygame.image.load(os.path.join(base,"bg.png")).convert()
    bg = pygame.transform.smoothscale(bg,(width,height))
    player_img = pygame.image.load(os.path.join(base,"player.png")).convert_alpha()
    player_img = pygame.transform.smoothscale(player_img,(40,40))
    bullet_img = pygame.image.load(os.path.join(base,"bullet.png")).convert_alpha()
    bullet_img = pygame.transform.smoothscale(bullet_img,(10,20))
    enemy1 = pygame.image.load(os.path.join(base,"enemy1.png")).convert_alpha()
    enemy1 = pygame.transform.smoothscale(enemy1,(40,40))
    enemy2 = pygame.image.load(os.path.join(base,"enemy2.png")).convert_alpha()
    enemy2 = pygame.transform.smoothscale(enemy2,(40,40))

    player_x, player_y = width//2, height - 40
    bullets, enemies = [], []
    speed, timer, score = 0.8, 0, 0
    started, paused = False, False
    
    # Leaderboard Hooks
    crashed, score_sent = False, False
    top_scores = []

    while len(enemies) < 2:
        img = enemy1 if random.randint(0,1)==0 else enemy2
        enemies.append([random.randint(0,width-40),0,img])

    running = True
    while running:
        screen.blit(bg,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.KEYDOWN:
                started = True
                if event.key == pygame.K_ESCAPE: return "menu"
                if event.key == pygame.K_p: paused = not paused
                if event.key == pygame.K_SPACE and not paused and not crashed:
                    bullets.append([player_x+15,player_y])

        if paused:
            screen.blit(font.render("PAUSED", True, white), (width//2 - 50,height//2 - 15))

        if started and not paused and not crashed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: player_x -= 5
            if keys[pygame.K_RIGHT]: player_x += 5
            if keys[pygame.K_UP]: player_y -= 5
            if keys[pygame.K_DOWN]: player_y += 5
            player_x = max(0, min(width - 40, player_x))
            player_y = max(0, min(height - 40, player_y))

            timer += 1
            if timer % 60 == 0: speed += 0.03
            while len(enemies) < 2:
                img = enemy1 if random.randint(0,1)==0 else enemy2
                enemies.append([random.randint(0,width-40),0,img])

        player_rect = pygame.Rect(player_x,player_y,40,40)
        screen.blit(player_img,(player_x,player_y))

        for bullet in bullets[:]:
            if started and not paused and not crashed: bullet[1] -= 7
            screen.blit(bullet_img,(bullet[0],bullet[1]))
            if bullet[1] < 0: bullets.remove(bullet)

        for enemy in enemies[:]:
            if started and not paused and not crashed: enemy[1] += speed
            screen.blit(enemy[2],(enemy[0],enemy[1]))
            enemy_rect = pygame.Rect(enemy[0],enemy[1],40,40)

            if started and not crashed and (enemy_rect.colliderect(player_rect) or enemy[1] > height):
                crashed = True # INJECTION: Stop game, don't exit yet

            for bullet in bullets[:]:
                if pygame.Rect(bullet[0],bullet[1],10,20).colliderect(enemy_rect):
                    bullets.remove(bullet); enemies.remove(enemy); score += 1; break

        screen.blit(font.render(f"Score: {score}", True, white),(width-120,10))
        if not started: screen.blit(font.render("Press any key to start", True, white),(180,180))

        if crashed:
            if not score_sent:
                leaderboard.submit_score("shooter", "Rohit", score)
                top_scores = leaderboard.get_top_scores("shooter")
                score_sent = True
            leaderboard.draw_leaderboard_overlay(screen, "shooter", top_scores, score)

        pygame.display.update()
        clock.tick(fps)

if __name__ == "__main__":
    pygame.init()
    run_shooter(pygame.display.set_mode((width, height)))