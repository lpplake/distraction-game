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

balls = [
    Ball(
        random.randint(MAX_RADIUS, SCREEN_WIDTH - MAX_RADIUS), 
        random.randint(MAX_RADIUS, SCREEN_HEIGHT - MAX_RADIUS), 
        random.choice(COLORS),
        random.randint(MIN_RADIUS, MAX_RADIUS)
    ) 
    for _ in range(NUM_BALLS)
]

THREAD_POOL_SIZE = 6
ball_lock = threading.Lock()

running = True
paused = False

def update_ball(ball, all_balls):
    with ball_lock:
        ball.move()
        for other_ball in all_balls:
            if ball != other_ball:
                colllide = ball.check_collision(other_ball)
                if not colllide :
                    ball.handle_soft_bump(other_ball)
                
                

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
