import pygame


class Obstacle:

    def __init__(self, x, y, color, width=1):
        self.color = color
        self.x = x
        self.y = y
        self.width = width

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x * self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.width)



