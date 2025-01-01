import sys
import pygame
from time import sleep

from settings import Settings
from button import Button
from game_stats import GameStats
from castle import Castle
from bullet import Bullet
from dragon import Dragon

class DragonInvasion:
    def __init__(self):
        # Initialize the game, settings, and screen object.
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Dragon Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.castle = Castle(self)
        self.bullets = pygame.sprite.Group()
        self.dragons = pygame.sprite.Group()

        # Create the initial fleet of dragons.
        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # Set up the clock for frame rate control.
        self.clock = pygame.time.Clock()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.castle.update()
                self._update_bullets()
                self._update_dragons()
            
            self._update_screen()
            self.clock.tick(60)  # Limit the game to 60 frames per second.

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Get rid of any remaining dragons and bullets.
            self.dragons.empty()
            self.bullets.empty()

            # Create a new fleet and center the castle.
            self._create_fleet()
            self.castle.center_castle()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.castle.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.castle.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.castle.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.castle.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        self.bullets.update()

        # Remove bullets that have disappeared off the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_dragon_collisions()

    def _check_bullet_dragon_collisions(self):
        """Respond to bullet-dragon collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.dragons, True, True)

        if not self.dragons:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _create_fleet(self):
        """Create a fleet of dragons."""
        # Create a single dragon to get its dimensions.
        dragon = Dragon(self)
        dragon_width, dragon_height = dragon.rect.size

        # Define the spacing between dragons.
        spacing = 50  # Space between dragons.

        # Calculate how many dragons fit across the screen width.
        available_space_x = self.settings.screen_width - 2 * spacing
        number_dragons_x = available_space_x // (dragon_width + spacing)

        # Calculate how many rows fit on the screen.
        castle_height = self.castle.rect.height  # Assuming a castle object exists.
        available_space_y = self.settings.screen_height - 2 * spacing - castle_height
        number_rows = available_space_y // (dragon_height + spacing)

        # Create the full fleet of dragons.
        for row_number in range(number_rows):
            for dragon_number in range(number_dragons_x):
                self._create_dragon(dragon_number, spacing, row_number)

    def _create_dragon(self, dragon_number, spacing, row_number):
        """Create a dragon and place it in the grid."""
        dragon = Dragon(self)
        dragon_width, dragon_height = dragon.rect.size
        dragon.x = spacing + (dragon_width + spacing) * dragon_number
        dragon.rect.x = dragon.x
        dragon.rect.y = spacing + (dragon_height + spacing) * row_number
        self.dragons.add(dragon)

    def _check_fleet_edges(self):
        """Respond appropriately if any dragons have reached an edge."""
        for dragon in self.dragons.sprites():
            if dragon.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for dragon in self.dragons.sprites():
            dragon.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_dragons(self):
        """Check if the fleet is at an edge, then update the positions of all dragons in the fleet."""
        self._check_fleet_edges()
        self.dragons.update()

        # Look for dragon-castle collisions.
        if pygame.sprite.spritecollideany(self.castle, self.dragons):
            self._castle_hit()

        # Look for dragons hitting the bottom of the screen.
        self._check_dragons_bottom()

    def _castle_hit(self):
        """Respond to the castle being hit by a dragon."""
        if self.stats.castle_left > 0:
            # Decrement castle_left.
            self.stats.castle_left -= 1

            # Get rid of any remaining dragons and bullets.
            self.dragons.empty()
            self.bullets.empty()

            # Create a new fleet and center the castle.
            self._create_fleet()
            self.castle.center_castle()

            # Pause for a brief moment.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_dragons_bottom(self):
        """Check if any dragons have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for dragon in self.dragons.sprites():
            if dragon.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the castle got hit.
                self._castle_hit()
                break

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.castle.blitme()

        # Draw each bullet.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw the dragons.
        self.dragons.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game.
    dri = DragonInvasion()
    dri.run_game()