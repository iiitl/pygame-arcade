import pygame
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common")))
from colors import *
from constants import *
import leaderboard

def run_snake(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("calibri", 30)
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/snake"))

    bg = pygame.image.load(os.path.join(base,"bg.png"))
    bg = pygame.transform.scale(bg,(width,height))
    obstacle_img = pygame.image.load(os.path.join(base,"obstacle.png"))
    obstacle_img = pygame.transform.scale(obstacle_img,(10,10))

    snake = [(100,100)]
    dx,dy = 10,0
    grid = 10
    obstacles = []
    while len(obstacles) < 25:
        pos = (random.randrange(20,width-20,grid), random.randrange(20,height-20,grid))
        if pos not in snake: obstacles.append(pos)

    def place_food():
        while True:
            candidate = (random.randrange(20,width-20,grid), random.randrange(20,height-20,grid))
            if candidate not in snake and candidate not in obstacles: return candidate

    food = place_food()
    speed, score = 8, 0
    started, paused = False, False
    crashed, score_sent = False, False # Leaderboard State
    top_scores = []

    running = True
    while running:
        screen.blit(bg,(0,0))
        panel = pygame.Surface((width-40, height-40), pygame.SRCALPHA)
        panel.fill((*BG_PANEL, 190))
        pygame.draw.rect(panel, (*BG_PANEL_LIGHT, 220), panel.get_rect(), border_radius=16, width=2)
        screen.blit(panel, (20,20))

        for x in range(20, width-20, grid):
            pygame.draw.line(screen, (*BG_SOFT, 40), (x,20), (x,height-20), 1)
        for y in range(20, height-20, grid):
            pygame.draw.line(screen, (*BG_SOFT, 40), (20,y), (width-20,y),1)

        for o in obstacles: screen.blit(obstacle_img,o)
        food_center = (food[0] + 5, food[1] + 5)
        pygame.draw.circle(screen, FOOD_ACCENT, food_center, 5)
        pygame.draw.circle(screen, (255,255,255), (food_center[0]-1, food_center[1]-1), 2)

        for segment in snake[1:]:
            pygame.draw.rect(screen, SNAKE_BODY, (*segment, grid, grid), border_radius=4)
        pygame.draw.rect(screen, SNAKE_HEAD, (*snake[0], grid, grid), border_radius=4)
        screen.blit(font.render(f"Score: {score}", True, white),(width-120,10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT): started = True
                if event.key == pygame.K_ESCAPE: return "menu"
                if event.key == pygame.K_p: paused = not paused
                if not crashed:
                    if event.key == pygame.K_UP and dy == 0: dx,dy = 0,-grid
                    elif event.key == pygame.K_DOWN and dy == 0: dx,dy = 0,grid
                    elif event.key == pygame.K_LEFT and dx == 0: dx,dy = -grid,0
                    elif event.key == pygame.K_RIGHT and dx == 0: dx,dy = grid,0

        if started and not paused and not crashed:
            new_head = (snake[0][0] + dx, snake[0][1] + dy)
            snake.insert(0, new_head)
            if new_head == food:
                score += 1; food = place_food()
            else:
                snake.pop()

            if (new_head[0] < 20 or new_head[0] >= width-20 or 
                new_head[1] < 20 or new_head[1] >= height-20 or 
                new_head in snake[1:] or new_head in obstacles):
                crashed = True # INJECTION

        if paused: screen.blit(font.render("PAUSED", True, white),(width//2 - 50,height//2 - 15))
        if not started: screen.blit(font.render("Press any key to start", True, white),(180,180))

        if crashed:
            if not score_sent:
                leaderboard.submit_score("snake", "Rohit", score)
                top_scores = leaderboard.get_top_scores("snake")
                score_sent = True
            leaderboard.draw_leaderboard_overlay(screen, "snake", top_scores, score)

        pygame.display.update()
        clock.tick(speed)

if __name__ == "__main__":
    pygame.init()
    run_snake(pygame.display.set_mode((width, height)))