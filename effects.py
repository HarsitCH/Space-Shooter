import pygame
import random
from config import *

class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, POWERUP_WIDTH, POWERUP_HEIGHT)
        self.speed = POWERUP_SPEED
        self.type = random.choice(list(POWERUP_TYPES.keys()))
        self.color = POWERUP_TYPES[self.type]['color']
        self.animation_timer = 0

    def update(self):
        self.rect.y += int(self.speed)
        self.animation_timer += 1
        return self.rect.bottom < HEIGHT

    def draw(self, screen):
        center = self.rect.center
        if self.type == 'rapid_fire':
            # Draw lightning bolt
            points = [
                (center[0] - 5, center[1] - 10),
                (center[0] + 2, center[1] - 2),
                (center[0] - 2, center[1] + 2),
                (center[0] + 5, center[1] + 10)
            ]
            pygame.draw.lines(screen, self.color, False, points, 3)
        elif self.type == 'spread_shot':
            # Draw three arrows
            for i in range(-1, 2):
                start_x = center[0] + i * 8
                pygame.draw.line(screen, self.color, (start_x, center[1] + 5), 
                               (start_x, center[1] - 5), 2)
                pygame.draw.polygon(screen, self.color, [
                    (start_x - 2, center[1] - 5),
                    (start_x + 2, center[1] - 5),
                    (start_x, center[1] - 8)
                ])
        elif self.type == 'shield':
            # Draw shield
            pygame.draw.circle(screen, self.color, center, 10, 2)
            pygame.draw.circle(screen, self.color, center, 6, 2)
        elif self.type == 'extra_life':
            # Draw heart
            pygame.draw.circle(screen, self.color, (center[0] - 3, center[1] - 3), 4)
            pygame.draw.circle(screen, self.color, (center[0] + 3, center[1] - 3), 4)
            points = [
                (center[0] - 7, center[1]),
                (center[0], center[1] + 8),
                (center[0] + 7, center[1])
            ]
            pygame.draw.polygon(screen, self.color, points)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.color = color
        self.lifetime = PARTICLE_LIFETIME
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravity
        self.lifetime -= 1
        self.size = max(1, self.size - 0.1)
        return self.lifetime > 0

    def draw(self, screen):
        alpha = self.lifetime / PARTICLE_LIFETIME
        color = tuple(int(c * alpha) for c in self.color)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.uniform(0.8, 2.5)
        self.brightness = random.randint(150, 255)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-50, 0)

    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 1)