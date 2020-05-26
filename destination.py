import pygame


class Destination:

    def __init__(self, x, y, color, width=22, image=None, image_path=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.image_path = image_path

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x * self.y)

    def draw(self, screen):
        if self.image:
            screen.blit(pygame.transform.scale(self.image, (self.width, self.width)),
                        (self.x - self.width / 2, self.y - self.width / 2))
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.width)
