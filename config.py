# Game Configuration
import pygame

# Screen
WIDTH, HEIGHT = 480, 640
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 60, 60)
YELLOW = (255, 255, 0)
BLUE = (100, 150, 255)
PURPLE = (200, 100, 255)
ORANGE = (255, 150, 0)

# Font initialization function
def init_fonts():
    global title_font, font, small_font
    title_font = pygame.font.SysFont("consolas", 36)
    font = pygame.font.SysFont("consolas", 20)
    small_font = pygame.font.SysFont("consolas", 16)

# Game States
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
DIFFICULTY_SELECT = 4

# Player
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 20
PLAYER_SPEED = 5

# Bullets
BULLET_WIDTH = 4
BULLET_HEIGHT = 10
BULLET_SPEED = 7
SHOOT_COOLDOWN = 8
SPREAD_BULLET_SPEED = 6

# Enemies
ENEMY_WIDTH = 35
ENEMY_HEIGHT = 20
ENEMY_BASE_SPEED = 2.0
ENEMY_ZIGZAG_SPEED = 2.5
ENEMY_CHASER_SPEED = 1.8
BOSS_WIDTH = 80
BOSS_HEIGHT = 60
BOSS_SPEED = 1.5
BOSS_HEALTH = 20

# Power-ups
POWERUP_WIDTH = 25
POWERUP_HEIGHT = 25
POWERUP_SPEED = 2
POWERUP_TYPES = {
    'rapid_fire': {'color': YELLOW, 'duration': 300},
    'spread_shot': {'color': ORANGE, 'duration': 400},
    'shield': {'color': BLUE, 'duration': 500},
    'extra_life': {'color': GREEN, 'duration': 0}
}

# Particles
PARTICLE_COUNT = 15
PARTICLE_LIFETIME = 30

# Waves
WAVE_ENEMY_COUNT = 5
WAVE_BONUS_SCORE = 50
BOSS_SPAWN_SCORE = 200

# Cooldowns
HIT_COOLDOWN_FRAMES = 60
POWERUP_SPAWN_CHANCE = 0.1

# Visual
STAR_COUNT = 50
SCREEN_SHAKE_DURATION = 10
SCREEN_SHAKE_INTENSITY = 5

# Difficulty
DIFFICULTY_SETTINGS = {
    'easy': {
        'enemy_speed_multiplier': 0.7,
        'spawn_rate_multiplier': 1.3,
        'boss_health_multiplier': 0.7
    },
    'normal': {
        'enemy_speed_multiplier': 1.0,
        'spawn_rate_multiplier': 1.0,
        'boss_health_multiplier': 1.0
    },
    'hard': {
        'enemy_speed_multiplier': 1.5,
        'spawn_rate_multiplier': 0.7,
        'boss_health_multiplier': 1.5
    }
}