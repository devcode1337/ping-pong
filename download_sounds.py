#!/usr/bin/env python3
"""
Завантажувач звуків та музики для Пінг-Понгу
Скачує звукові ефекти з вільних джерел
"""

import os
import urllib.request
from pathlib import Path

# Базовий шлях
BASE_PATH = Path(__file__).parent
SOUNDS_DIR = BASE_PATH / "assets" / "sounds"
SOUNDS_DIR.mkdir(parents=True, exist_ok=True)

# URL звуків з вільних джерел (альтернативні серверів)
SOUNDS = {
    # Звукові ефекти
    "paddle_hit.wav": "https://assets.mixkit.co/active_storage/sfx/2397/2397-preview.mp3",
    "wall_hit.wav": "https://assets.mixkit.co/active_storage/sfx/2574/2574-preview.mp3",
    "score.wav": "https://assets.mixkit.co/active_storage/sfx/2018/2018-preview.mp3",
    "menu_click.wav": "https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3",
    
    # Фонова музика
    "background_music.mp3": "https://assets.mixkit.co/active_storage/music/3222/3222-preview.mp3",
}

def download_sound(url, filename):
    """Завантажити звуковий файл"""
    filepath = SOUNDS_DIR / filename
    
    if filepath.exists():
        print(f"✓ {filename} вже існує")
        return True
    
    try:
        print(f"⬇️  Завантажую {filename}...")
        # Додати User-Agent щоб уникнути блокування
        request = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        urllib.request.urlopen(request).read()
        urllib.request.urlretrieve(url, filepath)
        print(f"✓ {filename} завантажено успішно")
        return True
    except Exception as e:
        print(f"❌ Помилка при завантаженні {filename}: {e}")
        return False

def main():
    print("🎵 Завантажувач звуків для Пінг-Понгу\n")
    
    success_count = 0
    total_count = len(SOUNDS)
    
    for filename, url in SOUNDS.items():
        if download_sound(url, filename):
            success_count += 1
    
    print(f"\n✨ Завантажено {success_count}/{total_count} файлів")
    
    if success_count == total_count:
        print("\n✅ Всі звуки завантажені!")
        print("🎮 Тепер можете грати з якісними звуками!")
    else:
        print("\n⚠️  Деякі файли не завантажилися.")
        print("💡 Спробуйте вручну завантажити звуки з:")
        print("   - https://pixabay.com/sound-effects/")
        print("   - https://freesound.org/")

if __name__ == "__main__":
    main()
