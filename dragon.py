import pygame
from pygame.sprite import Sprite

class Dragon(Sprite):
    # A class to represent a single dragon in the fleet

    def __init__(self, dri_game):
        # Initialize the dragon and set its starting position
        super().__init__()
        self.screen = dri_game.screen
        self.settings = dri_game.settings

        # Load the dragon image and set its rect attribute
        self.image = pygame.image.load('images/dragon.bmp')
        self.rect = self.image.get_rect()

        # Start each new dragon near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the dragon's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        # Return True if the dragon is at the edge of the screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self):
        # Move the dragon to the right or left
        self.x += (self.settings.dragon_speed * self.settings.fleet_direction)
        self.rect.x = self.x
