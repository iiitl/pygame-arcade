import pygame
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common")))

from colors import *
from constants import *

pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
font = pygame.font.Font(None,30)

base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/flappy"))

bg = pygame.image.load(os.path.join(base,"bg.png"))
bg = pygame.transform.scale(bg,(width,height))

bird_img = pygame.image.load(os.path.join(base,"bird.png"))
bird_img = pygame.transform.scale(bird_img,(40,40))

bird_w, bird_h = bird_img.get_size()

bird_y = height//2
velocity = 0
gravity = 0.5

pipe_width = 60

speed = 2
timer = 0
score = 0
started = False

crashed = False
crash_time = 0

def create_pipe(x):
    min_gap = bird_h+65
    max_gap = 180

    gap = random.randint(min_gap, max_gap)
    top = random.randint(50, height - gap - 50)

    return [x, top, gap]

pipes = []
for i in range(3):
    pipes.append(create_pipe(width + i*200))

running = True

paused = False

while running:
    screen.blit(bg,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                paused = not paused
            if not started:
                started = True
            if event.key == pygame.K_SPACE and not crashed and not paused:
                velocity = -6

    
    bird_rect = pygame.Rect(100 + 4, int(bird_y) + 8, bird_w - 8, bird_h - 16)

    if started and not crashed and not paused:
        velocity += gravity
        bird_y += velocity

        timer += 1
        if timer % 60 == 0:
            speed += 0.03

    for pipe in pipes:
        if started and not crashed and not paused:
            pipe[0] -= speed

        top_rect = pygame.Rect(pipe[0]+6,0,pipe_width-12,pipe[1])
        bottom_rect = pygame.Rect(pipe[0]+6,pipe[1]+pipe[2],pipe_width-12,height)

        pygame.draw.rect(screen, black, top_rect)
        pygame.draw.rect(screen, black, bottom_rect)

        if not crashed and bird_rect.colliderect(top_rect) and not paused:
            bird_y = top_rect.bottom - (bird_h // 2)
            crashed = True
            crash_time = pygame.time.get_ticks()

        if not crashed and bird_rect.colliderect(bottom_rect) and not paused:
            bird_y = bottom_rect.top - 8
            crashed = True
            crash_time = pygame.time.get_ticks()

        if pipe[0] < -pipe_width and not crashed and not paused:
            pipes.remove(pipe)
            pipes.append(create_pipe(width))
            score += 1

    if started and not crashed and not paused:
        if bird_y > height or bird_y < 0:
            crashed = True
            crash_time = pygame.time.get_ticks()

    
    if not crashed:
       
        tilt = velocity * -3 
       
        if tilt < -90: tilt = -90 
        if tilt > 45: tilt = 45
        
        rotated_bird = pygame.transform.rotate(bird_img, tilt)
        screen.blit(rotated_bird, (100, int(bird_y)))
    else:
        
        rotated_bird = pygame.transform.rotate(bird_img, -90)
        screen.blit(rotated_bird, (100, int(bird_y)))

    
    text = font.render(f"Score: {score}", True, white)
    screen.blit(text,(width-120,10))

    if paused:
        paused_text = font.render("PAUSED", True, white)
        screen.blit(paused_text, (width//2 - 50,height//2 - 15))

    if not started:
        msg = font.render("Press any key to start", True, white)
        screen.blit(msg,(180,180))

    if crashed:
        if pygame.time.get_ticks() - crash_time > 1000:
            running = False

    pygame.display.update()
    clock.tick(fps)

pygame.quit()