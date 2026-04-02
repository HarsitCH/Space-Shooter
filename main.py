import pygame
import sys
import config
from config import *
from game import Game

def main():
    pygame.init()
    config.init_fonts()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Retro Space Shooter - Enhanced Edition")
    clock = pygame.time.Clock()
    pygame.mixer.init()
    
    game = Game()
    running = True
    
    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game.state == MENU:
                    if event.key == pygame.K_RETURN:
                        game.reset_game()
                        game.state = PLAYING
                    elif event.key == pygame.K_d:
                        game.state = DIFFICULTY_SELECT
                
                elif game.state == DIFFICULTY_SELECT:
                    if event.key == pygame.K_1:
                        game.difficulty = 'easy'
                        game.state = MENU
                    elif event.key == pygame.K_2:
                        game.difficulty = 'normal'
                        game.state = MENU
                    elif event.key == pygame.K_3:
                        game.difficulty = 'hard'
                        game.state = MENU
                    elif event.key == pygame.K_ESCAPE:
                        game.state = MENU
                
                elif game.state == PLAYING:
                    if event.key == pygame.K_p:
                        game.state = PAUSED
                
                elif game.state == PAUSED:
                    if event.key == pygame.K_p:
                        game.state = PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        game.state = MENU
                
                elif game.state == GAME_OVER:
                    if event.key == pygame.K_r:
                        game.reset_game()
                        game.state = PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        game.state = MENU
        
        keys = pygame.key.get_pressed()
        
        if game.state == PLAYING:
            game.update_playing(keys)
        
        if game.state == MENU:
            game.draw_menu(screen)
        elif game.state == DIFFICULTY_SELECT:
            game.draw_difficulty_select(screen)
        elif game.state == PLAYING:
            game.draw_playing(screen)
        elif game.state == PAUSED:
            game.draw_playing(screen)
            game.draw_paused(screen)
        elif game.state == GAME_OVER:
            game.draw_game_over(screen)
        
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    
