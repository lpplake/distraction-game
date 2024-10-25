import pygame
import random
import math

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GRAVITY_STRENGTH = 0.1
COEFFICIENT_OF_RESTITUTION = 0.9  
MAX_SPEED = 5  # Cap the maximum speed 

class Ball:
    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = radius  
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-5, 5)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.dx = -self.dx * COEFFICIENT_OF_RESTITUTION
            self.x = max(self.radius, min(self.x, SCREEN_WIDTH - self.radius)) 

        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            self.dy = -self.dy * COEFFICIENT_OF_RESTITUTION
            self.y = max(self.radius, min(self.y, SCREEN_HEIGHT - self.radius))  

        self.limit_speed()

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

        if distance < self.radius + other.radius:
            nx = dx / distance
            ny = dy / distance

            dvx = self.dx - other.dx
            dvy = self.dy - other.dy

            velocity_along_normal = dvx * nx + dvy * ny

            if velocity_along_normal > 0:
                return False

            impulse = (-(1 + COEFFICIENT_OF_RESTITUTION) * velocity_along_normal) / (1 / self.mass + 1 / other.mass)

            self.dx -= (impulse / self.mass) * nx
            self.dy -= (impulse / self.mass) * ny
            other.dx += (impulse / other.mass) * nx
            other.dy += (impulse / other.mass) * ny

            self.limit_speed()
            other.limit_speed()
            return True

    def handle_soft_bump(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if self.radius + other.radius > distance > self.radius + other.radius * 0.95:
            self.dx *= 0.98
            self.dy *= 0.98
            other.dx *= 0.98
            other.dy *= 0.98
