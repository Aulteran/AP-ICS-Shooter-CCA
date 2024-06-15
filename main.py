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

# sprite groups
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# make sprites
player = Player()
player_group.add(player)

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,250)

game_menu = ['1 - Start Game', '2 - Exit Game']

running = True
game_running = False

while running:

    keyPressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game_running = True
            if event.key == pygame.K_2:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_ESCAPE:
                game_running = not game_running
        
        if game_running:
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     bullet_group.add(player.create_bullet())
            if event.type == ADDENEMY:
                new_enemy = Enemy()
                enemy_group.add(new_enemy)
    
    # show a game menu if game hasn't started
    if not game_running:
        for i in range(len(game_menu)):
            font = pygame.font.Font(None, 36)
            text = font.render(game_menu[i], True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + i*30))
            window.blit(text, text_rect)
        pygame.display.flip()
        continue

    # update sprites if game is running
    if game_running:
        player_group.update()
        bullet_group.update()
        enemy_group.update()

    window.fill((BLACK))
    window.blit(player.surf, player.rect)
    for entity in bullet_group:
        window.blit(entity.surf, entity.rect)

    clock.tick(FPS)

pygame.quit()