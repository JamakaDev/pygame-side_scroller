import pygame
from random import randint
from settings import *


class Enemy(pygame.sprite.Sprite):
  def __init__(self, postion, groups, file, obstacle_sprites):
    super().__init__(groups)
    self.offset = pygame.math.Vector2(0,TILE_HEIGHT)
    self.images_right = [pygame.transform.smoothscale(surf, (TILE_WIDTH, TILE_HEIGHT)) for surf in [pygame.image.load(f'./graphics/enemies/male/{file}_{i}.png').convert_alpha() for i in range(10)]]
    self.images_left = [pygame.transform.flip(surf, True, False) for surf in self.images_right]
    self.images_attack_right = [pygame.transform.smoothscale(surf, (TILE_WIDTH, TILE_HEIGHT)) for surf in [pygame.image.load(f'./graphics/enemies/male/Attack_{i}.png').convert_alpha() for i in  range(1,9)]]
    self.images_attack_left = [pygame.transform.flip(surf, flip_x=True, flip_y=False) for surf in self.images_attack_right]
    self.image = self.images_left[0]
    self.mask  = pygame.mask.from_surface(self.image)
    self.rect = self.image.get_rect(bottomleft=postion+self.offset)
    self.rect.inflate_ip(-24,0)
    self.hitbox = self.rect.inflate(self.rect.width*8,0)
    self.image_frame = 0
    self.attack_frame = 0
    self.walk_count = 0
    self.facing_right = False
    self.falling = False
    self.attacking = False
    self.direction = pygame.math.Vector2()
    self.obstacle_sprites = obstacle_sprites
    # self.outline = sorted(self.mask.outline(), key=lambda coord: coord[0])[-10:]
  def apply_gravity(self):
    self.direction.y += GRAVITY
    self.rect.y += self.direction.y
    self.hitbox.y += self.direction.y

  def attack(self, direction):
    if not direction:
      self.attacking = True
      if self.facing_right: self.image = self.images_attack_right[int(self.attack_frame)] 
      else: self.image = self.images_attack_left[int(self.attack_frame)]
      self.mask = pygame.mask.from_surface(self.image)
      return
    if direction < 0: self.facing_right = False
    if direction > 0: self.facing_right = True      
    self.rect.x += direction
    self.hitbox.x += direction
    
    self.image = self.images_right[int(self.image_frame)] if self.facing_right else self.images_left[int(self.image_frame)]
    self.mask = pygame.mask.from_surface(self.image)
    
  def horizontal_collision(self):
    for obstacle in self.obstacle_sprites:
      if pygame.sprite.collide_rect(self, obstacle):
        self.falling = False
        if self.facing_right:
          self.direction.x = -1
          self.facing_right = False
        else:
          self.direction.x = 1
          self.facing_right = True
   
  def update(self, shift, player):
    self.vertical_collision()
    self.horizontal_collision()
    if self.falling: self.apply_gravity()
    self.rect.x += shift
    self.hitbox.x += shift
    self.image_frame += ANIMATION_SPEED
    if self.image_frame >= 10: self.image_frame = 0
    self.attack_frame += ANIMATION_SPEED
    if self.attack_frame >= 8: self.attack_frame = 0

    if self.hitbox.colliderect(player.rect):
      if self.rect.collidepoint(player.rect.center): self.attack(0)
      elif player.rect.center < self.rect.center: self.attack(-1)
      elif player.rect.center >  self.rect.center: self.attack(1)
    else: self.walk()
  
  def vertical_collision(self):
    for obstacle in self.obstacle_sprites:
      if obstacle.rect.collidepoint(self.rect.midbottom):
        if self.direction.y > 0:
          self.falling = False
          self.rect.bottom = obstacle.hitbox.top
          self.hitbox.center = self.rect.center
          self.direction.y = 0
      else:
        self.falling = True

  def walk(self):
    self.walk_count = self.walk_count+1 if self.walk_count < 1_000_000 else 0
    if self.walk_count % 128 == 0: self.facing_right = not self.facing_right
    if self.facing_right: 
      self.image = self.images_right[int(self.image_frame)]
      direction = 1
    else: 
      self.image = self.images_left[int(self.image_frame)]
      direction = -1
    self.rect.x += direction
    self.hitbox.x += direction

    self.mask = pygame.mask.from_surface(self.image)

  

