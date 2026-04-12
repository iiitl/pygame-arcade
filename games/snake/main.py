import pygame
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common")))

from colors import *
from constants import *

def run_snake(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None,30)

    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/snake"))

    bg = pygame.image.load(os.path.join(base,"bg.png"))
    bg = pygame.transform.scale(bg,(width,height))

    obstacle_img = pygame.image.load(os.path.join(base,"obstacle.png"))
    obstacle_img = pygame.transform.scale(obstacle_img,(10,10))

    snake = [(100,100)]
    dx,dy = 10,0

    grid = 10

    food = (
        random.randrange(0,width,grid),
        random.randrange(0,height,grid)
    )

    obstacles = []
    for _ in range(25):
        obstacles.append((
            random.randrange(0,width,grid),
            random.randrange(0,height,grid)
        ))

    speed = 8
    score = 0
    started = False
    paused = False

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
                if event.key == pygame.K_UP and dy != 10:
                    dx,dy = 0,-10
                if event.key == pygame.K_DOWN and dy != -10:
                    dx,dy = 0,10
                if event.key == pygame.K_LEFT and dx != 10:
                    dx,dy = -10,0
                if event.key == pygame.K_RIGHT and dx != -10:
                    dx,dy = 10,0

        if paused:
            paused_text = font.render("PAUSED", True, white)
            screen.blit(paused_text, (width//2 - 50,height//2 - 15))

        if started and not paused:
            head = (snake[0][0]+dx, snake[0][1]+dy)
            snake.insert(0, head)

            if head == food:
                score += 1
                food = (
                    random.randrange(0,width,grid),
                    random.randrange(0,height,grid)
                )
            else:
                snake.pop()

            if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
                return "menu"

            if head in obstacles:
                return "menu"

            body = snake.copy()
            body.pop(0)
            if head in body:
                return "menu"

        for s in snake:
            pygame.draw.rect(screen, green, (*s,10,10))

        for o in obstacles:
            screen.blit(obstacle_img,o)

        pygame.draw.rect(screen, red, (*food,10,10))

        text = font.render(f"Score: {score}", True, white)
        screen.blit(text,(width-120,10))

        if not started:
            msg = font.render("Press any key to start", True, white)
            screen.blit(msg,(180,180))

        pygame.display.update()
        clock.tick(speed)
