#!/usr/bin/env python3
"""
Генератор звукових файлів MP3 для Пінг-Понгу
Створює реальні звукові файли на основі синтезу
"""

import numpy as np
from pathlib import Path
import struct

# Базовий шлях
BASE_PATH = Path(__file__).parent
SOUNDS_DIR = BASE_PATH / "assets" / "sounds"
SOUNDS_DIR.mkdir(parents=True, exist_ok=True)

def create_wav(filename, frequency=440, duration=0.1, volume=0.8, sample_rate=44100):
    """Створити WAV файл з однією частотою"""
    num_samples = int(duration * sample_rate)
    
    # Генерувати хвилю
    t = np.linspace(0, duration, num_samples)
    wave = np.sin(2.0 * np.pi * frequency * t)
    
    # Додати огинаючу (ADSR)
    attack = int(sample_rate * 0.01)  # 10ms
    release = int(sample_rate * 0.05)  # 50ms
    
    envelope = np.ones(num_samples)
    # Attack
    envelope[:attack] = np.linspace(0, 1, attack)
    # Release
    envelope[-release:] = np.linspace(1, 0, release)
    
    wave = wave * envelope * volume
    
    # Конвертувати в 16-bit PCM
    wave = (wave * 32767).astype(np.int16)
    
    # Писати WAV файл
    filepath = SOUNDS_DIR / filename
    
    with open(filepath, 'wb') as f:
        # WAV header
        num_channels = 1
        bytes_per_sample = 2
        byte_rate = sample_rate * num_channels * bytes_per_sample
        block_align = num_channels * bytes_per_sample
        
        # RIFF header
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + len(wave) * bytes_per_sample))
        f.write(b'WAVE')
        
        # fmt subchunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))  # Subchunk1Size
        f.write(struct.pack('<H', 1))   # AudioFormat (PCM)
        f.write(struct.pack('<H', num_channels))
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', byte_rate))
        f.write(struct.pack('<H', block_align))
        f.write(struct.pack('<H', 16))  # BitsPerSample
        
        # data subchunk
        f.write(b'data')
        f.write(struct.pack('<I', len(wave) * bytes_per_sample))
        f.write(wave.tobytes())
    
    print(f"✓ {filename} створено ({frequency}Hz, {duration}s)")
    return True

def create_multiple_notes_wav(filename, frequencies, durations, volume=0.8, sample_rate=44100):
    """Створити WAV з кількома нотами"""
    waves = []
    
    for freq, dur in zip(frequencies, durations):
        num_samples = int(dur * sample_rate)
        t = np.linspace(0, dur, num_samples)
        wave = np.sin(2.0 * np.pi * freq * t)
        
        # Огинаюча
        attack = int(sample_rate * 0.01)
        release = int(sample_rate * 0.05)
        envelope = np.ones(num_samples)
        envelope[:attack] = np.linspace(0, 1, attack)
        envelope[-release:] = np.linspace(1, 0, release)
        
        wave = wave * envelope * volume
        waves.append(wave)
    
    full_wave = np.concatenate(waves)
    full_wave = (full_wave * 32767).astype(np.int16)
    
    filepath = SOUNDS_DIR / filename
    
    with open(filepath, 'wb') as f:
        num_channels = 1
        bytes_per_sample = 2
        byte_rate = sample_rate * num_channels * bytes_per_sample
        block_align = num_channels * bytes_per_sample
        
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + len(full_wave) * bytes_per_sample))
        f.write(b'WAVE')
        
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<H', num_channels))
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', byte_rate))
        f.write(struct.pack('<H', block_align))
        f.write(struct.pack('<H', 16))
        
        f.write(b'data')
        f.write(struct.pack('<I', len(full_wave) * bytes_per_sample))
        f.write(full_wave.tobytes())
    
    print(f"✓ {filename} створено (композиція)")
    return True

def main():
    print("🎵 Генерування звукових файлів для Пінг-Понгу\n")
    
    # Звукові ефекти
    print("📢 Звукові ефекти:")
    create_wav("paddle_hit.wav", frequency=800, duration=0.08)
    create_wav("wall_hit.wav", frequency=600, duration=0.06)
    create_multiple_notes_wav("score.wav", 
                             frequencies=[1000, 1200],
                             durations=[0.05, 0.05])
    create_wav("menu_click.wav", frequency=700, duration=0.05)
    
    print("\n🎵 Фонова музика:")
    # Фонова музика - медленная мелодия
    create_multiple_notes_wav(
        "background_music.wav",
        frequencies=[262, 294, 330, 294, 262, 294, 330, 294] * 2,  # Повторюється
        durations=[0.3] * 16
    )
    
    print("\n✨ Всі звуки створені успішно!")
    print(f"📁 Звуки збережені в: {SOUNDS_DIR}")

if __name__ == "__main__":
    main()
