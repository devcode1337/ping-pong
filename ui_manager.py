"""
Модуль для управління ресурсами та UI компонентами
"""

import pygame
import json
from pathlib import Path
from typing import Dict, Tuple, Optional

class ResourceManager:
    """Менеджер для завантаження та управління ресурсами"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.assets_path = self.base_path / "assets"
        self.images = {}
        self.sounds = {}
        self.skins_config = {}
        self.load_all_resources()
    
    def load_all_resources(self):
        """Завантажити всі ресурси"""
        self.load_images()
        self.load_skins_config()
    
    def load_images(self):
        """Завантажити всі зображення"""
        images_dir = self.assets_path / "images"
        
        if not images_dir.exists():
            print(f"⚠️  Директорія з зображеннями не знайдена: {images_dir}")
            return
        
        # Завантажити фони
        bg_dir = images_dir / "backgrounds"
        if bg_dir.exists():
            for img_file in bg_dir.glob("*.png"):
                try:
                    self.images[img_file.stem] = pygame.image.load(str(img_file))
                except Exception as e:
                    print(f"❌ Помилка завантаження {img_file.name}: {e}")
        
        # Завантажити м'ячі
        balls_dir = images_dir / "balls"
        if balls_dir.exists():
            for img_file in balls_dir.glob("*.png"):
                try:
                    self.images[f"ball_{img_file.stem}"] = pygame.image.load(str(img_file)).convert_alpha()
                except Exception as e:
                    print(f"❌ Помилка завантаження {img_file.name}: {e}")
        
        # Завантажити платформи
        paddles_dir = images_dir / "paddles"
        if paddles_dir.exists():
            for img_file in paddles_dir.glob("*.png"):
                try:
                    self.images[f"paddle_{img_file.stem}"] = pygame.image.load(str(img_file)).convert_alpha()
                except Exception as e:
                    print(f"❌ Помилка завантаження {img_file.name}: {e}")
        
        # Завантажити кнопки
        buttons_dir = images_dir / "buttons"
        if buttons_dir.exists():
            for img_file in buttons_dir.glob("*.png"):
                try:
                    self.images[f"btn_{img_file.stem}"] = pygame.image.load(str(img_file)).convert_alpha()
                except Exception as e:
                    print(f"❌ Помилка завантаження {img_file.name}: {e}")
        
        # Завантажити UI панелі
        if images_dir.exists():
            for img_file in images_dir.glob("ui_*.png"):
                try:
                    self.images[img_file.stem] = pygame.image.load(str(img_file)).convert_alpha()
                except Exception as e:
                    print(f"❌ Помилка завантаження {img_file.name}: {e}")
        
        print(f"✓ Завантажено {len(self.images)} зображень")
    
    def load_skins_config(self):
        """Завантажити конфіг скінів"""
        config_file = self.assets_path / "config" / "skins.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.skins_config = json.load(f)
                print(f"✓ Конфіг скінів завантажено")
            except Exception as e:
                print(f"❌ Помилка завантаження конфігу скінів: {e}")
        else:
            print(f"⚠️  Конфіг скінів не знайдено: {config_file}")
    
    def get_image(self, name: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """Отримати зображення за назвою"""
        if name not in self.images:
            print(f"⚠️  Зображення не знайдено: {name}")
            return None
        
        img = self.images[name]
        if size:
            img = pygame.transform.scale(img, size)
        return img
    
    def get_skin_data(self, skin_type: str) -> list:
        """Отримати дані скінів певного типу"""
        return self.skins_config.get(skin_type, [])


class Button:
    """Клас для кнопки в меню"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str = "", 
                 color: Tuple[int, int, int] = (100, 150, 200), image: Optional[pygame.Surface] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.image = image
        self.hovered = False
        self.clicked = False
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Обробити подію миші"""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
        return False
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Малювати кнопку"""
        # Колір залежить від стану
        current_color = tuple(min(c + 30, 255) for c in self.color) if self.hovered else self.color
        
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, current_color, self.rect)
            pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        
        # Текст на кнопці
        if self.text:
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)


class SkinShop:
    """Магазин скінів"""
    
    def __init__(self, resource_manager: ResourceManager, screen_width: int, screen_height: int):
        self.resource_manager = resource_manager
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_tab = "balls"  # "balls" або "paddles"
        self.player_coins = 500  # Поточні монети гравця
        self.selected_ball = "ball_white"
        self.selected_paddle = "paddle_magenta"
        self.buttons = self._create_buttons()
    
    def _create_buttons(self):
        """Створити кнопки магазину"""
        buttons = {
            "balls_tab": Button(50, 80, 150, 50, "М'ячі", (100, 150, 200)),
            "paddles_tab": Button(250, 80, 150, 50, "Платформи", (100, 150, 200)),
            "back": Button(650, 20, 120, 40, "Назад", (150, 100, 100)),
        }
        
        # Кнопки для скінів
        skins = self.resource_manager.get_skin_data("balls")
        for i, skin in enumerate(skins):
            buttons[f"skin_{skin['id']}"] = Button(
                50 + (i % 3) * 200,
                200 + (i // 3) * 150,
                180, 130,
                "", (80, 80, 100)
            )
        
        return buttons
    
    def handle_event(self, event: pygame.event.Event):
        """Обробити подію"""
        for button_name, button in self.buttons.items():
            if button.handle_event(event):
                self._handle_button_click(button_name)
    
    def _handle_button_click(self, button_name: str):
        """Обробити клік на кнопку"""
        if button_name == "balls_tab":
            self.current_tab = "balls"
        elif button_name == "paddles_tab":
            self.current_tab = "paddles"
        elif button_name == "back":
            return "MENU"  # Повернутися до меню
        # Обробити клік на скін
        if button_name.startswith("skin_"):
            skin_id = button_name.replace("skin_", "")
            if self.current_tab == "balls":
                self.selected_ball = skin_id
            else:
                self.selected_paddle = skin_id
        
        return None
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font, large_font: pygame.font.Font):
        """Малювати магазин"""
        # Фон
        bg = self.resource_manager.get_image("ui_shop")
        if bg:
            bg = pygame.transform.scale(bg, (self.screen_width, self.screen_height))
            screen.blit(bg, (0, 0))
        else:
            screen.fill((20, 20, 40))
        
        # Заголовок
        title = large_font.render("МАГАЗИН СКІНІВ", True, (255, 200, 100))
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 20))
        
        # Вкладки
        self.buttons["balls_tab"].draw(screen, font)
        self.buttons["paddles_tab"].draw(screen, font)
        self.buttons["back"].draw(screen, font)
        
        # Монети
        coins_text = font.render(f"Монети: {self.player_coins}", True, (255, 200, 100))
        screen.blit(coins_text, (20, self.screen_height - 40))
        
        # Список скінів поточної вкладки
        skins = self.resource_manager.get_skin_data(self.current_tab)
        
        for i, skin in enumerate(skins):
            button_key = f"skin_{skin['id']}"
            if button_key in self.buttons:
                button = self.buttons[button_key]
                button.draw(screen, font)
                
                # Інформація про скін
                name_text = font.render(skin['name'], True, (255, 255, 255))
                price_text = font.render(f"💰 {skin['price']}", True, (255, 200, 0))
                
                screen.blit(name_text, (button.rect.x, button.rect.y + 100))
                screen.blit(price_text, (button.rect.x, button.rect.y + 120))
                
                # Позначка обраного скіну
                if (self.current_tab == "balls" and skin['id'] == self.selected_ball) or \
                   (self.current_tab == "paddles" and skin['id'] == self.selected_paddle):
                    pygame.draw.rect(screen, (0, 255, 0), button.rect, 3)


class GameMenu:
    """Головне меню гри"""
    
    def __init__(self, resource_manager: ResourceManager, screen_width: int, screen_height: int):
        self.resource_manager = resource_manager
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = {
            "play": Button(screen_width // 2 - 100, 200, 200, 60, "Грати", (100, 200, 100)),
            "settings": Button(screen_width // 2 - 100, 300, 200, 60, "Налаштування", (100, 150, 200)),
            "shop": Button(screen_width // 2 - 100, 400, 200, 60, "Магазин", (200, 150, 100)),
            "exit": Button(screen_width // 2 - 100, 500, 200, 60, "Вихід", (200, 100, 100)),
        }
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Обробити подію, повернути дію"""
        for action, button in self.buttons.items():
            if button.handle_event(event):
                return action
        return None
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font, large_font: pygame.font.Font):
        """Малювати меню"""
        # Фон
        bg = self.resource_manager.get_image("bg_menu")
        if bg:
            bg = pygame.transform.scale(bg, (self.screen_width, self.screen_height))
            screen.blit(bg, (0, 0))
        else:
            screen.fill((30, 10, 50))
        
        # Заголовок
        title = large_font.render("ПІНГ-ПОНГ", True, (255, 100, 200))
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))
        
        # Кнопки
        for button in self.buttons.values():
            button.draw(screen, font)


class PlayerSettings:
    """Налаштування гравця"""
    
    def __init__(self, resource_manager: ResourceManager, screen_width: int, screen_height: int):
        self.resource_manager = resource_manager
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_name = ""
        self.selected_ball_skin = "ball_white"
        self.selected_paddle_skin = "paddle_magenta"
        self.back_button = Button(screen_width // 2 - 100, 500, 200, 60, "Назад", (150, 100, 100))
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Обробити подію"""
        if self.back_button.handle_event(event):
            return "MENU"
        
        # Обробити введення тексту
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif len(self.player_name) < 20:
                self.player_name += event.unicode
        
        return None
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font, large_font: pygame.font.Font):
        """Малювати налаштування"""
        # Фон
        bg = self.resource_manager.get_image("bg_settings")
        if bg:
            bg = pygame.transform.scale(bg, (self.screen_width, self.screen_height))
            screen.blit(bg, (0, 0))
        else:
            screen.fill((20, 10, 30))
        
        # Заголовок
        title = large_font.render("НАЛАШТУВАННЯ", True, (200, 150, 255))
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 30))
        
        # Введення імені
        name_label = font.render("Ім'я гравця:", True, (255, 255, 255))
        screen.blit(name_label, (100, 150))
        
        # Поле вводу
        input_rect = pygame.Rect(100, 200, 400, 50)
        pygame.draw.rect(screen, (50, 50, 80), input_rect)
        pygame.draw.rect(screen, (200, 200, 200), input_rect, 2)
        
        name_text = font.render(self.player_name, True, (255, 255, 255))
        screen.blit(name_text, (110, 210))
        
        # Інформація про скіни
        ball_label = font.render(f"М'яч: {self.selected_ball_skin}", True, (255, 200, 100))
        paddle_label = font.render(f"Платформа: {self.selected_paddle_skin}", True, (255, 200, 100))
        screen.blit(ball_label, (100, 300))
        screen.blit(paddle_label, (100, 350))
        
        # Кнопка назад
        self.back_button.draw(screen, font)
