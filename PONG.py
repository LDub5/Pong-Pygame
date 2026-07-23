import pygame
import sys
import random
import time

# 1. Initialize Pygame
pygame.init()

# 2. Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Variables
player1_y = 250
player2_y = 250
keys = pygame.key.get_pressed()
ball_speed_x = 5
ball_speed_y = 5
ball_x = 390
ball_y = random.randint(0, 585)
player1_score = 0
player2_score = 0
score_font = pygame.font.Font("PressStart2P.ttf", 43) 
ball_waiting = False
respawn_time = 0

# 3. Set up the game clock
clock = pygame.time.Clock()
FPS = 60

# 4. Main Game Loop
running = True
while running:
    # 5. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 6. Game Logic Updates
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_y > 0:
        player1_y = player1_y - 5
    if keys[pygame.K_s] and player1_y < 510:
        player1_y = player1_y + 5
    if keys[pygame.K_UP] and player2_y > 0:
        player2_y = player2_y - 5
    if keys[pygame.K_DOWN] and player2_y < 510:
        player2_y = player2_y + 5
    
    left_paddle = pygame.Rect(30, player1_y, 15, 90)
    right_paddle = pygame.Rect(755, player2_y, 15, 90)
    
    # Move the ball
    if ball_waiting and pygame.time.get_ticks() > respawn_time:
        ball_x = 390
        ball_y = 290
        ball_speed_x = random.choice([-5, 5]) 
        ball_speed_y = random.choice([-5, 5]) 
        ball_waiting = False

    ball_x += ball_speed_x
    ball_y += ball_speed_y
    if ball_y <= 0 or ball_y >=585:
        ball_speed_y = ball_speed_y * -1
        
    # Score
    if ball_x < 0 and not ball_waiting:
        player2_score += 1
        ball_waiting = True
        respawn_time = pygame.time.get_ticks() + 1000 
        ball_x = -100  
        ball_speed_x = 0
        ball_speed_y = 0

    if ball_x > 800 and not ball_waiting:
        player1_score += 1
        ball_waiting = True
        respawn_time = pygame.time.get_ticks() + 1000 
        ball_x = -100 
        ball_speed_x = 0
        ball_speed_y = 0
    
    
       # Create the ball
    ball_rect = pygame.Rect(ball_x, ball_y, 15, 15)
    
    # Left Paddle Collision
    if ball_rect.colliderect(left_paddle) and ball_speed_x < 0:
        ball_speed_x = ball_speed_x * -1.05  
        ball_speed_y = ball_speed_y * 1.05
        
        # Right Speed Limit
        if ball_speed_x > 10: ball_speed_x = 10
        if ball_speed_y > 10: ball_speed_y = 10
        if ball_speed_y < -10: ball_speed_y = -10

    # Right Paddle Collision
    if ball_rect.colliderect(right_paddle) and ball_speed_x > 0:
        ball_speed_x = ball_speed_x * -1.01  
        ball_speed_y = ball_speed_y * 1.01
        
        # Left Speed Limit
        if ball_speed_x < -7: ball_speed_x = -7
        if ball_speed_y > 7: ball_speed_y = 7
        if ball_speed_y < -7: ball_speed_y = -7

    # 7. Drawing and Rendering
    screen.fill((0, 0, 0))  # Clear screen with black background
    pygame.draw.rect(screen, (255, 255, 255), left_paddle) # Draw left paddle
    pygame.draw.rect(screen, (255, 255, 255), right_paddle) # Draw right paddle
    pygame.draw.rect(screen, (255, 255, 255), ball_rect) # Draw ball
    p1_surface = score_font.render(str(player1_score), False, (255, 255, 255)) # Render P1 Score
    p2_surface = score_font.render(str(player2_score), False, (255, 255, 255)) # Render P2 Score
    screen.blit(p1_surface, (200, 30))  # P1 Score
    screen.blit(p2_surface, (580, 30))  # P2 Score
    
    if player1_score == 11:
        screen.fill((128, 0, 0))
        game_over = score_font.render("Player 1 Victory!", True, (255, 255, 255))
        text_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over, text_rect)
        running = False
    
    if player2_score == 11:
        screen.fill((128, 0, 0))
        game_over = score_font.render("Player 2 Victory!", True, (255, 255, 255))
        text_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over, text_rect)
        running = False
        
    # 8. Flip the display
    pygame.display.flip()

    # 9. Maintain Frame Rate
    clock.tick(FPS)

# 10. Clean up and exit
time.sleep(3)
pygame.quit()
sys.exit()
