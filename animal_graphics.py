
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
CAT_SIZE = 50
SPEED = 5

# Set up some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Graphics")

# Load the cat image
cat_image = pygame.image.load("cat.png")
cat_image = pygame.transform.scale(cat_image, (CAT_SIZE, CAT_SIZE))

# Set up the cat's position
cat_x, cat_y = WIDTH / 2, HEIGHT / 2

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the current key presses
    keys = pygame.key.get_pressed()

    # Move the cat
    if keys[pygame.K_UP]:
        cat_y -= SPEED
    if keys[pygame.K_DOWN]:
        cat_y += SPEED
    if keys[pygame.K_LEFT]:
        cat_x -= SPEED
    if keys[pygame.K_RIGHT]:
        cat_x += SPEED

    # Ensure the cat doesn't move off the screen
    cat_x = max(0, min(cat_x, WIDTH - CAT_SIZE))
    cat_y = max(0, min(cat_y, HEIGHT - CAT_SIZE))

    # Draw everything
    screen.fill(BLACK)
    screen.blit(cat_image, (cat_x, cat_y))
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(1000 // 60)