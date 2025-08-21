import pygame
import random

# Initialize Pygame
pygame.init()

# Game Window Settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Bird Settings
bird_width = 64
bird_height = 64
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipe Settings
pipe_width = 60
pipe_height = random.randint(100, 400)
pipe_gap = 150
pipe_velocity = 3

# Load images
bird_img = pygame.image.load('bird.png')
bird_img = pygame.transform.scale(bird_img, (bird_width, bird_height))  # Resize the bird image
pipe_img = pygame.image.load('pipe.png')
pipe_img = pygame.transform.scale(pipe_img, (pipe_width, HEIGHT))  # Resize the pipe image

# Font for score
font = pygame.font.SysFont("Arial", 30)

def draw_bird(y):
    screen.blit(bird_img, (bird_x, y))

def draw_pipe(x, height):
    # Top pipe
    screen.blit(pipe_img, (x, 0, pipe_width, height))
    # Bottom pipe
    screen.blit(pipe_img, (x, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap))

def check_collision(bird_rect, pipes):
    for pipe in pipes:
        pipe_rect_top = pygame.Rect(pipe[0], 0, pipe_width, pipe[1])
        pipe_rect_bottom = pygame.Rect(pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT - pipe[1] - pipe_gap)
        if bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    return False

def main():
    global bird_y, bird_velocity
    bird_y = HEIGHT // 2  # Reset bird position
    bird_velocity = 0  # Reset bird velocity
    pipes = []  # List to store pipe positions
    score = 0
    pipe_x = WIDTH

    # Main game loop
    running = True
    while running:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = jump_strength  # Make the bird jump

        # Update bird position
        bird_velocity += gravity
        bird_y += bird_velocity

        # Draw bird
        draw_bird(bird_y)

        # Create and move pipes
        if pipe_x <= 0:
            pipe_x = WIDTH
            pipe_height = random.randint(100, 400)
            pipes.append([pipe_x, pipe_height])

        pipes = [[x - pipe_velocity, h] for x, h in pipes]

        # Draw pipes
        for pipe in pipes:
            draw_pipe(pipe[0], pipe[1])

        # Check for collisions
        bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
        if check_collision(bird_rect, pipes):
            running = False  # End game on collision

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe[0] + pipe_width > 0]

        # Score handling
        for pipe in pipes:
            if pipe[0] + pipe_width == bird_x:  # If the bird passes a pipe
                score += 1

        # Display score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Update display
        pygame.display.update()

        # Frame rate control
        clock.tick(FPS)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
