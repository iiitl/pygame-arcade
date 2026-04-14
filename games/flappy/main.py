import pygame
import random
import os
import sys

# Ensure common folder is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common")))

from colors import *
from constants import *
import leaderboard # The centralized logic

def run_flappy(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("calibri", 30)

    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/flappy"))

    bg = pygame.image.load(os.path.join(base,"bg.png")).convert()
    bg = pygame.transform.smoothscale(bg,(width,height))

    bird_img = pygame.image.load(os.path.join(base,"bird.png")).convert_alpha()
    bird_img = pygame.transform.smoothscale(bird_img,(40,40))

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
    paused = False
    
    # --- Leaderboard State ---
    score_sent = False
    top_scores = []
    player_name = "Rohit" 

    def create_pipe(x):
        min_gap = bird_h + 65
        max_gap = 180
        gap = random.randint(min_gap, max_gap)
        top = random.randint(50, height - gap - 50)
        return [x, top, gap]

    pipes = []
    for i in range(3):
        pipes.append(create_pipe(width + i*200))

    running = True
    while running:
        screen.blit(bg,(0,0))

        # --- Your Original UI Elements ---
        gradient = pygame.Surface((width, height), pygame.SRCALPHA)
        for y in range(height):
            alpha = int(120 * (y / height))
            pygame.draw.line(gradient, (255, 255, 255, alpha), (0, y), (width, y))
        screen.blit(gradient, (0, 0))

        cloud_shapes = [(60, 50, 160, 44), (240, 40, 140, 38), (440, 70, 130, 34)]
        for cx, cy, cw, ch in cloud_shapes:
            pygame.draw.ellipse(screen, (245, 247, 255, 220), (cx, cy, cw, ch))
            pygame.draw.ellipse(screen, (255, 255, 255, 180), (cx + 10, cy + 10, cw - 30, ch - 16))

        pygame.draw.line(screen, (245, 247, 255, 130), (0, height - 56), (width, height - 56), 3)

        vignette = pygame.Surface((width, height), pygame.SRCALPHA)
        max_radius = max(width, height)
        for radius in range(0, max_radius, 12):
            alpha = int(100 * (radius / max_radius))
            pygame.draw.circle(vignette, (0, 0, 0, alpha), (width // 2, height // 2), radius)
        screen.blit(vignette, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if not started:
                    started = True
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_SPACE and not crashed and not paused:
                    velocity = -6

        if started and not crashed and not paused:
            velocity += gravity
            bird_y += velocity
            timer += 1
            if timer % 60 == 0:
                speed += 0.03    

        bird_rect = pygame.Rect(100, int(bird_y), bird_w, bird_h).inflate(-28, -28)
        offset = (bird_h - bird_rect.height) // 2

        for pipe in pipes[:]:
            if started and not crashed and not paused:
                pipe[0] -= speed

            top_rect = pygame.Rect(pipe[0], 0, pipe_width, pipe[1])
            bottom_rect = pygame.Rect(pipe[0], pipe[1] + pipe[2], pipe_width, height)

            # --- YOUR ORIGINAL PIPE DESIGN (UNTOUCHED) ---
            pipe_color = (70, 140, 70)
            pipe_dark = (50, 100, 50)
            pipe_highlight = (120, 200, 120)

            pygame.draw.rect(screen, pipe_color, top_rect, border_radius=10)
            pygame.draw.rect(screen, pipe_color, bottom_rect, border_radius=10)

            cap_height = 12
            pygame.draw.rect(screen, pipe_dark, (pipe[0]-2, pipe[1]-cap_height, pipe_width+4, cap_height), border_radius=8)
            pygame.draw.rect(screen, pipe_dark, (pipe[0]-2, pipe[1]+pipe[2], pipe_width+4, cap_height), border_radius=8)

            pygame.draw.rect(screen, pipe_highlight, (pipe[0]+10, 16, 12, pipe[1]-16), border_radius=6)
            pygame.draw.rect(screen, pipe_highlight, (pipe[0]+10, pipe[1]+pipe[2]+6, 12, height - (pipe[1]+pipe[2]+6)), border_radius=6)

            if not crashed and bird_rect.colliderect(top_rect) and not paused:
                crashed = True
                crash_time = pygame.time.get_ticks()

            if not crashed and bird_rect.colliderect(bottom_rect) and not paused:
                crashed = True
                crash_time = pygame.time.get_ticks()

            if pipe[0] < -pipe_width and not crashed and not paused:
                pipes.remove(pipe)
                pipes.append(create_pipe(width))
                score += 1

        if started and not crashed and not paused:
            if bird_rect.bottom > height or bird_rect.top < 0:
                crashed = True
                crash_time = pygame.time.get_ticks()

        screen.blit(bird_img, (bird_rect.x - offset, bird_rect.y - offset))

        text = font.render(f"Score: {score}", True, white)
        screen.blit(text, (width - 120, 10))

        if paused:
            p_msg = font.render("PAUSED", True, white)
            screen.blit(p_msg, (width // 2 - 40, height // 2))

        if not started:
            msg = font.render("Press any key to start", True, white)
            screen.blit(msg, (180, 180))

        # --- REFACTORED LEADERBOARD DISPLAY ---
        if crashed:
            if not score_sent:
                # Call network logic once
                leaderboard.submit_score("flappy", player_name, score)
                top_scores = leaderboard.get_top_scores("flappy")
                score_sent = True
            
            # Show the centralized overlay on top of your game
            leaderboard.draw_leaderboard_overlay(screen, "flappy", top_scores, score)
            
            # Keep your original delay before allowing return to menu
            if pygame.time.get_ticks() - crash_time > 2000: # Increased to 2s to see scores
                 if any(pygame.key.get_pressed()): # Wait for any key to return
                    return "menu"

        pygame.display.update()
        clock.tick(fps)

# This makes the window pop up when running main.py directly
if __name__ == "__main__":
    pygame.init()
    # Use standard dimensions from constants
    test_win = pygame.display.set_mode((600, 400)) 
    pygame.display.set_caption("Flappy Test")
    run_flappy(test_win)
    pygame.quit()