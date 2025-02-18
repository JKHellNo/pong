import pygame
import random
import sys

if __name__ == "__main__":
    if sys.platform == "emscripten":
        print("Running in browser")
        
# Initialize the game
pygame.init()

# Set up the display
FRAMES = 60
WIDTH, HEIGHT = 700, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")    
surface=pygame.display.get_surface()
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Initialize the score and set up font/size of the score
PLAYER_SCORE, AI_SCORE = 0, 0  
FONT_SIZE = 74
font = pygame.font.Font(None, FONT_SIZE)

# Define colors
WHITE = (255, 255, 255)

# Set up the game clock
clock = pygame.time.Clock()

# Set up the ball
BALL_RADIUS = 28  
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5 
ball_speed_y = 5 
ball_speedup = 0 
RESET_POSITION = False

ball_dx = random.choice([-ball_speed_x, ball_speed_x])    #constant speed but random left/right direction
ball_dy = random.randint(-ball_speed_y, ball_speed_y)     #random speed and random up/down direction

# ball animation
ball_sprite_sheet = pygame.image.load("hadoken.png")
frame_width, frame_height = 310, 53
current_ball_direction = "right"
frame_length_width = 4            #how many images from left to right
frame_length_height = 1           #how many images from the top to the bottom
frame_width_offset, frame_height_offset = -39, -25    #image to circle object offset
frame_width = frame_width / frame_length_width
frame_height = frame_height / frame_length_height
frames = []

# frame per second of the ball animation
desired_frame_rate = 6  
frame_switch_interval = int(FRAMES / desired_frame_rate)
frame_counter = 0
current_frame_index = 0

for j in range(frame_length_height):    #splits the image into rows
    for i in range(frame_length_width):  #splits the image into columns
        frame_rect = pygame.Rect(i * frame_width, j * frame_height, frame_width, frame_height)
        frame = ball_sprite_sheet.subsurface(frame_rect)
        frames.append(frame)

# Set up the paddles
player_paddle_image = pygame.image.load("player_paddle.png")
ai_paddle_image = pygame.image.load("ai_paddle.png")
PADDLE_WIDTH, PADDLE_HEIGHT = 25,  110 
PLAYER_PADDLE_SPEED= 10 
AI_PADDLE_SPEED = 4.52 
AI_CENTERING = PADDLE_HEIGHT // 3
WALL_DISTANCE = WIDTH / 25 
player_paddle_image = pygame.transform.scale(player_paddle_image, (PADDLE_WIDTH, PADDLE_HEIGHT))
ai_paddle_image = pygame.transform.scale(ai_paddle_image, (PADDLE_WIDTH, PADDLE_HEIGHT))
player_paddle = pygame.Rect(WALL_DISTANCE, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT) # x y width height
ai_paddle = pygame.Rect(WIDTH - WALL_DISTANCE - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Set up the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.y > 0:   
        player_paddle.y -= PLAYER_PADDLE_SPEED
    if keys[pygame.K_s] and player_paddle.y < HEIGHT - PADDLE_HEIGHT:   
        player_paddle.y += PLAYER_PADDLE_SPEED

    # Fun little feature to cheat against the AI
    if keys[pygame.K_r]:
        player_paddle.width += 4
        player_paddle.height +=13
        player_paddle_image = pygame.transform.scale(player_paddle_image, (player_paddle.width, player_paddle.height))
    
    # Move the AI paddle
    if ai_paddle.y - AI_CENTERING + PADDLE_HEIGHT // 2 < ball_y:    #Lines itself up to the ball
        ai_paddle.y += AI_PADDLE_SPEED 
    if ai_paddle.y + AI_CENTERING + PADDLE_HEIGHT // 2 > ball_y:
        ai_paddle.y -= AI_PADDLE_SPEED 

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Inside the game loop
    frame_counter += 1
    if frame_counter >= frame_switch_interval:
        current_frame_index = (current_frame_index + 1) % len(frames)
        frame_counter = 0
    current_frame = frames[current_frame_index]

    # Check for ball collision with paddles, velocity handles collision glitch detection
    if player_paddle.collidepoint(ball_x, ball_y) and ball_dx < 0:
        ball_dx = -ball_dx + ball_speedup
        ball_dy = random.choice([-ball_speed_y, ball_speed_y])
    elif ai_paddle.collidepoint(ball_x, ball_y) and ball_dx > 0:    
        ball_dx = -ball_dx - ball_speedup
        ball_dy = random.choice([-ball_speed_y+2, ball_speed_y-2])

    #Recenters the ball to the center of the screen
    if RESET_POSITION:  
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = random.choice([-ball_speed_x, ball_speed_x])
        ball_dy = random.choice([-ball_speed_y, ball_speed_y])
        RESET_POSITION = False    

    #handles the image direction of the ball
    if ball_dx < 0:
        ball_direction = "left"
    else:
        ball_direction = "right"

    # Flip the ball image if it changes direction          
    if current_ball_direction != ball_direction:
        current_ball_direction = ball_direction
        for i in range(len(frames)):
            frames[i] = pygame.transform.flip(frames[i], True, False)

    # Check for ball collision with walls
    if ball_y < 0 or ball_y > HEIGHT - BALL_RADIUS:
        ball_dy *= -1

    # Check for ball going out of bounds
    if ball_x < 0:   #AI Wins
        AI_SCORE += 1
        RESET_POSITION=True
    elif ball_x > WIDTH:   #Player Wins
        PLAYER_SCORE += 1
        RESET_POSITION=True

    # Clear the screen
    WIN.blit(background_image, (0, 0))

    #Draw the ball
    WIN.blit(current_frame, (ball_x+frame_width_offset, ball_y+frame_height_offset))  #ball with image
    #pygame.draw.circle(WIN, WHITE, (ball_x, ball_y), BALL_RADIUS) #the ball that handles collision(not rendered, good for debugging)

    #Draw the paddles
    WIN.blit(player_paddle_image, player_paddle)
    WIN.blit(ai_paddle_image, ai_paddle)

    # Draw the score
    player_text = font.render(f"{PLAYER_SCORE}", True, WHITE)
    ai_text = font.render(f"{AI_SCORE}", True, WHITE)
    TEXT_WIDTH, TEXT_HEIGHT=250, 10
    WIN.blit(player_text, (TEXT_WIDTH, TEXT_HEIGHT))
    WIN.blit(ai_text, (WIDTH - TEXT_WIDTH, TEXT_HEIGHT))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FRAMES)

# Quit the game
pygame.quit()