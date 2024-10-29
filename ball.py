import pygame
import random
import math

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GRAVITY_STRENGTH = 0.1
COEFFICIENT_OF_RESTITUTION = 0.9
MAX_SPEED = 5  # Cap the maximum speed 
INITIAL_SPEED = 3

class Ball:
    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = radius
        angle = random.uniform(0, 2 * math.pi)
        self.dx = INITIAL_SPEED * math.cos(angle)
        self.dy = INITIAL_SPEED * math.sin(angle)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self, all_balls):
        self.x += self.dx
        self.y += self.dy
        
        if self.x - self.radius < 0:
            self.dx = abs(self.dx) * COEFFICIENT_OF_RESTITUTION
            self.x = self.radius
        elif self.x + self.radius > SCREEN_WIDTH:
            self.dx = -abs(self.dx) * COEFFICIENT_OF_RESTITUTION
            self.x = SCREEN_WIDTH - self.radius

        if self.y - self.radius < 0:
            self.dy = abs(self.dy) * COEFFICIENT_OF_RESTITUTION
            self.y = self.radius
        elif self.y + self.radius > SCREEN_HEIGHT:
            self.dy = -abs(self.dy) * COEFFICIENT_OF_RESTITUTION
            self.y = SCREEN_HEIGHT - self.radius

        for other_ball in all_balls:
            if self != other_ball:
                self.resolve_overlap(other_ball)
                # self.check_collision(other_ball)

    def limit_speed(self):
        speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if speed > MAX_SPEED:
            scaling_factor = MAX_SPEED / speed
            self.dx *= scaling_factor
            self.dy *= scaling_factor

    def check_collision(self, other) -> bool:
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance <= self.radius + other.radius:
            nx = dx / distance
            ny = dy / distance

            dvx = self.dx - other.dx
            dvy = self.dy - other.dy
            velocity_along_normal = dvx * nx + dvy * ny

            if velocity_along_normal > 0:
                return False
            impulse = (-(1 + COEFFICIENT_OF_RESTITUTION) * velocity_along_normal) / (1 / self.mass + 1 / other.mass)
            # impulse = ((1 + COEFFICIENT_OF_RESTITUTION) * velocity_along_normal) / (1 / self.mass + 1 / other.mass)

            # self.dx =  - self.dx * (impulse / self.mass) * nx
            # self.dy = - self.dy *(impulse / self.mass) * ny
            # other.dx = -self.dx(impulse / other.mass) * nx
            # other.dy = -self.dy(impulse / other.mass) * ny
            self.dx -=  (impulse / self.mass) * nx
            self.dy -= (impulse / self.mass) * ny
            other.dx += (impulse / other.mass) * nx
            other.dy += (impulse / other.mass) * ny

            self.limit_speed()
            other.limit_speed()
            return True
        return False

    def resolve_overlap(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < self.radius + other.radius:
            overlap = (self.radius + other.radius) - distance
            nx = dx / distance
            ny = dy / distance

            self.x -= nx * overlap / 2 
            self.y -= ny * overlap / 2 
            other.x += nx * overlap / 2
            other.y += ny * overlap / 2


            # dvx = self.dx - other.dx
            # dvy = self.dy - other.dy
            # velocity_along_normal = dvx * nx + dvy * ny

            # if velocity_along_normal > 0:
            #     return False
            # impulse = (-(1 + COEFFICIENT_OF_RESTITUTION) * velocity_along_normal) / (1 / self.mass + 1 / other.mass)

            # self.dx -= (impulse / self.mass) * nx
            # self.dy -= (impulse / self.mass) * ny
            # other.dx += (impulse / other.mass) * nx
            # other.dy += (impulse / other.mass) * ny

            # self.limit_speed()
            # other.limit_speed()
            



