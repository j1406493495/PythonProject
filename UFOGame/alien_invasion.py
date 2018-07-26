import sys
import pygame

from settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    pygame.init()

    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Woong Invasion")

    ship = Ship(screen, ai_settings)

    # 开始游戏主循环
    while True:
        gf.check_events(ship)
        ship.update()
        gf.update_screen(ai_settings, screen, ship)

        # 让最新绘制的屏幕可见
        pygame.display.flip()


run_game()
