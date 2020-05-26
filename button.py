import pygame


# Class Definitions
class Button:
    def __init__(self, colour, x, y, width, height):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, [self.x, self.y, self.width, self.height])

    # Function Definition : Text on Button
    def draw_text(self, screen, color, text='CHANGE PHASE'):
        font = pygame.font.Font('freesansbold.ttf', 14)
        text = font.render(text, True, color)
        textRect = text.get_rect()
        textRect.center = (self.x + self.width/2, self.y + self.height/2)
        screen.blit(text, textRect)
