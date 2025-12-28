"""
Модуль для управління звуками
Генерує та відтворює звукові ефекти
"""

import pygame
import numpy as np
from pathlib import Path
from typing import Optional

class SoundGenerator:
    """Генератор звукових ефектів"""
    
    @staticmethod
    def generate_beep(frequency=440, duration=100, sample_rate=22050):
        """
        Генерувати звуковий сигнал (биття)
        
        Args:
            frequency: Частота в Гц
            duration: Тривалість в мс
            sample_rate: Частота дискретизації
        """
        frames = int(sample_rate * duration / 1000)
        arr = np.sin(2.0 * np.pi * frequency * np.linspace(0, duration/1000, frames))
        
        # Додати огинаючу (ADSR)
        attack = int(frames * 0.05)
        decay = int(frames * 0.1)
        sustain = frames - attack - decay - int(frames * 0.2)
        release = int(frames * 0.2)
        
        envelope = np.concatenate([
            np.linspace(0, 1, attack),
            np.linspace(1, 0.7, decay),
            np.ones(sustain) * 0.7,
            np.linspace(0.7, 0, release)
        ])
        
        arr = arr * envelope
        arr = (arr * 32767).astype(np.int16)
        arr = np.repeat(arr[:, np.newaxis], 2, axis=1)
        
        return pygame.sndarray.make_sound(arr)
    
    @staticmethod
    def generate_platform_hit():
        """Звук удару м'яча об платформу"""
        return SoundGenerator.generate_beep(frequency=800, duration=80)
    
    @staticmethod
    def generate_wall_hit():
        """Звук удару м'яча об стіну"""
        return SoundGenerator.generate_beep(frequency=600, duration=60)
    
    @staticmethod
    def generate_score():
        """Звук набрання очка"""
        # Дві ноти
        sound1 = SoundGenerator.generate_beep(frequency=1000, duration=100)
        sound2 = SoundGenerator.generate_beep(frequency=1200, duration=100)
        return sound1  # Спрощено, використовуємо звичайний биток
    
    @staticmethod
    def generate_menu_click():
        """Звук клік на кнопку"""
        return SoundGenerator.generate_beep(frequency=700, duration=50)


class AudioManager:
    """Менеджер для управління звуками"""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.sounds = {}
        self.current_music = None
        self.volume = 0.8
        
        # Ініціалізувати pygame.mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Загенерувати звуки
        self._generate_sounds()
    
    def _generate_sounds(self):
        """Загенерувати всі звукові ефекти"""
        print("🔊 Генерування звукових ефектів...")
        
        try:
            self.sounds['platform_hit'] = SoundGenerator.generate_platform_hit()
            self.sounds['wall_hit'] = SoundGenerator.generate_wall_hit()
            self.sounds['score'] = SoundGenerator.generate_score()
            self.sounds['menu_click'] = SoundGenerator.generate_menu_click()
            
            print("✓ Звукові ефекти готові")
        except Exception as e:
            print(f"❌ Помилка при генеруванні звуків: {e}")
            self.enabled = False
    
    def play_sound(self, sound_name: str):
        """Відтворити звуковий ефект"""
        if not self.enabled or sound_name not in self.sounds:
            return
        
        try:
            self.sounds[sound_name].set_volume(self.volume)
            self.sounds[sound_name].play()
        except Exception as e:
            print(f"❌ Помилка при відтворенні звуку {sound_name}: {e}")
    
    def set_volume(self, volume: float):
        """Встановити гучність (0.0 - 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def stop_sound(self, sound_name: str):
        """Зупинити звук"""
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
    
    def stop_all(self):
        """Зупинити всі звуки"""
        pygame.mixer.stop()
