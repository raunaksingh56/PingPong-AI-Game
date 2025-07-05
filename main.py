import pygame
import random
import numpy as np

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
WHITE = (255, 255, 255)
FPS = 60

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong AI Game")

# Define the paddles and ball
player_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)

# Initialize the ball velocity
ball_dx, ball_dy = random.choice([1, -1]) * 5, random.choice([1, -1]) * 5

# AI parameters (Q-Learning)
Q_table = np.zeros((HEIGHT, 2))  # Height by action space (0: move up, 1: move down)
learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.1  # Exploration rate

# Score variables
player_score = 0
ai_score = 0

def ai_move():
    """AI decision based on Q-learning."""
    global ai_paddle, Q_table
    state = ai_paddle.top

    if random.random() < epsilon:
        action = random.choice([0, 1])  # Exploration: move up (0) or move down (1)
    else:
        action = np.argmax(Q_table[state])  # Exploitation: choose the best action
    
    if action == 0 and ai_paddle.top > 0:
        ai_paddle.move_ip(0, -5)  # Move up
    elif action == 1 and ai_paddle.bottom < HEIGHT:
        ai_paddle.move_ip(0, 5)  # Move down

def update_q_table(reward, new_state, action):
    """Update Q-table using Q-learning formula."""
    global Q_table
    best_future_q = np.max(Q_table[new_state])
    Q_table[state][action] += learning_rate * (reward + discount_factor * best_future_q - Q_table[state][action])

def main():
    global player_score, ai_score, ball_dx, ball_dy, player_paddle, ai_paddle, ball
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill((0, 0, 0))  # Fill the screen with black
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_paddle.top > 0:
                    player_paddle.move_ip(0, -5)
                elif event.key == pygame.K_DOWN and player_paddle.bottom < HEIGHT:
                    player_paddle.move_ip(0, 5)
        
        # Move ball
        ball.x += ball_dx
        ball.y += ball_dy
        
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy = -ball_dy  # Bounce the ball off top and bottom walls
        
        if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
            ball_dx = -ball_dx  # Bounce the ball off paddles
        
        if ball.left <= 0:
            ai_score += 1
            ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)
            ball_dx, ball_dy = random.choice([1, -1]) * 5, random.choice([1, -1]) * 5
        elif ball.right >= WIDTH:
            player_score += 1
            ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)
            ball_dx, ball_dy = random.choice([1, -1]) * 5, random.choice([1, -1]) * 5
        
        ai_move()

        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.rect(screen, WHITE, ai_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        
        # Display score
        font = pygame.font.SysFont('Arial', 30)
        score_text = font.render(f"Player: {player_score} AI: {ai_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
              
