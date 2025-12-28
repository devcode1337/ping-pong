"""
Пінг-Понг - Клієнт з розширеним UI та меню
"""

import pygame
from pygame import *
import socket
import json
from threading import Thread
from pathlib import Path
import sys

# Імпортувати модулі UI
from ui_manager import ResourceManager, GameMenu, PlayerSettings, SkinShop, Button
from audio_manager import AudioManager

# --- PYGAME НАЛАШТУВАННЯ ---
WIDTH, HEIGHT = 800, 600
init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Пінг-Понг")

# --- РЕСУРСИ ---
resource_manager = ResourceManager(str(Path(__file__).parent))
audio_manager = AudioManager(enabled=True)

# --- ШРИФТИ ---
font_small = font.Font(None, 24)
font_main = font.Font(None, 36)
font_large = font.Font(None, 72)
font_title = font.Font(None, 80)

# --- ГЛОБАЛЬНІ ЗМІННІ ---
game_state = {}
buffer = ""
client = None
my_id = None
game_over = False
current_screen = "MENU"  # MENU, SETTINGS, SHOP, CONNECTING, GAME, WIN
player_name = ""
selected_ball_skin = "ball_white"
selected_paddle_skin = "paddle_magenta"

# --- СЕРВЕР ---
def connect_to_server():
    """Підключитися до сервера"""
    global client, my_id, buffer, game_state
    
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('localhost', 8080))
            buffer = ""
            game_state = {}
            my_id = int(client.recv(24).decode())
            
            # Відправити інформацію про гравця
            player_info = {
                "name": player_name,
                "ball_skin": selected_ball_skin,
                "paddle_skin": selected_paddle_skin
            }
            client.send(json.dumps(player_info).encode() + b'\n')
            
            print(f"✓ Підключено до сервера. ID: {my_id}")
            return True
        except Exception as e:
            print(f"❌ Помилка підключення: {e}")
            return False


def receive():
    """Отримувати дані від сервера"""
    global buffer, game_state, game_over, current_screen
    
    while not game_over and client:
        try:
            data = client.recv(1024).decode()
            if not data:
                break
            
            buffer += data
            while "\n" in buffer:
                packet, buffer = buffer.split("\n", 1)
                if packet.strip():
                    game_state = json.loads(packet)
                    
                    # Відтворити звукові ефекти
                    if game_state.get('sound_event'):
                        audio_manager.play_sound(game_state['sound_event'])
        except:
            if current_screen == "GAME":
                game_state["winner"] = -1
            break


def draw_game(screen):
    """Малювати ігрове поле"""
    if not game_state:
        return
    
    # Фон
    bg = resource_manager.get_image("bg_main")
    if bg:
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        screen.blit(bg, (0, 0))
    else:
        screen.fill((30, 30, 30))
    
    # Платформи
    left_paddle_skin = resource_manager.get_image(f"paddle_{selected_paddle_skin}")
    if left_paddle_skin:
        paddle_y = game_state['paddles']['0']
        left_paddle_skin = pygame.transform.scale(left_paddle_skin, (20, 100))
        screen.blit(left_paddle_skin, (20, paddle_y))
    else:
        draw.rect(screen, (0, 255, 0), (20, game_state['paddles']['0'], 20, 100))
    
    right_paddle_skin = resource_manager.get_image(f"paddle_{selected_paddle_skin}")
    if right_paddle_skin:
        paddle_y = game_state['paddles']['1']
        right_paddle_skin = pygame.transform.scale(right_paddle_skin, (20, 100))
        screen.blit(right_paddle_skin, (WIDTH - 40, paddle_y))
    else:
        draw.rect(screen, (255, 0, 255), (WIDTH - 40, game_state['paddles']['1'], 20, 100))
    
    # М'яч
    ball_skin = resource_manager.get_image(f"ball_{selected_ball_skin}")
    if ball_skin:
        ball_skin = pygame.transform.scale(ball_skin, (20, 20))
        screen.blit(ball_skin, (game_state['ball']['x'] - 10, game_state['ball']['y'] - 10))
    else:
        draw.circle(screen, (255, 255, 255), (game_state['ball']['x'], game_state['ball']['y']), 10)
    
    # Рахунок
    score_text = font_large.render(
        f"{game_state['scores'][0]} : {game_state['scores'][1]}", 
        True, (255, 255, 255)
    )
    score_rect = score_text.get_rect(center=(WIDTH // 2, 20))
    screen.blit(score_text, score_rect)
    
    # Інформація про гравців
    player_info = font_small.render(f"Гравець: {player_name}", True, (200, 200, 255))
    screen.blit(player_info, (10, 10))


def draw_countdown(screen):
    """Малювати відлік перед грою"""
    if "countdown" in game_state and game_state["countdown"] > 0:
        screen.fill((0, 0, 0))
        countdown_text = font_title.render(str(game_state["countdown"]), True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - 30, HEIGHT // 2 - 50))
        return True
    return False


def draw_win_screen(screen, you_winner):
    """Малювати екран перемоги"""
    screen.fill((20, 20, 20))
    
    if you_winner:
        text = "ТИ ПЕРЕМІГ! 🎉"
        color = (255, 215, 0)
    else:
        text = "ТИ ПРОГРАВ! 😢"
        color = (255, 100, 100)
    
    win_text = font_title.render(text, True, color)
    text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(win_text, text_rect)
    
    restart_text = font_main.render('Натисни K для рестарту', True, color)
    text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
    screen.blit(restart_text, text_rect)


def draw_waiting_screen(screen):
    """Малювати екран очікування"""
    bg = resource_manager.get_image("bg_main")
    if bg:
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        screen.blit(bg, (0, 0))
    else:
        screen.fill((20, 20, 40))
    
    waiting_text = font_main.render("Очікування гравців...", True, (200, 200, 255))
    screen.blit(waiting_text, (WIDTH // 2 - waiting_text.get_width() // 2, HEIGHT // 2))
    
    # Анімована точка
    dots = (int(clock.get_time() / 500) % 4)
    dots_text = font_main.render("." * dots, True, (200, 200, 255))
    screen.blit(dots_text, (WIDTH // 2 - 30, HEIGHT // 2 + 100))


# --- ГОЛОВНІ МЕНЮ ОБЪЕКТИ ---
game_menu = GameMenu(resource_manager, WIDTH, HEIGHT)
player_settings = PlayerSettings(resource_manager, WIDTH, HEIGHT)
skin_shop = SkinShop(resource_manager, WIDTH, HEIGHT)

# Запустити музику в меню
audio_manager.play_music(loop=True)

# --- ГОЛОВНА ГРА ЦИКЛ ---
def main_loop():
    global current_screen, game_over, player_name, selected_ball_skin, selected_paddle_skin
    global my_id, client
    
    you_winner = None
    
    # Ініціалізувати UI об'єкти
    player_settings = PlayerSettings(resource_manager, WIDTH, HEIGHT)
    local_game_menu = game_menu
    local_skin_shop = skin_shop
    
    while True:
        for e in event.get():
            if e.type == QUIT:
                game_over = True
                if client:
                    client.close()
                pygame.quit()
                sys.exit()
            
            # Обробити взаємодію в залежності від екрану
            if current_screen == "MENU":
                action = local_game_menu.handle_event(e)
                if action == "play":
                    current_screen = "SETTINGS"
                    audio_manager.play_sound("menu_click")
                elif action == "settings":
                    current_screen = "SETTINGS"
                    audio_manager.play_sound("menu_click")
                elif action == "shop":
                    current_screen = "SHOP"
                    audio_manager.play_sound("menu_click")
                elif action == "exit":
                    game_over = True
                    if client:
                        client.close()
                    pygame.quit()
                    sys.exit()
            
            elif current_screen == "SETTINGS":
                action = player_settings.handle_event(e)
                if action == "MENU":
                    player_name = player_settings.player_name
                    selected_ball_skin = player_settings.selected_ball_skin
                    selected_paddle_skin = player_settings.selected_paddle_skin
                    current_screen = "MENU"
                    audio_manager.play_sound("menu_click")
                
                # Кнопка "Грати"
                if e.type == KEYDOWN and e.key == K_RETURN:
                    player_name = player_settings.player_name
                    if player_name:
                        current_screen = "CONNECTING"
                        connect_to_server()
                        if my_id is not None:
                            Thread(target=receive, daemon=True).start()
                            current_screen = "GAME"
                        audio_manager.play_sound("menu_click")
            
            elif current_screen == "SHOP":
                action = local_skin_shop.handle_event(e)
                if action == "MENU":
                    current_screen = "MENU"
                    # selected_ball вже має формат "ball_white", потрібно очистити
                    selected_ball_skin = local_skin_shop.selected_ball.split("_", 1)[1] if "_" in local_skin_shop.selected_ball else local_skin_shop.selected_ball
                    selected_paddle_skin = local_skin_shop.selected_paddle.split("_", 1)[1] if "_" in local_skin_shop.selected_paddle else local_skin_shop.selected_paddle
                    audio_manager.play_sound("menu_click")
            
            elif current_screen == "GAME":
                if e.type == KEYDOWN and e.key == K_k and you_winner is not None:
                    current_screen = "MENU"
                    you_winner = None
                    game_state.clear()
                    player_settings = PlayerSettings(resource_manager, WIDTH, HEIGHT)
        
        # КЕРУВАННЯ ПЛАТФОРМОЮ (постійна перевірка натиснутих клавіш)
        if current_screen == "GAME" and client:
            keys = key.get_pressed()
            if keys[K_w]:
                client.send(b"UP")
            elif keys[K_s]:
                client.send(b"DOWN")
        
        # МАЛЮВАННЯ
        if current_screen == "MENU":
            local_game_menu.draw(screen, font_main, font_title)
        
        elif current_screen == "SETTINGS":
            player_settings.draw(screen, font_main, font_title)
        
        elif current_screen == "SHOP":
            local_skin_shop.draw(screen, font_main, font_title)
        
        elif current_screen == "GAME":
            if "countdown" in game_state and game_state["countdown"] > 0:
                draw_countdown(screen)
            elif "winner" in game_state and game_state["winner"] is not None:
                if you_winner is None:
                    you_winner = game_state["winner"] == my_id
                draw_win_screen(screen, you_winner)
            elif game_state:
                draw_game(screen)
            else:
                draw_waiting_screen(screen)
        
        elif current_screen == "CONNECTING":
            screen.fill((0, 0, 0))
            connecting_text = font_main.render("Підключення до сервера...", True, (255, 255, 255))
            screen.blit(connecting_text, (WIDTH // 2 - connecting_text.get_width() // 2, HEIGHT // 2))
        
        display.update()
        clock.tick(60)


if __name__ == "__main__":
    print("🎮 Запуск Пінг-Понгу...")
    print("📦 Ресурси завантажені")
    main_loop()
