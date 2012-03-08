# By Nick Chen
import pygame, sys

def quit():
    sys.exit(0)
    pygame.quit()

def replay(winner):
    screen.fill(BLACK)
    font = pygame.font.SysFont("Times New Roman", 20)
    msg = font.render("Player %d wins! Press space to play again, esc to quit"
                      % winner, True, WHITE)
    screen.blit(msg, ((SCREEN_WIDTH / 2)/ 2, SCREEN_HEIGHT / 2)) 
    pygame.display.flip()
    again = True
    while again == True:
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                again = False
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                quit()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# (x, y) Coordinates
PADDLE_ONE_START = (10,  SCREEN_HEIGHT / 2)
PADDLE_TWO_START = (780, SCREEN_HEIGHT / 2)
PADDLE_W = 10
PADDLE_H = 100
DIVIDER_WIDTH = 2
DIVIDER_HEIGHT = SCREEN_HEIGHT
BALL_SPEED = 10
BALL_W_H = 16
BALL_DEF_POS = (SCREEN_WIDTH / 2 - BALL_W_H / 2, SCREEN_HEIGHT / 2)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Rect that contains the ball. Default pos = center of the screen
ball_rect = pygame.Rect(BALL_DEF_POS, (BALL_W_H, BALL_W_H))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_one_rect = pygame.Rect(PADDLE_ONE_START, (PADDLE_W, PADDLE_H))

# Player 2 paddle
paddle_two_rect = pygame.Rect(PADDLE_TWO_START, (PADDLE_W, PADDLE_H))

# Central divider
divider = pygame.Rect((SCREEN_WIDTH / 2 - 1, 0), (DIVIDER_WIDTH, DIVIDER_HEIGHT))

# Scoring: 1 point if you hit the ball 
p1_score = 0
p2_score = 0

# Ball delay
counter = 0
delay = 100

# Load the font for displaying the p1_score
font = pygame.font.SysFont("Times New Roman", 30)

# Game loop
while True:
    # Check for a win.  Scores are reset here because otherwise they are not
    # preserved across the function call (...?)
    if p1_score >= 11:
        p1_score = 0
        p2_score = 0
        replay(1)
    if p2_score >= 11:
        p1_score = 0
        p2_score = 0
        replay(2)

    # Event handler
    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
            quit()

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
    	sys.exit(0)
    	pygame.quit()

    # This tests if up or down keys are pressed; if yes, move the paddle
    if pygame.key.get_pressed()[pygame.K_w] and paddle_one_rect.top > 0:
    	paddle_one_rect.top -= BALL_SPEED

    elif pygame.key.get_pressed()[pygame.K_s] and \
         paddle_one_rect.bottom < SCREEN_HEIGHT:
    	paddle_one_rect.top += BALL_SPEED

    if ((paddle_two_rect.top + paddle_two_rect.bottom)/2) > ball_rect.top:
        paddle_two_rect.top -= BALL_SPEED
    elif ((paddle_two_rect.top + paddle_two_rect.bottom)/2) < ball_rect.top:
        paddle_two_rect.top += BALL_SPEED

    if pygame.key.get_pressed()[pygame.K_UP] and \
       paddle_two_rect.top > 0:
    	paddle_two_rect.top -= BALL_SPEED

    elif pygame.key.get_pressed()[pygame.K_DOWN] and \
         paddle_two_rect.bottom < SCREEN_HEIGHT:
    	paddle_two_rect.top += BALL_SPEED
    	
    # Update ball position
    if counter < 100:
        counter = counter + 1
    else:
        ball_rect.left += ball_speed[0]
        ball_rect.top += ball_speed[1]

    # Ball collision with borders
    if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
    	ball_speed[1] = -ball_speed[1]

    if ball_rect.right >= SCREEN_WIDTH:
        ball_rect.left = BALL_DEF_POS[0]
        ball_rect.top = BALL_DEF_POS[1]
        ball_speed = [BALL_SPEED, BALL_SPEED]
    	p1_score += 1
        counter = 0

    elif ball_rect.left <= 0:
        ball_rect.left = BALL_DEF_POS[0]
        ball_rect.top = BALL_DEF_POS[1]
        ball_speed = [-BALL_SPEED, -BALL_SPEED]
    	p2_score += 1
        counter = 0

    # Test if the ball is hit by the paddle; if yes reverse speed 
    if paddle_one_rect.colliderect(ball_rect):
    	ball_speed[0] = -ball_speed[0]
        sys.stdout.write(chr(7))
    if paddle_two_rect.colliderect(ball_rect):
    	ball_speed[0] = -ball_speed[0]
        sys.stdout.write(chr(7))
    
    # Clear screen
    screen.fill(BLACK)

    # Render the ball, paddles, and score
    pygame.draw.rect(screen, WHITE, divider)
    pygame.draw.rect(screen, WHITE, paddle_one_rect) 
    pygame.draw.rect(screen, WHITE, paddle_two_rect)

    # The ball
    pygame.draw.circle(screen, WHITE, ball_rect.center, ball_rect.width / 2) 

    # The p1_score
    p1_score_text = font.render(str(p1_score), True, WHITE)
    screen.blit(p1_score_text, ((SCREEN_WIDTH / 4) - \
                                font.size(str(p1_score))[0] / 2, 5)) 

    # The p2_score
    p2_score_text = font.render(str(p2_score), True, WHITE)
    screen.blit(p2_score_text, ((SCREEN_WIDTH * 3 / 4) - \
                                font.size(str(p2_score))[0] / 2, 5)) 
    
    # Update screen and wait 20 milliseconds
    pygame.display.flip()
    pygame.time.delay(20)
