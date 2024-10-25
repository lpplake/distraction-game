import pygame
import random
import math

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GRAVITY_STRENGTH = 0.1

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
            self.dx = -self.dx
            self.x = max(self.radius, min(self.x, SCREEN_WIDTH - self.radius))
        
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            self.dy = -self.dy
            self.y = max(self.radius, min(self.y, SCREEN_HEIGHT - self.radius))

    def apply_gravity(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            return
        force = GRAVITY_STRENGTH * self.mass * other.mass / distance**2
        self.dx += (force * dx / distance) / self.mass
        self.dy += (force * dy / distance) / self.mass
    
    def eat(self, other):
        self.mass += other.mass
        self.radius = int(self.mass)
        other.mass = 0
        other.radius = 0
        other.dx, other.dy = 0, 0
