import sys
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ship, ai_settings, screen, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


# 监听键盘和鼠标事件
def check_events(ship, ai_settings, screen, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, ai_settings, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


# 每次循环时都重会背景
def update_screen(ai_settings, screen, ship, aliens, bullets):
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()


# 更新子弹的位置，并删除已消失的子弹
def update_bullets(ai_settings, screen, ship, aliens, bullets):
    # 更新子弹的位置 bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, aliens)


def create_fleet(ai_settings, screen, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算每行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    # 创建第一行外星人
    for alien_number in range(number_aliens_x):
        create_alien(ai_settings, screen, aliens, alien_number)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    aliens.add(alien)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
        ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens):
    """ 检查是否有外星人位于屏幕边缘，并更新整群外星人的位置 """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
