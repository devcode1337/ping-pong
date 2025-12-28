#!/usr/bin/env python3
"""
Скрипт для швидкого старту гри
Встановлює залежності та генерує ресурси
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Виконати команду та показати результат"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {description} - УСПІШНО\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ПОМИЛКА: {e}\n")
        return False

def main():
    print("\n" + "="*60)
    print("🎮 ПІНГ-ПОНГ - ШВИДКИЙ СТАРТ")
    print("="*60)
    
    base_path = Path(__file__).parent
    
    # Крок 1: Встановлення залежностей
    if not run_command(
        f"{sys.executable} -m pip install pygame numpy Pillow",
        "Встановлення залежностей (pygame, numpy, Pillow)"
    ):
        print("⚠️  Спробуйте встановити залежності вручну:")
        print("   pip install pygame numpy Pillow")
        return
    
    # Крок 2: Генерування ресурсів
    if not run_command(
        f"{sys.executable} {base_path}/assets_generator.py",
        "Генерування текстур та звуків"
    ):
        print("⚠️  Спробуйте запустити вручну:")
        print(f"   python {base_path}/assets_generator.py")
        return
    
    # Крок 3: Інструкції
    print("\n" + "="*60)
    print("✨ ГОТОВО ДО ЗАПУСКУ!")
    print("="*60)
    print("""
Тепер виконайте наступні кроки:

1️⃣  ЗАПУСТІТЬ СЕРВЕР (в одному терміналі):
   python server.py

2️⃣  ЗАПУСТІТЬ КЛІЄНТІВ (у двох окремих терміналах):
   python client.py
   python client.py

3️⃣  ИГРАЙТЕ!
   - W/S для рухання платформи
   - K для рестарту після гри
   - Mouse для кліків на кнопки

Для детальної інформації див. README.md 📖
    """)

if __name__ == "__main__":
    main()
