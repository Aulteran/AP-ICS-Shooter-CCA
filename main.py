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

class Player (pygame.sprite.Sprite):
  def __init__(self):
      super(Player, self).__init__()
      self.image = pygame.image.load('soldier.png').convert()
      self.image.set_colorkey((WHITE), RLEACCEL)
      self.image = pygame.transform.scale(self.image, (60,60))
      self.rect = self.image.get_rect()
      self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT-100)
      self.hp = 100
  def update(self, game_running):
      if game_running:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)

      # add boundary checking to make sure player doesn't go off screen
      if self.rect.left < 0:
          self.rect.left = 0
      if self.rect.right > WINDOW_WIDTH:
          self.rect.right = WINDOW_WIDTH
      if self.rect.top <= 0:
          self.rect.top = 0
      if self.rect.bottom >= WINDOW_HEIGHT:
          self.rect.bottom = WINDOW_HEIGHT

      # add collision detection
      if pygame.sprite.spritecollide(self, enemy_group, True):
          self.hp -= 10
          print('Player HP:', self.hp)
          if self.hp <= 0:
              print('Game Over')
              pygame.quit()
              sys.exit()

class Bullet (pygame.sprite.Sprite):
  def __init__(self, pos_x, pos_y):
      super(Bullet, self).__init__()
      self.image = pygame.image.load('bullet.png').convert()
      self.image = pygame.transform.scale(self.image, (10,10))
      self.image.set_colorkey((WHITE), RLEACCEL)
      self.rect = self.image.get_rect(center = (pos_x, pos_y))

  def update (self):
      self.rect.y -= 5
      if self.rect.y > WINDOW_HEIGHT:
          self.kill()

class Enemy(pygame.sprite.Sprite):
  def __init__(self):
    super(Enemy,self).__init__()
    self.image_variants = ['ship_boomerang_icon.png', 'ship_boomerang_pirate.png', 'ship_boomerang_shield.png', 'ship_boomerang_zom.png', 'ship_boomerang.png']
    self.image = pygame.image.load(self.image_variants[random.randint(0,4)]).convert()
    self.image = pygame.transform.scale(self.image, (50,50))
    self.image.set_colorkey(WHITE, RLEACCEL)
    self.rect = self.image.get_rect(center = (random.randint(0,WINDOW_WIDTH), random.randint(-100,0)))
    self.speed = random.randint(5,20)

  def update(self):
    self.rect.move_ip(0,self.speed)
    if self.rect.bottom > WINDOW_HEIGHT:
      self.kill()
    
    # add collision detection to break enemy bullets when hit by self bullet
    if pygame.sprite.spritecollide(self, bullet_group, True):
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
first_run = True

while running:
    window.fill(BLACK)

    if first_run:
      player_group.update(game_running)
      player_group.draw(window)

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
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.centery)
                bullet_group.add(bullet)
        # if the game is running, add sprites at intervals
        if game_running:
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

    # update sprites if game is running
    if game_running:
        player_group.update(game_running)
        player_group.draw(window)
        bullet_group.update()
        bullet_group.draw(window)
        enemy_group.update()
        enemy_group.draw(window)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()