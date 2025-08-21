import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
ANIMAL_SIZE = 20
FOOD_SIZE = 10
FOOD_SIZE = 10
OBSTACLE_SIZE = 30
SPEED = 5

# Set up some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Game")

# Set up the animal, food, and obstacles
animal_x, animal_y = WIDTH / 2, HEIGHT / 2
food_x, food_y = random.randint(0, WIDTH - FOOD_SIZE), random.randint(0, HEIGHT - FOOD_SIZE)
obstacles = [(random.randint(0, WIDTH - OBSTACLE_SIZE), random.randint(0, HEIGHT - OBSTACLE_SIZE)) for _ in range(5)]

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the current key presses
    keys = pygame.key.get_pressed()

    # Move the animal
    if keys[pygame.K_UP]:
        animal_y -= SPEED
    if keys[pygame.K_DOWN]:
        animal_y += SPEED
    if keys[pygame.K_LEFT]:
        animal_x -= SPEED
    if keys[pygame.K_RIGHT]:
        animal_x += SPEED

    # Ensure the animal doesn't move off the screen
    animal_x = max(0, min(animal_x, WIDTH - ANIMAL_SIZE))
    animal_y = max(0, min(animal_y, HEIGHT - ANIMAL_SIZE))

    # Check for collision with food
    if (animal_x, animal_y) == (food_x, food_y):
        food_x, food_y = random.randint(0, WIDTH - FOOD_SIZE), random.randint(0, HEIGHT - FOOD_SIZE)

    # Check for collision with obstacles
    for obstacle in obstacles:
        if (animal_x, animal_y) == obstacle:
            pygame.quit()
            sys.exit()

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, (animal_x, animal_y, ANIMAL_SIZE, ANIMAL_SIZE))
    pygame.draw.rect(screen, WHITE, (food_x, food_y, FOOD_SIZE, FOOD_SIZE))
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], OBSTACLE_SIZE, OBSTACLE_SIZE))
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(1000 // 60)