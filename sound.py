import pygame
import numpy as np
from config import *

class SoundManager:
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        try:
            self.generate_sounds()
        except:
            # If sound generation fails, disable sounds
            self.enabled = False
    
    def generate_sounds(self):
        """Generate simple sound effects using numpy"""
        if not pygame.mixer.get_init():
            return
        
        sample_rate = 22050
        
        # Shoot sound
        duration = 0.1
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        frequency = 800
        shoot_wave = np.sin(frequency * 2 * np.pi * t) * np.exp(-t * 10)
        shoot_wave = (shoot_wave * 32767).astype(np.int16)
        stereo_shoot = np.zeros((len(shoot_wave), 2), dtype=np.int16)
        stereo_shoot[:, 0] = shoot_wave
        stereo_shoot[:, 1] = shoot_wave
        shoot_sound = pygame.sndarray.make_sound(stereo_shoot)
        self.sounds['shoot'] = shoot_sound
        
        # Explosion sound
        duration = 0.2
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        noise = np.random.normal(0, 0.1, len(t))
        explosion_wave = noise * np.exp(-t * 5)
        explosion_wave = (explosion_wave * 32767).astype(np.int16)
        stereo_explosion = np.zeros((len(explosion_wave), 2), dtype=np.int16)
        stereo_explosion[:, 0] = explosion_wave
        stereo_explosion[:, 1] = explosion_wave
        explosion_sound = pygame.sndarray.make_sound(stereo_explosion)
        self.sounds['explosion'] = explosion_sound
        
        # Power-up sound
        duration = 0.3
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        frequencies = [400, 600, 800]
        powerup_wave = np.zeros_like(t)
        for freq in frequencies:
            powerup_wave += np.sin(freq * 2 * np.pi * t) * (1/3)
        powerup_wave *= np.exp(-t * 2)
        powerup_wave = (powerup_wave * 32767).astype(np.int16)
        stereo_powerup = np.zeros((len(powerup_wave), 2), dtype=np.int16)
        stereo_powerup[:, 0] = powerup_wave
        stereo_powerup[:, 1] = powerup_wave
        powerup_sound = pygame.sndarray.make_sound(stereo_powerup)
        self.sounds['powerup'] = powerup_sound
        
        # Hit sound
        duration = 0.05
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        frequency = 200
        hit_wave = np.sin(frequency * 2 * np.pi * t) * np.exp(-t * 20)
        hit_wave = (hit_wave * 32767).astype(np.int16)
        stereo_hit = np.zeros((len(hit_wave), 2), dtype=np.int16)
        stereo_hit[:, 0] = hit_wave
        stereo_hit[:, 1] = hit_wave
        hit_sound = pygame.sndarray.make_sound(stereo_hit)
        self.sounds['hit'] = hit_sound
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if self.enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.enabled = not self.enabled