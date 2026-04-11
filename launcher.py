import pygame
import os
from games.snake.main import run_snake
from games.flappy.main import run_flappy
from games.shooter.main import run_shooter

pygame.init()
screen = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 40)

base = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets/launcher"))
bg = pygame.image.load(os.path.join(base,"bg.png"))
bg = pygame.transform.scale(bg,(600,400))

options = ["Snake", "Flappy", "Shooter"]
selected = 0

running = True
state = "menu"

while running:
    if state == "menu":
        screen.blit(bg,(0,0))

        for i, text in enumerate(options):
            color = (0,0,0) if i == selected else (255,255,255)
            render = font.render(text, True, color)
            screen.blit(render, (250, 150 + i*50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 3
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3
                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        state = "snake"
                    elif selected == 1:
                        state = "flappy"
                    elif selected == 2:
                        state = "shooter"

        pygame.display.update()
        clock.tick(60)

    elif state == "snake":
        result = run_snake(screen)
        state = result

    elif state == "flappy":
        result = run_flappy(screen)
        state = result

    elif state == "shooter":
        result = run_shooter(screen)
        state = result

    elif state == "quit":
        running = False

pygame.quit()