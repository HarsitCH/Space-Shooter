import pygame
import random
from config import *

class Bullet:
    def __init__(self, x, y, speed=BULLET_SPEED, angle=0):
        self.rect = pygame.Rect(int(x), int(y), BULLET_WIDTH, BULLET_HEIGHT)
        self.speed = speed
        self.angle = angle
        self.dx = 0
        self.dy = -speed
        if angle != 0:
            self.dx = speed * 0.5 * (1 if angle > 0 else -1)
            self.dy = -speed * 0.7

    def update(self):
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)
        return self.rect.top > 0 and self.rect.bottom < HEIGHT and self.rect.left > 0 and self.rect.right < WIDTH

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Enemy:
    def __init__(self, x, y, enemy_type='basic', speed_multiplier=1.0):
        self.type = enemy_type
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.rect = pygame.Rect(int(x), int(y), self.width, self.height)
        self.speed_multiplier = speed_multiplier
        self.health = 1
        self.timer = random.randint(0, 60)
        
        if enemy_type == 'basic':
            self.speed = ENEMY_BASE_SPEED * speed_multiplier
            self.color = RED
            self.score_value = 10
        elif enemy_type == 'zigzag':
            self.speed = ENEMY_ZIGZAG_SPEED * speed_multiplier
            self.color = ORANGE
            self.score_value = 20
            self.direction = random.choice([-1, 1])
        elif enemy_type == 'chaser':
            self.speed = ENEMY_CHASER_SPEED * speed_multiplier
            self.color = PURPLE
            self.score_value = 30
        elif enemy_type == 'speeder':
            self.speed = ENEMY_BASE_SPEED * speed_multiplier * 1.8
            self.color = YELLOW
            self.score_value = 25
            self.direction = random.choice([-1, 1])
        elif enemy_type == 'tank':
            self.speed = ENEMY_BASE_SPEED * speed_multiplier * 0.5
            self.color = (100, 100, 100)
            self.score_value = 40
            self.health = 2

    def update(self, player_x=None):
        self.timer += 1
        
        if self.type == 'basic':
            self.rect.y += int(self.speed)
        elif self.type == 'zigzag':
            self.rect.y += int(self.speed)
            if self.timer % 25 == 0:
                self.direction *= -1
            self.rect.x += int(self.direction * self.speed * 0.6)
        elif self.type == 'chaser' and player_x is not None:
            self.rect.y += int(self.speed)
            if abs(player_x - self.rect.centerx) > 5:
                move_x = self.speed * 0.4 * (1 if player_x > self.rect.centerx else -1)
                self.rect.x += int(move_x)
        elif self.type == 'speeder':
            self.rect.y += int(self.speed)
            self.rect.x += int(self.direction * self.speed * 0.7)
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.direction *= -1
        elif self.type == 'tank':
            self.rect.y += int(self.speed)
        
        return self.rect.bottom < HEIGHT

    def draw(self, screen):
        if self.type == 'tank':
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, (50, 50, 50), self.rect, 2)
        elif self.type == 'speeder':
            cx = self.rect.centerx
            points = [
                (cx, self.rect.bottom),
                (self.rect.left, self.rect.centery),
                (cx, self.rect.top),
                (self.rect.right, self.rect.centery)
            ]
            pygame.draw.polygon(screen, self.color, points)
        else:
            cx = self.rect.centerx
            points = [
                (cx, self.rect.bottom),
                (self.rect.left, self.rect.top),
                (self.rect.right, self.rect.top)
            ]
            pygame.draw.polygon(screen, self.color, points)

class Boss:
    def __init__(self, x, y, health_multiplier=1.0):
        self.rect = pygame.Rect(int(x), int(y), BOSS_WIDTH, BOSS_HEIGHT)
        self.speed = BOSS_SPEED
        self.max_health = int(BOSS_HEALTH * health_multiplier)
        self.health = self.max_health
        self.direction = 1
        self.color = RED

    def update(self):
        self.rect.y += int(self.speed)
        self.rect.x += int(self.direction * self.speed * 0.5)
        
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1
        
        return self.rect.bottom < HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        bar_width = self.rect.width
        bar_height = 5
        bar_x = self.rect.x
        bar_y = self.rect.y - 10
        
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

    def take_damage(self):
        self.health -= 1
        return self.health <= 0