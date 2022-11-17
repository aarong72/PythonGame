class Settings:

    def __init__(self):

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (100, 100, 200)

        self.bullet_speed = 7
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 6

        self.ship_limit = 3

        self.alien_speed = 1.0
        self.fleetDropSpeed = 10
        self.fleetDirection = 1

        self.speedUp_scale = 1.1
        self.initialize_dynamic()

    def initialize_dynamic(self):
        self.bullet_speed = 2
        self.alien_speed = 2.0
        self.fleetDirection = 1
        self.alien_points = 50

    def speed_up(self):
        self.bullet_speed *= self.speedUp_scale
        self.alien_speed *= self.speedUp_scale