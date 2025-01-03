class Settings:
    # A class to store all settings for Dragon Invasion

    def __init__(self):
        # Initialize the game's settings

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (151, 157, 204)  # Light lavender and blue background

        # Bullet settings
        self.bullet_speed = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Castle settings
        self.castle_speed = 3
        self.castle_limit = 3

        # Dragon settings
        self.dragon_speed = 1.0
        self.fleet_drop_speed = 10  # Increased for better visibility
        # Fleet direction: 1 represents right, -1 represents left
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # Initialize settings that change throughout the game
        self.castle_speed = 1.5
        self.bullet_speed = 3.0
        self.dragon_speed = 1.0
        # Fleet direction: 1 represents right, -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        # Increase speed settings
        self.castle_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.dragon_speed *= self.speedup_scale
