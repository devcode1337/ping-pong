"""
Генератор текстур для гри Пінг-Понг
Створює всі необхідні зображення та ресурси для гри
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

# Визначити базовий шлях
BASE_PATH = Path(__file__).parent

ASSETS_DIR = BASE_PATH / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
BG_DIR = IMAGES_DIR / "backgrounds"
BALLS_DIR = IMAGES_DIR / "balls"
PADDLES_DIR = IMAGES_DIR / "paddles"
BUTTONS_DIR = IMAGES_DIR / "buttons"
SOUNDS_DIR = ASSETS_DIR / "sounds"

# Створити директорії
for directory in [BG_DIR, BALLS_DIR, PADDLES_DIR, BUTTONS_DIR, SOUNDS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


def create_gradient_background(filename, width=800, height=600, color1=(20, 20, 40), color2=(40, 20, 60)):
    """Створити фон з градієнтом"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    img.save(filename)
    print(f"✓ Створено: {filename}")


def create_ball(filename, size=20, color=(255, 255, 255), shadow=True):
    """Створити текстуру м'яча"""
    img = Image.new('RGBA', (size * 2 + 10, size * 2 + 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Тінь
    if shadow:
        draw.ellipse(
            [(2, 2), (size * 2 + 6, size * 2 + 6)],
            fill=(0, 0, 0, 80)
        )
    
    # М'яч
    draw.ellipse(
        [(5, 5), (size * 2 + 5, size * 2 + 5)],
        fill=color
    )
    
    # Блиск
    draw.ellipse(
        [(7, 7), (size + 5, size + 5)],
        fill=(255, 255, 255, 100)
    )
    
    img.save(filename)
    print(f"✓ Створено: {filename}")


def create_paddle(filename, width=20, height=100, color=(255, 0, 255)):
    """Створити текстуру платформи"""
    img = Image.new('RGBA', (width + 10, height + 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Основна платформа з градієнтом
    for i in range(height):
        ratio = i / height
        brightness = int(200 + 55 * ratio)
        current_color = (
            int(color[0] * brightness / 255),
            int(color[1] * brightness / 255),
            int(color[2] * brightness / 255),
        )
        draw.line([(5, 5 + i), (width + 5, 5 + i)], fill=current_color)
    
    # Бордюр
    draw.rectangle([(5, 5), (width + 5, height + 5)], outline=(255, 255, 255), width=2)
    
    img.save(filename)
    print(f"✓ Створено: {filename}")


def create_button(filename, width=200, height=50, text="", color=(100, 200, 255)):
    """Створити кнопку"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Основа кнопки
    draw.rectangle([(0, 0), (width - 1, height - 1)], fill=color, outline=(200, 200, 200), width=2)
    
    # Блиск на кнопці
    draw.rectangle([(2, 2), (width - 3, height // 2)], fill=(255, 255, 255), outline=None)
    
    # Текст (якщо є)
    if text:
        try:
            # Спробувати використати системний шрифт
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    img.save(filename)
    print(f"✓ Створено: {filename}")


def create_ui_panel(filename, width=600, height=400, title=""):
    """Створити панель інтерфейсу"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 150))
    draw = ImageDraw.Draw(img)
    
    # Бордюр
    draw.rectangle([(2, 2), (width - 2, height - 2)], outline=(200, 150, 255), width=3)
    
    # Заголовок
    if title:
        draw.rectangle([(2, 2), (width - 2, 50)], fill=(100, 50, 150))
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()
        
        draw.text((20, 15), title, fill=(255, 255, 255), font=font)
    
    img.save(filename)
    print(f"✓ Створено: {filename}")


def create_skin_data():
    """Створити конфіг скінів"""
    skin_config = {
        "balls": [
            {
                "id": "ball_white",
                "name": "Білий м'яч",
                "file": "ball_white.png",
                "color": (255, 255, 255),
                "price": 0,
                "unlocked": True
            },
            {
                "id": "ball_red",
                "name": "Червоний м'яч",
                "file": "ball_red.png",
                "color": (255, 50, 50),
                "price": 100,
                "unlocked": False
            },
            {
                "id": "ball_blue",
                "name": "Синій м'яч",
                "file": "ball_blue.png",
                "color": (50, 100, 255),
                "price": 100,
                "unlocked": False
            },
            {
                "id": "ball_gold",
                "name": "Золотий м'яч",
                "file": "ball_gold.png",
                "color": (255, 200, 0),
                "price": 200,
                "unlocked": False
            },
            {
                "id": "ball_green",
                "name": "Зелений м'яч",
                "file": "ball_green.png",
                "color": (50, 255, 50),
                "price": 100,
                "unlocked": False
            }
        ],
        "paddles": [
            {
                "id": "paddle_magenta",
                "name": "Магента платформа",
                "file": "paddle_magenta.png",
                "color": (255, 0, 255),
                "price": 0,
                "unlocked": True
            },
            {
                "id": "paddle_green",
                "name": "Зелена платформа",
                "file": "paddle_green.png",
                "color": (0, 255, 0),
                "price": 100,
                "unlocked": False
            },
            {
                "id": "paddle_blue",
                "name": "Синя платформа",
                "file": "paddle_blue.png",
                "color": (0, 150, 255),
                "price": 100,
                "unlocked": False
            },
            {
                "id": "paddle_gold",
                "name": "Золота платформа",
                "file": "paddle_gold.png",
                "color": (255, 200, 0),
                "price": 200,
                "unlocked": False
            },
            {
                "id": "paddle_neon",
                "name": "Неон платформа",
                "file": "paddle_neon.png",
                "color": (0, 255, 200),
                "price": 300,
                "unlocked": False
            }
        ]
    }
    
    import json
    config_file = ASSETS_DIR / "config" / "skins.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(skin_config, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Створено: {config_file}")
    return skin_config


def generate_all_assets():
    """Генерувати всі текстури"""
    print("🎮 Генерування текстур для Пінг-Понгу...\n")
    
    # Фони
    print("📦 Фони:")
    create_gradient_background(str(BG_DIR / "bg_main.png"))
    create_gradient_background(str(BG_DIR / "bg_menu.png"), color1=(10, 5, 20), color2=(50, 20, 80))
    create_gradient_background(str(BG_DIR / "bg_settings.png"), color1=(20, 10, 30), color2=(40, 30, 60))
    
    # М'ячі
    print("\n🔵 М'ячі:")
    create_ball(str(BALLS_DIR / "ball_white.png"), color=(255, 255, 255))
    create_ball(str(BALLS_DIR / "ball_red.png"), color=(255, 50, 50))
    create_ball(str(BALLS_DIR / "ball_blue.png"), color=(50, 100, 255))
    create_ball(str(BALLS_DIR / "ball_gold.png"), color=(255, 200, 0))
    create_ball(str(BALLS_DIR / "ball_green.png"), color=(50, 255, 50))
    
    # Платформи
    print("\n🎯 Платформи:")
    create_paddle(str(PADDLES_DIR / "paddle_magenta.png"), color=(255, 0, 255))
    create_paddle(str(PADDLES_DIR / "paddle_green.png"), color=(0, 255, 0))
    create_paddle(str(PADDLES_DIR / "paddle_blue.png"), color=(0, 150, 255))
    create_paddle(str(PADDLES_DIR / "paddle_gold.png"), color=(255, 200, 0))
    create_paddle(str(PADDLES_DIR / "paddle_neon.png"), color=(0, 255, 200))
    
    # Кнопки
    print("\n🔘 Кнопки:")
    create_button(str(BUTTONS_DIR / "btn_play.png"), text="Грати", color=(100, 200, 100))
    create_button(str(BUTTONS_DIR / "btn_settings.png"), text="Налаштування", color=(100, 150, 200))
    create_button(str(BUTTONS_DIR / "btn_exit.png"), text="Вихід", color=(200, 100, 100))
    create_button(str(BUTTONS_DIR / "btn_back.png"), text="Назад", color=(150, 150, 150))
    create_button(str(BUTTONS_DIR / "btn_buy.png"), text="Купити", color=(200, 150, 50))
    create_button(str(BUTTONS_DIR / "btn_select.png"), text="Вибрати", color=(100, 200, 150))
    
    # UI Панелі
    print("\n📋 UI Панелі:")
    create_ui_panel(str(IMAGES_DIR / "ui_main_menu.png"), title="ПІНГ-ПОНГ")
    create_ui_panel(str(IMAGES_DIR / "ui_settings.png"), title="НАЛАШТУВАННЯ")
    create_ui_panel(str(IMAGES_DIR / "ui_shop.png"), width=700, height=500, title="МАГАЗИН СКІНІВ")
    
    # Конфіг скінів
    print("\n⚙️  Конфіг:")
    create_skin_data()
    
    print("\n✨ Усі текстури успішно створені!")


if __name__ == "__main__":
    generate_all_assets()
