import pygame
import random
import math
from ball import Ball

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
NUM_BALLS = 10
MIN_RADIUS = 10
MAX_RADIUS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
COLORS = [RED, BLUE]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Distraction Balls Game")

balls = [
    Ball(
        random.randint(MAX_RADIUS, SCREEN_WIDTH - MAX_RADIUS), 
        random.randint(MAX_RADIUS, SCREEN_HEIGHT - MAX_RADIUS), 
        random.choice(COLORS),
        random.randint(MIN_RADIUS, MAX_RADIUS)
    ) 
    for _ in range(NUM_BALLS)
]

running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if 0 < mouse_x < SCREEN_WIDTH and 0 < mouse_y < SCREEN_HEIGHT:
                paused = False
            else:
                paused = True

    if not paused:
        screen.fill(WHITE)
        active_balls = [ball for ball in balls if ball.radius > 0]

        if len(active_balls) <= 1:
            running = False
            continue
        for i, ball in enumerate(balls):
            ball.move()
            for j, other in enumerate(balls):
                if i != j and ball.radius > other.radius:
                    ball.apply_gravity(other)
                    if random.uniform(0, 1) < 0.01 and math.hypot(ball.x - other.x, ball.y - other.y) < (ball.radius + other.radius):
                        ball.eat(other)
            
            if ball.radius > 0:
                ball.draw(screen)

    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()
