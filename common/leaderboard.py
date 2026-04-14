import requests
import pygame
from colors import white, red, yellow

BASE_URL = "https://flappy-scores-ec9d5-default-rtdb.firebaseio.com/"

def submit_score(game_id, name, score):
    # This happens once when you die, not every frame (Separates Logic)
    url = f"{BASE_URL}{game_id}_scores.json"
    try:
        requests.post(url, json={"name": name, "score": score}, timeout=2)
    except: pass

def get_top_scores(game_id):
    url = f"{BASE_URL}{game_id}_scores.json"
    try:
        response = requests.get(url, timeout=2)
        if response.text == "null": return []
        data = response.json()
        scores = [{"name": v["name"], "score": v["score"]} for v in data.values()]
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:5]
    except: return []

def draw_leaderboard_overlay(screen, game_id, top_scores, score):
    # This is the Pygame UI (Replaces the blocking input() call)
    w, h = screen.get_size()
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180)) 
    screen.blit(s, (0, 0))
    
    font = pygame.font.SysFont("Arial", 30)
    big_font = pygame.font.SysFont("Arial", 50, bold=True)
    
    screen.blit(big_font.render("GAME OVER", True, red), (w//2 - 120, h//2 - 150))
    screen.blit(font.render(f"Your Score: {score}", True, white), (w//2 - 80, h//2 - 80))
    
    screen.blit(font.render(f"--- TOP 5 {game_id.upper()} ---", True, yellow), (w//2 - 110, h//2 - 20))
    for i, entry in enumerate(top_scores):
        txt = f"{i+1}. {entry['name']}: {entry['score']}"
        screen.blit(font.render(txt, True, white), (w//2 - 100, h//2 + 20 + (i * 30)))
    
    hint_font = pygame.font.SysFont("calibri", 25)
    hint_text = hint_font.render("Press ESC to return to Main Menu", True, (200, 200, 200))
    screen.blit(hint_text, (screen.get_width()//2 - 140, screen.get_height() - 30))