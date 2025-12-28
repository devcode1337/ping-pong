"""
Модуль для управління звуками та музикою
Завантажує звукові файли та музику з папки assets/sounds
"""

import pygame
from pathlib import Path
from typing import Optional


class AudioManager:
    """Менеджер для управління звуками та музикою"""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.sounds = {}
        self.current_music = None
        self.volume = 0.8
        
        # Ініціалізувати pygame.mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Завантажити звуки
        self._load_sounds()
    
    def _load_sounds(self):
        """Завантажити всі звукові ефекти та музику"""
        sounds_dir = Path(__file__).parent / "assets" / "sounds"
        
        print("🔊 Завантаження звуків...")
        
        # Звукові ефекти (WAV формат для швидкої відповіді)
        sound_files = {
            'platform_hit': 'paddle_hit.wav',
            'wall_hit': 'wall_hit.wav',
            'score': 'score.wav',
            'menu_click': 'menu_click.wav',
        }
        
        for sound_key, filename in sound_files.items():
            filepath = sounds_dir / filename
            if filepath.exists():
                try:
                    self.sounds[sound_key] = pygame.mixer.Sound(str(filepath))
                    print(f"  ✓ {sound_key} завантажено")
                except Exception as e:
                    print(f"  ❌ Помилка при завантаженні {filename}: {e}")
                    self.sounds[sound_key] = None
            else:
                print(f"  ⚠️  {filename} не знайдено")
                self.sounds[sound_key] = None
        
        # Фонова музика - спробуємо WAV або MP3
        for music_file in ['background_music.wav', 'background_music.mp3']:
            self.music_path = sounds_dir / music_file
            if self.music_path.exists():
                print(f"  ✓ {music_file} знайдено")
                return
        
        print(f"  ⚠️  background_music не знайдено")
        self.music_path = None
    
    def play_sound(self, sound_key: str):
        """
        Відтворити звуковий ефект
        
        Args:
            sound_key: Ключ звуку ('platform_hit', 'wall_hit', 'score', 'menu_click')
        """
        if not self.enabled:
            return
        
        if sound_key in self.sounds and self.sounds[sound_key] is not None:
            try:
                self.sounds[sound_key].set_volume(self.volume)
                self.sounds[sound_key].play()
            except Exception as e:
                print(f"Помилка при відтворенні звуку {sound_key}: {e}")
    
    def play_music(self, loop: bool = True):
        """
        Відтворити фонову музику
        
        Args:
            loop: Повторювати музику нескінченно
        """
        if not self.enabled or not hasattr(self, 'music_path') or not self.music_path:
            return
        
        if not self.music_path.exists():
            print(f"Музика не знайдена: {self.music_path}")
            return
        
        try:
            pygame.mixer.music.load(str(self.music_path))
            pygame.mixer.music.play(-1 if loop else 0)
            pygame.mixer.music.set_volume(self.volume * 0.5)  # Музика тихіша за ефекти
            print(f"🎵 Фонова музика запущена: {self.music_path.name}")
        except Exception as e:
            print(f"Помилка при завантаженні музики: {e}")
    
    def stop_music(self):
        """Зупинити фонову музику"""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Помилка при зупинці музики: {e}")
    
    def set_volume(self, volume: float):
        """
        Встановити гучність
        
        Args:
            volume: Гучність від 0 до 1
        """
        self.volume = max(0, min(1, volume))
        try:
            pygame.mixer.music.set_volume(self.volume * 0.5)
        except:
            pass
    
    def toggle_mute(self):
        """Вмикнути/вимкнути звук"""
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop_music()
        else:
            if hasattr(self, 'music_path') and self.music_path.exists():
                self.play_music()
