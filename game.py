import pygame
import random
import json
import os
import config
from config import *
from player import Player
from game_objects import Bullet, Enemy, Boss
from effects import PowerUp, Particle, Star
from sound import SoundManager

class Game:
    def __init__(self):
        self.state = MENU
        self.score = 0
        self.lives = 3
        self.high_score = 0
        self.difficulty = 'normal'
        self.sound_manager = SoundManager()
        self.load_high_score()
        self.reset_playing()

    def load_high_score(self):
        try:
            if os.path.exists('high_score.json'):
                with open('high_score.json', 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
        except:
            self.high_score = 0

    def save_high_score(self):
        try:
            with open('high_score.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass

    def reset_playing(self):
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.boss = None
        self.powerups = []
        self.particles = []
        self.stars = [Star() for _ in range(STAR_COUNT)]
        self.spawn_timer = 0
        self.shoot_cooldown = 0
        self.hit_cooldown = 0
        self.wave_number = 1
        self.enemies_in_wave = WAVE_ENEMY_COUNT
        self.wave_complete = False
        self.screen_shake_timer = 0
        self.screen_shake_offset = [0, 0]
        self.boss_spawned = False
        self.space_pressed = False

    def reset_game(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.score = 0
        self.lives = 3
        self.wave_number = 1
        self.boss_spawned = False
        self.reset_playing()

    def create_explosion(self, x, y, color):
        for _ in range(PARTICLE_COUNT):
            self.particles.append(Particle(x, y, color))

    def apply_screen_shake(self):
        self.screen_shake_timer = SCREEN_SHAKE_DURATION

    def update_screen_shake(self):
        if self.screen_shake_timer > 0:
            self.screen_shake_timer -= 1
            self.screen_shake_offset = [
                random.randint(-SCREEN_SHAKE_INTENSITY, SCREEN_SHAKE_INTENSITY),
                random.randint(-SCREEN_SHAKE_INTENSITY, SCREEN_SHAKE_INTENSITY)
            ]
        else:
            self.screen_shake_offset = [0, 0]

    def spawn_enemy(self):
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        
        # Simplified enemy distribution for better performance
        if self.wave_number <= 2:
            enemy_types = ['basic', 'basic', 'zigzag', 'speeder']
        elif self.wave_number <= 5:
            enemy_types = ['basic', 'zigzag', 'chaser', 'speeder', 'tank']
        else:
            enemy_types = ['basic', 'zigzag', 'chaser', 'speeder', 'tank', 'tank']
        
        enemy_type = random.choice(enemy_types)
        
        # Random spawn position with bias towards edges sometimes
        if random.random() < 0.3:  # 30% chance to spawn at edges
            if random.random() < 0.5:
                ex = random.randint(0, WIDTH // 4)
            else:
                ex = random.randint(3 * WIDTH // 4, WIDTH - ENEMY_WIDTH)
        else:
            ex = random.randint(0, WIDTH - ENEMY_WIDTH)
        
        # Random initial Y position for more variety
        initial_y = random.randint(-ENEMY_HEIGHT - 50, -ENEMY_HEIGHT)
        
        enemy = Enemy(ex, initial_y, enemy_type, 
                     settings['enemy_speed_multiplier'])
        
        # Add random speed variation
        enemy.speed *= random.uniform(0.8, 1.3)
        
        self.enemies.append(enemy)

    def spawn_boss(self):
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        bx = WIDTH // 2 - BOSS_WIDTH // 2
        self.boss = Boss(bx, -BOSS_HEIGHT, settings['boss_health_multiplier'])
        self.boss_spawned = True

    def update_playing(self, keys):
        # Update screen shake
        self.update_screen_shake()

        # Decrement cooldowns
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Player movement
        self.player.update(keys)

        # Shooting with power-ups - requires key release between shots
        shoot_cooldown = SHOOT_COOLDOWN
        if self.player.rapid_fire_active:
            shoot_cooldown = shoot_cooldown // 2

        # Only shoot on initial key press, not hold
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            if self.space_pressed == False:  # New key press
                if self.player.spread_shot_active:
                    # Spread shot - 3 bullets
                    for angle in [-15, 0, 15]:
                        bx = self.player.rect.centerx - BULLET_WIDTH // 2
                        self.bullets.append(Bullet(bx, self.player.rect.top, SPREAD_BULLET_SPEED, angle))
                else:
                    # Normal shot
                    bx = self.player.rect.centerx - BULLET_WIDTH // 2
                    self.bullets.append(Bullet(bx, self.player.rect.top))
                self.sound_manager.play_sound('shoot')
                self.shoot_cooldown = shoot_cooldown
                self.space_pressed = True
        elif not keys[pygame.K_SPACE]:
            self.space_pressed = False  # Reset when key is released

        # Update bullets
        self.bullets = [b for b in self.bullets if b.update()]

        # Wave-based spawning
        if not self.boss_spawned:
            settings = DIFFICULTY_SETTINGS[self.difficulty]
            self.spawn_timer += 1
            spawn_delay = max(20, int(40 * settings['spawn_rate_multiplier']) - (self.wave_number // 2))
            
            if self.spawn_timer >= spawn_delay and len(self.enemies) < self.enemies_in_wave:
                self.spawn_timer = 0
                self.spawn_enemy()

            # Check wave completion
            if len(self.enemies) == 0 and not self.wave_complete:
                self.wave_complete = True
                self.score += WAVE_BONUS_SCORE
                self.wave_number += 1
                self.enemies_in_wave = min(WAVE_ENEMY_COUNT + self.wave_number * 2, 15)

            # Spawn boss at certain score
            if self.score >= BOSS_SPAWN_SCORE * (1 if not self.boss_spawned else 2):
                self.spawn_boss()

        # Update enemies
        self.enemies = [e for e in self.enemies if e.update(self.player.rect.centerx)]

        # Update boss
        if self.boss:
            if not self.boss.update():
                self.boss = None
                self.boss_spawned = False
                self.score += 100

        # Update power-ups
        self.powerups = [p for p in self.powerups if p.update()]

        # Update particles
        self.particles = [p for p in self.particles if p.update()]

        # Update stars
        for star in self.stars:
            star.update()

        # Bullet-enemy collisions
        for enemy in self.enemies[:]:
            for bullet in self.bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    
                    # Handle enemy health (for tanks)
                    enemy.health -= 1
                    if enemy.health <= 0:
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                        self.score += enemy.score_value
                        self.create_explosion(enemy.rect.centerx, enemy.rect.centery, enemy.color)
                        self.sound_manager.play_sound('explosion')
                        self.apply_screen_shake()
                        
                        # Chance to spawn power-up
                        if random.random() < POWERUP_SPAWN_CHANCE:
                            self.powerups.append(PowerUp(enemy.rect.centerx - POWERUP_WIDTH // 2, 
                                                       enemy.rect.centery))
                    break

        # Bullet-boss collisions
        if self.boss is not None:
            for bullet in self.bullets[:]:
                if self.boss.rect.colliderect(bullet.rect):
                    self.bullets.remove(bullet)
                    if self.boss.take_damage():
                        self.create_explosion(self.boss.rect.centerx, self.boss.rect.centery, RED)
                        self.sound_manager.play_sound('explosion')
                        self.apply_screen_shake()
                        self.boss = None
                        self.boss_spawned = False
                        self.score += 100
                        break

        # Player-enemy collisions
        if self.hit_cooldown == 0:
            for enemy in self.enemies[:]:
                if enemy.rect.colliderect(self.player.rect):
                    if not self.player.shield_active:
                        self.enemies.remove(enemy)
                        self.lives -= 1
                        self.hit_cooldown = HIT_COOLDOWN_FRAMES
                        self.create_explosion(self.player.rect.centerx, self.player.rect.centery, RED)
                        self.sound_manager.play_sound('hit')
                        self.apply_screen_shake()
                        if self.lives <= 0:
                            self.state = GAME_OVER
                            if self.score > self.high_score:
                                self.high_score = self.score
                                self.save_high_score()
                    else:
                        # Shield blocks damage
                        self.enemies.remove(enemy)
                        self.player.shield_active = False
                        self.player.shield_timer = 0
                    break
        
        # Player-enemy bullet collisions (from shooter enemies)
        if self.hit_cooldown == 0:
            for enemy in self.enemies:
                if enemy.type == 'shooter':
                    for bullet in enemy.bullets[:]:
                        if bullet.rect.colliderect(self.player.rect):
                            if not self.player.shield_active:
                                enemy.bullets.remove(bullet)
                                self.lives -= 1
                                self.hit_cooldown = HIT_COOLDOWN_FRAMES
                                self.create_explosion(self.player.rect.centerx, self.player.rect.centery, RED)
                                self.sound_manager.play_sound('hit')
                                self.apply_screen_shake()
                                if self.lives <= 0:
                                    self.state = GAME_OVER
                                    if self.score > self.high_score:
                                        self.high_score = self.score
                                        self.save_high_score()
                            else:
                                # Shield blocks damage
                                enemy.bullets.remove(bullet)
                                self.player.shield_active = False
                                self.player.shield_timer = 0
                            break

        # Player-boss collisions
        if self.boss and self.hit_cooldown == 0:
            if self.boss.rect.colliderect(self.player.rect):
                if not self.player.shield_active:
                    self.lives -= 1
                    self.hit_cooldown = HIT_COOLDOWN_FRAMES
                    self.create_explosion(self.player.rect.centerx, self.player.rect.centery, RED)
                    self.sound_manager.play_sound('hit')
                    self.apply_screen_shake()
                    if self.lives <= 0:
                        self.state = GAME_OVER
                        if self.score > self.high_score:
                            self.high_score = self.score
                            self.save_high_score()
                else:
                    self.player.shield_active = False
                    self.player.shield_timer = 0

        # Player-powerup collisions
        for powerup in self.powerups[:]:
            if powerup.rect.colliderect(self.player.rect):
                if powerup.type == 'extra_life':
                    self.lives += 1
                else:
                    self.player.activate_powerup(powerup.type)
                self.sound_manager.play_sound('powerup')
                self.powerups.remove(powerup)

    def draw_menu(self, screen):
        title = config.title_font.render("RETRO SPACE SHOOTER", True, GREEN)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        instructions = [
            "OBJECTIVE:",
            "Destroy all enemies and bosses!",
            "",
            "CONTROLS:",
            "← → Move Ship",
            "SPACE Fire",
            "P Pause",
            "",
            "Press ENTER to Play",
            "Press D for Difficulty"
        ]
        y = 180
        for line in instructions:
            text = config.font.render(line, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
            y += 25

    def draw_difficulty_select(self, screen):
        title = config.title_font.render("SELECT DIFFICULTY", True, GREEN)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

        difficulties = [
            ("1 - EASY", "Slower enemies, more health", GREEN),
            ("2 - NORMAL", "Balanced gameplay", YELLOW),
            ("3 - HARD", "Fast enemies, less health", RED)
        ]

        y = 250
        for key, desc, color in difficulties:
            key_text = config.font.render(key, True, color)
            desc_text = config.small_font.render(desc, True, WHITE)
            screen.blit(key_text, (WIDTH // 2 - key_text.get_width() // 2, y))
            screen.blit(desc_text, (WIDTH // 2 - desc_text.get_width() // 2, y + 25))
            y += 70

        back_text = config.font.render("Press ESC to go back", True, WHITE)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, 500))

    def draw_paused(self, screen):
        pause_text = config.title_font.render("PAUSED", True, YELLOW)
        resume_text = config.font.render("Press P to Resume", True, WHITE)
        menu_text = config.font.render("Press ESC for Menu", True, WHITE)
        
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 + 20))
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 60))

    def draw_playing(self, screen):
        # Apply screen shake offset
        shake_offset_x, shake_offset_y = self.screen_shake_offset

        # Create a surface for game content
        game_surface = pygame.Surface((WIDTH, HEIGHT))
        game_surface.fill(BLACK)

        # Background stars
        for star in self.stars:
            star.draw(game_surface)

        # Enemies
        for enemy in self.enemies:
            enemy.draw(game_surface)

        # Boss
        if self.boss:
            self.boss.draw(game_surface)

        # Power-ups
        for powerup in self.powerups:
            powerup.draw(game_surface)

        # Particles
        for particle in self.particles:
            particle.draw(game_surface)

        # Bullets
        for bullet in self.bullets:
            bullet.draw(game_surface)

        # Player
        self.player.draw(game_surface)

        # Blit game surface to screen with shake offset
        screen.blit(game_surface, (shake_offset_x, shake_offset_y))

        # UI (draw without shake)
        score_text = config.font.render(f"SCORE: {self.score}", True, WHITE)
        lives_text = config.font.render(f"LIVES: {self.lives}", True, WHITE)
        wave_text = config.font.render(f"WAVE: {self.wave_number}", True, WHITE)
        difficulty_text = config.small_font.render(f"{self.difficulty.upper()}", True, YELLOW)
        
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 120, 10))
        screen.blit(wave_text, (10, 40))
        screen.blit(difficulty_text, (WIDTH - 80, 40))

        # Power-up indicators
        y_offset = 70
        if self.player.rapid_fire_active:
            rf_text = config.small_font.render(f"RAPID FIRE: {self.player.rapid_fire_timer // 60 + 1}s", True, YELLOW)
            screen.blit(rf_text, (10, y_offset))
            y_offset += 20
        if self.player.spread_shot_active:
            ss_text = config.small_font.render(f"SPREAD SHOT: {self.player.spread_shot_timer // 60 + 1}s", True, ORANGE)
            screen.blit(ss_text, (10, y_offset))
            y_offset += 20
        if self.player.shield_active:
            sh_text = config.small_font.render(f"SHIELD: {self.player.shield_timer // 60 + 1}s", True, BLUE)
            screen.blit(sh_text, (10, y_offset))

    def draw_game_over(self, screen):
        over = config.title_font.render("GAME OVER", True, RED)
        final = config.font.render(f"FINAL SCORE: {self.score}", True, WHITE)
        high = config.font.render(f"HIGH SCORE: {self.high_score}", True, YELLOW)
        restart = config.font.render("Press R to Restart", True, YELLOW)
        menu = config.font.render("Press ESC for Menu", True, WHITE)
        
        screen.blit(over, (WIDTH // 2 - over.get_width() // 2, 200))
        screen.blit(final, (WIDTH // 2 - final.get_width() // 2, 270))
        screen.blit(high, (WIDTH // 2 - high.get_width() // 2, 300))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 350))
        screen.blit(menu, (WIDTH // 2 - menu.get_width() // 2, 380))
