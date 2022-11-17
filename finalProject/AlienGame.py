import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullets import Bullet
from alien import Alien
from GameStats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienGame:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invaders")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.score = Scoreboard(self)

        self.create_fleet()
        self.play_button = Button(self, "Play")
        #self.background_image = pygame.image.load("space2.png")

    def ship_hit(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self.create_fleet()
            self.ship.center_ship()

            sleep(5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def check_bottom_aliens(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break

    def fleet_edges(self):

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.fleet_direction()
                break

    def fleet_direction(self):

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleetDropSpeed
        self.settings.fleetDirection *= -1

    def create_fleet(self):
        alien = Alien(self)
        width_alien, height_alien = alien.rect.size
        space_x = self.settings.screen_width - (2 * width_alien)
        alienFleet = space_x // (2 * width_alien)

        ship_height = self.ship.rect.height
        space_y = (self.settings.screen_height - (3 * height_alien) - ship_height)
        number_rows = space_y // (2 * height_alien)

        for rows in range(number_rows):
            for alien_amount in range(alienFleet):
                self.create_alien(alien_amount, rows)

    def create_alien(self, alien_amount, rows):
        alien = Alien(self)
        width_alien, height_alien = alien.rect.size
        alien.x = width_alien + 2 * width_alien * alien_amount
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * rows
        self.aliens.add(alien)

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_button(mouse_pos)

    def check_button(self, mouse_pos):

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic()
            self.stats.reset_stats()
            self.stats.game_active = True

            self.aliens.empty()
            self.bullets.empty()
            self.create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
            self.score.prep_score()
            self.score.prep_level()

    def check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullets()

    def check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def fire_bullets(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def updateScreen(self):
        #self.screen.blit(self.background_image, (0, 0))
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.score.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.settings.speed_up()
            self.stats.level += 1
            self.score.prep_level()

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.score.prep_score()
            self.score.check_high_score()

    def update_aliens(self):

        self.fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("SHIP HIT!!!!")
            self.ship_hit()

        self.check_bottom_aliens()

    def run_game(self):

        while True:

            self.checkEvents()

            if self.stats.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
            self.updateScreen()




if __name__ == '__main__':
    ai = AlienGame()
    ai.run_game()