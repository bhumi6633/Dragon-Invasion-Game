import pygame

class Castle:  # A class to manage the castle

    def __init__(self, dri_game):  # Initialize the castle and set its starting position
        self.screen = dri_game.screen
        self.settings = dri_game.settings
        self.screen_rect = dri_game.screen.get_rect()

        # Load the castle image and get its rect
        self.image = pygame.image.load('images/castle.bmp')
        self.rect = self.image.get_rect()

        # Start each new castle at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the castle's horizontal position
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def center_castle(self):
        #Center the castle on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):  # Update the castle position based on the movement flags
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.castle_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.castle_speed

    def blitme(self):
        # Draw the castle at its current location
        self.screen.blit(self.image, self.rect)
