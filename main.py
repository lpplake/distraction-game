import math
import pygame
import random
# import math
import threading
from concurrent.futures import ThreadPoolExecutor
from ball import Ball
# import time
import concurrent

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
NUM_BALLS = 50
MIN_RADIUS = 10
MAX_RADIUS = 30
GRAVITY = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
COLORS = [RED, BLUE]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Realistic Pool-Like Ball Simulation")

def initializing(num_balls, screen_width, screen_height, min_radius, max_radius):
    balls = []
    while len(balls) < num_balls:
        new_ball = Ball(
            random.randint(max_radius, screen_width - max_radius),
            random.randint(max_radius, screen_height - max_radius),
            random.choice(COLORS),
            random.randint(min_radius, max_radius)
        )

        # Check for overlaps with existing balls
        overlap = False
        for existing_ball in balls:
            dx = existing_ball.x - new_ball.x
            dy = existing_ball.y - new_ball.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance < existing_ball.radius + new_ball.radius:
                overlap = True
                break

        # Only add the ball if there's no overlap
        if not overlap:
            balls.append(new_ball)
    
    return balls

balls = initializing(NUM_BALLS, SCREEN_WIDTH, SCREEN_HEIGHT, MIN_RADIUS, MAX_RADIUS)


THREAD_POOL_SIZE = 6
ball_lock = threading.Lock()

running = True
paused = False

def update_ball(ball, all_balls):
    with ball_lock:
        ball.move(all_balls)
        for other_ball in all_balls:
            if ball != other_ball:
                ball.check_collision(other_ball)
                # if collide :
                    # ball.move(all_balls)

                
                

def run():
    global running, paused

    with ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE) as executor:
        while running:
            if paused:
                continue

            screen.fill(WHITE)

            futures = [executor.submit(update_ball, ball, balls) for ball in balls]

            concurrent.futures.wait(futures)

            with ball_lock:
                for ball in balls:
                    ball.draw(screen)

            pygame.display.flip()
            pygame.time.delay(10)

        executor.shutdown(wait=True)

    print("Simulation thread terminated.")

def main():
    global running, paused

    simulation_thread = threading.Thread(target=run)
    simulation_thread.start()

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

    simulation_thread.join()
    pygame.quit()

if __name__ == "__main__":
    main()
