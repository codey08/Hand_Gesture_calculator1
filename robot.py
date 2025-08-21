import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
ROBOT_SIZE = 50
SPEED = 5

# Set up some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (255, 0, 0)
# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot")

# Set up the robot
robot_x, robot_y = WIDTH / 2, HEIGHT / 2

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the current key presses
    keys = pygame.key.get_pressed()

    # Move the robot
    if keys[pygame.K_UP]:
        robot_y -= SPEED
    if keys[pygame.K_DOWN]:
        robot_y += SPEED
    if keys[pygame.K_LEFT]:
        robot_x -= SPEED
    if keys[pygame.K_RIGHT]:
        robot_x += SPEED

    # Ensure the robot doesn't move off the screen
    robot_x = max(0, min(robot_x, WIDTH - ROBOT_SIZE))
    robot_y = max(0, min(robot_y, HEIGHT - ROBOT_SIZE))

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, (robot_x, robot_y, ROBOT_SIZE, ROBOT_SIZE))
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(1000 // 60)