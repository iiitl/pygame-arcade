import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "common")))
from constants import *

pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
player_name=""

font = pygame.font.Font(None, 40)
base = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets/launcher"))
bg = pygame.image.load(os.path.join(base,"bg.png"))
bg = pygame.transform.scale(bg,(width,height))

options = ["Snake", "Flappy", "Shooter"]
selected = 0

option_rects = []
for i, text in enumerate(options):
    rect = pygame.Rect(0, 150 + i*50, width, 50)
    option_rects.append(rect)

running = True
while running:
    screen.blit(bg,(0,0))

    for i, text in enumerate(options):
        color = (0,0,0) if i == selected else (255,255,255)
        render = font.render(text, True, color)
        screen.blit(render, (250, 150 + i*50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(option_rects):
                if rect.collidepoint(event.pos):
                    selected = i

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(event.pos):
                        selected = i
                        if selected == 0:
                            os.system("python games/snake/main.py")
                        elif selected == 1:
                            os.system("python games/flappy/main.py")
                        elif selected == 2:
                            os.system("python games/shooter/main.py")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected = (selected - 1) % 3
            if event.key == pygame.K_DOWN:
                selected = (selected + 1) % 3
            if event.key == pygame.K_RETURN:
                if selected == 0:
                    os.system("python games/snake/main.py")
                if selected == 1:
                    os.system("python games/flappy/main.py")
                if selected == 2:
                    os.system("python games/shooter/main.py")

    pygame.display.update()
    clock.tick(60)

pygame.quit()