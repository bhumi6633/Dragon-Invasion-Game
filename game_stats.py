from pygame.sprite import Sprite

class GameStats:
  #Track statistics for dragon Invasion.

    def __init__(self, dri_game):
        #Initialize statistics.
        self.settings = dri_game.settings
        self.reset_stats()

        # Start Dragon Invasion in an active state.
        self.game_active = True
        
        # Start game in an inactive state.
        self.game_active = False

    def reset_stats(self):
        #Initialize statistics that can change during the game.
        self.castle_left = self.settings.castle_limit