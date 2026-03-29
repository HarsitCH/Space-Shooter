import pygame
import sys
import random
import json
import config
from config import *
from player import Player
from game_objects import Bullet, Enemy, Boss
from effects import PowerUp, Particle, Star
from sound import SoundManager

def main():
    pygame.init()
    config.init_fonts()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Retro Space Shooter - Enhanced Edition")
    clock = pygame.time.Clock()
    pygame.mixer.init()
    
    # Simple game state
    state = MENU
    difficulty = 'normal'
    score = 0
    lives = 3
    wave = 1
    high_score = 0
    
    # Load high score
    try:
        import os
        if os.path.exists('high_score.json'):
            with open('high_score.json', 'r') as f:
                high_score = json.load(f).get('high_score', 0)
    except:
        high_score = 0
    
    # Game objects
    player = Player()
    bullets = []
    enemies = []
    stars = [Star() for _ in range(STAR_COUNT)]
    particles = []
    powerups = []
    
    # Timers
    shoot_cooldown = 0
    hit_cooldown = 0
    spawn_timer = 0
    space_pressed = False
    
    def create_explosion(x, y, color):
        for _ in range(15):
            particles.append(Particle(x, y, color))
    
    def spawn_enemy():
        settings = DIFFICULTY_SETTINGS[difficulty]
        
        if wave <= 2:
            enemy_types = ['basic', 'basic', 'zigzag', 'speeder']
        elif wave <= 5:
            enemy_types = ['basic', 'zigzag', 'chaser', 'speeder', 'tank']
        else:
            enemy_types = ['basic', 'zigzag', 'chaser', 'speeder', 'tank', 'tank']
        
        enemy_type = random.choice(enemy_types)
        ex = random.randint(0, WIDTH - ENEMY_WIDTH)
        enemy = Enemy(ex, -ENEMY_HEIGHT, enemy_type, settings['enemy_speed_multiplier'])
        enemy.speed *= random.uniform(0.8, 1.3)
        enemies.append(enemy)
    
    running = True
    while running:
        dt = clock.tick(FPS)
        screen.fill(BLACK)
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if state == MENU:
                    if event.key == pygame.K_RETURN:
                        state = PLAYING
                        score = 0
                        lives = 3
                        wave = 1
                        player = Player()
                        bullets = []
                        enemies = []
                        particles = []
                        powerups = []
                    elif event.key == pygame.K_d:
                        state = DIFFICULTY_SELECT
                
                elif state == DIFFICULTY_SELECT:
                    if event.key == pygame.K_1:
                        difficulty = 'easy'
                        state = MENU
                    elif event.key == pygame.K_2:
                        difficulty = 'normal'
                        state = MENU
                    elif event.key == pygame.K_3:
                        difficulty = 'hard'
                        state = MENU
                    elif event.key == pygame.K_ESCAPE:
                        state = MENU
                
                elif state == PLAYING:
                    if event.key == pygame.K_p:
                        state = PAUSED
                
                elif state == PAUSED:
                    if event.key == pygame.K_p:
                        state = PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        state = MENU
                
                elif state == GAME_OVER:
                    if event.key == pygame.K_r:
                        state = PLAYING
                        score = 0
                        lives = 3
                        wave = 1
                        player = Player()
                        bullets = []
                        enemies = []
                        particles = []
                        powerups = []
                    elif event.key == pygame.K_ESCAPE:
                        state = MENU
        
        keys = pygame.key.get_pressed()
        
        # Update game logic
        if state == PLAYING:
            # Update player
            player.update(keys)
            
            # Update cooldowns
            if shoot_cooldown > 0:
                shoot_cooldown -= 1
            if hit_cooldown > 0:
                hit_cooldown -= 1
            
            # Shooting
            if keys[pygame.K_SPACE] and shoot_cooldown <= 0 and not space_pressed:
                if player.spread_shot_active:
                    for angle in [-15, 0, 15]:
                        bx = player.rect.centerx - BULLET_WIDTH // 2
                        bullets.append(Bullet(bx, player.rect.top, SPREAD_BULLET_SPEED, angle))
                else:
                    bx = player.rect.centerx - BULLET_WIDTH // 2
                    bullets.append(Bullet(bx, player.rect.top))
                shoot_cooldown = SHOOT_COOLDOWN
                space_pressed = True
            elif not keys[pygame.K_SPACE]:
                space_pressed = False
            
            # Update bullets
            bullets = [b for b in bullets if b.update()]
            
            # Spawn enemies
            settings = DIFFICULTY_SETTINGS[difficulty]
            spawn_timer += 1
            spawn_delay = max(20, int(40 * settings['spawn_rate_multiplier']) - (wave // 2))
            
            if spawn_timer >= spawn_delay and len(enemies) < (5 + wave):
                spawn_timer = 0
                spawn_enemy()
            
            # Update enemies
            enemies = [e for e in enemies if e.update(player.rect.centerx)]
            
            # Update particles
            particles = [p for p in particles if p.update()]
            
            # Update stars
            for star in stars:
                star.update()
            
            # Collisions
            for enemy in enemies[:]:
                for bullet in bullets[:]:
                    if enemy.rect.colliderect(bullet.rect):
                        if bullet in bullets:
                            bullets.remove(bullet)
                        enemy.health -= 1
                        if enemy.health <= 0 and enemy in enemies:
                            enemies.remove(enemy)
                            score += enemy.score_value
                            create_explosion(enemy.rect.centerx, enemy.rect.centery, enemy.color)
            
            # Player collisions
            if hit_cooldown == 0:
                for enemy in enemies[:]:
                    if enemy.rect.colliderect(player.rect):
                        if not player.shield_active:
                            enemies.remove(enemy)
                            lives -= 1
                            hit_cooldown = 60
                            create_explosion(player.rect.centerx, player.rect.centery, RED)
                            if lives <= 0:
                                state = GAME_OVER
                                if score > high_score:
                                    high_score = score
                                    try:
                                        with open('high_score.json', 'w') as f:
                                            json.dump({'high_score': high_score}, f)
                                    except:
                                        pass
                        else:
                            enemies.remove(enemy)
                            player.shield_active = False
                            player.shield_timer = 0
                        break
            
            # Update player power-ups
            if player.rapid_fire_timer > 0:
                player.rapid_fire_timer -= 1
                if player.rapid_fire_timer == 0:
                    player.rapid_fire_active = False
            if player.spread_shot_timer > 0:
                player.spread_shot_timer -= 1
                if player.spread_shot_timer == 0:
                    player.spread_shot_active = False
            if player.shield_timer > 0:
                player.shield_timer -= 1
                if player.shield_timer == 0:
                    player.shield_active = False
        
        # Draw
        if state == MENU:
            title = config.title_font.render("RETRO SPACE SHOOTER", True, GREEN)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
            
            instructions = [
                "OBJECTIVE: Destroy all enemies!",
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
        
        elif state == DIFFICULTY_SELECT:
            title = config.title_font.render("SELECT DIFFICULTY", True, GREEN)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
            
            difficulties = [
                ("1 - EASY", "Slower enemies", GREEN),
                ("2 - NORMAL", "Balanced gameplay", YELLOW),
                ("3 - HARD", "Fast enemies", RED)
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
        
        elif state in [PLAYING, PAUSED]:
            # Draw stars
            for star in stars:
                star.draw(screen)
            
            # Draw enemies
            for enemy in enemies:
                enemy.draw(screen)
            
            # Draw bullets
            for bullet in bullets:
                bullet.draw(screen)
            
            # Draw particles
            for particle in particles:
                particle.draw(screen)
            
            # Draw player
            player.draw(screen)
            
            # Draw UI
            score_text = config.font.render(f"SCORE: {score}", True, WHITE)
            lives_text = config.font.render(f"LIVES: {lives}", True, WHITE)
            wave_text = config.font.render(f"WAVE: {wave}", True, WHITE)
            diff_text = config.small_font.render(f"{difficulty.upper()}", True, YELLOW)
            
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (WIDTH - 120, 10))
            screen.blit(wave_text, (10, 40))
            screen.blit(diff_text, (WIDTH - 80, 40))
            
            if state == PAUSED:
                pause_text = config.title_font.render("PAUSED", True, YELLOW)
                resume_text = config.font.render("Press P to Resume", True, WHITE)
                menu_text = config.font.render("Press ESC for Menu", True, WHITE)
                
                screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 50))
                screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 + 20))
                screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 60))
        
        elif state == GAME_OVER:
            over = config.title_font.render("GAME OVER", True, RED)
            final = config.font.render(f"FINAL SCORE: {score}", True, WHITE)
            high = config.font.render(f"HIGH SCORE: {high_score}", True, YELLOW)
            restart = config.font.render("Press R to Restart", True, YELLOW)
            menu = config.font.render("Press ESC for Menu", True, WHITE)
            
            screen.blit(over, (WIDTH // 2 - over.get_width() // 2, 200))
            screen.blit(final, (WIDTH // 2 - final.get_width() // 2, 270))
            screen.blit(high, (WIDTH // 2 - high.get_width() // 2, 300))
            screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 350))
            screen.blit(menu, (WIDTH // 2 - menu.get_width() // 2, 380))
        
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()