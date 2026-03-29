import pygame
import random
from config import *

class Player:
    def __init__(self):
        self.x = WIDTH // 2 - PLAYER_WIDTH // 2
        self.y = HEIGHT - 60
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shield_active = False
        self.shield_timer = 0
        self.rapid_fire_active = False
        self.rapid_fire_timer = 0
        self.spread_shot_active = False
        self.spread_shot_timer = 0

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
        self.rect.topleft = (self.x, self.y)

        # Update power-up timers
        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer == 0:
                self.shield_active = False
        
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer == 0:
                self.rapid_fire_active = False
        
        if self.spread_shot_timer > 0:
            self.spread_shot_timer -= 1
            if self.spread_shot_timer == 0:
                self.spread_shot_active = False

    def draw(self, screen):
        cx = self.x + self.width // 2
        
        # Draw shield if active
        if self.shield_active:
            shield_rect = pygame.Rect(self.x - 5, self.y - 5, self.width + 10, self.height + 10)
            pygame.draw.rect(screen, BLUE, shield_rect, 2)
        
        # Main ship triangle (pointing up)
        points = [
            (cx, self.y),  # Nose
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, GREEN, points)
        
        # Center detail line
        pygame.draw.line(screen, (0, 200, 0), (cx, self.y + 5), (cx, self.y + self.height - 3), 2)
        
        # Thruster flame
        flame_points = [
            (cx - 6, self.y + self.height),
            (cx + 6, self.y + self.height),
            (cx, self.y + self.height + 8)
        ]
        pygame.draw.polygon(screen, YELLOW, flame_points)

    def activate_powerup(self, powerup_type):
        if powerup_type == 'rapid_fire':
            self.rapid_fire_active = True
            self.rapid_fire_timer = POWERUP_TYPES['rapid_fire']['duration']
        elif powerup_type == 'spread_shot':
            self.spread_shot_active = True
            self.spread_shot_timer = POWERUP_TYPES['spread_shot']['duration']
        elif powerup_type == 'shield':
            self.shield_active = True
            self.shield_timer = POWERUP_TYPES['shield']['duration']