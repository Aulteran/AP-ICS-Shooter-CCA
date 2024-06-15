import random
import pygame, sys
from pygame.locals import *
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 480
WINDOW_WIDTH = 480
FPS = 30

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

class Player (pygame.sprite.Sprite):
  def __init__(self):
      super(Player, self).__init__()
      self.surf = pygame.image.load('soldier.png').convert()
      self.surf.set_colorkey((WHITE), RLEACCEL)
      self.rect = self.surf.get_rect()


  def update (self):
      self.rect.center = pygame.mouse.get_pos()

  def create_bullet (self):
      return Bullet(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

class Bullet (pygame.sprite.Sprite):
  def __init__(self, pos_x, pos_y):
      super(Bullet, self).__init__()
      self.surf = pygame.image.load('bullet.png').convert()
      self.surf.set_colorkey((WHITE), RLEACCEL)
      self.rect = self.surf.get_rect(center = (pos_x, pos_y))

  def update (self):
      self.rect.y += -5
      if self.rect.y > WINDOW_HEIGHT:
          self.kill()

class Enemy(pygame.sprite.Sprite):
  def __init__(self):
    super(Enemy,self).__init__()
    self.surf = pygame.image.load('enemy_bullet.png').convert()
    self.surf.set_colorkey(WHITE, RLEACCEL)
    self.rect = self.surf.get_rect(center = (random.randint(0,WINDOW_WIDTH), random.randint(-100,0)))
    self.speed = random.randint(5,20)

  def update(self):
    self.rect.move_ip(0,self.speed)
    if self.rect.bottom > WINDOW_HEIGHT:
      self.kill()

player = Player()

running = True

player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
bullet_group = pygame.sprite.Group()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,250)

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet_group.add(player.create_bullet())

        if event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    player.update()
    enemies.update()

    window.fill((BLACK))
    window.blit(player.surf, player.rect)
    for entity in bullet_group:
        window.blit(entity.surf, entity.rect)
    for entity in all_sprites:
        window.blit(entity.surf,entity.rect)
    player_group.update()
    bullet_group.update()

    if pygame.sprite.spritecollideany(player,enemies):
        player.kill()
        pygame.time.delay(500)
        running = False
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()