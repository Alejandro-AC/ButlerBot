import pygame


class Wall:

    def __init__(self, x1, y1, x2, y2, color, width=1):
        self.color = color
        self.point1 = (x1, y1)
        self.point2 = (x2, y2)
        self.width = width

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.point1, self.point2)



