import pygame
import os

from settings import *

class Player(pygame.sprite.Sprite):
  def __init__(self, position, groups, obstacle_sprites, enemy_sprites):
    super().__init__(groups)
    # Variables
    self.attacking = False
    self.attack_frame = 0
    self.current_action = 'idle'
    self.direction = pygame.math.Vector2()
    self.display_surface = pygame.display.get_surface()
    self.facing_right = True
    self.image_frame = 0
    self.jumping = False
    self.jump_frame = 0
    self.recovering = False
    self.reset_position = position
    self.state = 'normal'
    self.velocity = 3
    

    # Storing all of the player surfaces for use in movement
    self.all_images = [pygame.image.load(f'./graphics/ninja/{file}').convert_alpha() for file in os.listdir('graphics/ninja')]
    self.all_images = [pygame.transform.smoothscale(surf, (TILE_WIDTH,TILE_HEIGHT)) for surf in self.all_images]    
    
    # self.all_images_damaged = [pygame.image.load(f'./graphics/ninja/{file}').convert_alpha() for file in os.listdir('graphics/ninja')]
    self.all_images_damaged = [pygame.transform.smoothscale(surf, (TILE_WIDTH,TILE_HEIGHT)) for surf in self.all_images]    
    for image in self.all_images_damaged:
      tint_surf = image.copy()
      tint_surf.fill('red', None, pygame.BLEND_RGBA_MULT)
      image.blit(tint_surf, (0,0))

    self.animations = {
      'normal' : {
        'attack_right': [pygame.transform.smoothscale(surf, (TILE_WIDTH,TILE_HEIGHT-8)) for surf in self.all_images[:10]],
        'attack_left': [pygame.transform.flip(surf, flip_x=True, flip_y=False) for surf in [pygame.transform.smoothscale(surf, (TILE_WIDTH,TILE_HEIGHT-8)) for surf in self.all_images[:10]]],
        'dead': self.all_images[10:20],
        'idle_left': [pygame.transform.smoothscale(surf, (TILE_WIDTH,TILE_HEIGHT-12)) for surf in self.all_images[20:30]],
        'idle_right': [pygame.transform.smoothscale(surf, (TILE_WIDTH-24,TILE_HEIGHT-12)) for surf in self.all_images[30:40]],
        'jump_attack': self.all_images[40:50],
        'jump_right': [pygame.transform.smoothscale(surf, (TILE_WIDTH-12,TILE_HEIGHT)) for surf in self.all_images[50:60]],
        'jump_left': [pygame.transform.flip(surf, flip_x=True, flip_y=False) for surf in [pygame.transform.smoothscale(surf, (TILE_WIDTH-12,TILE_HEIGHT-12)) for surf in self.all_images[50:60]]],
        'jump_throw': self.all_images[60:70],
        'run_right': [pygame.transform.smoothscale(surf, (TILE_WIDTH-24,TILE_HEIGHT-12)) for surf in self.all_images[71:81]],
        'run_left': [pygame.transform.flip(surf, flip_x=True, flip_y=False) for surf in [pygame.transform.smoothscale(surf, (TILE_WIDTH-24,TILE_HEIGHT-12)) for surf in self.all_images[71:81]]],
        'slide': self.all_images[81:91],
        'throw': self.all_images[91:]
      },
      'damage' : {
        'attack_right': [pygame.transform.smoothscale(surf, (TILE_WIDTH,TILE_HEIGHT-8)) for surf in self.all_images_damaged[:10]],
        'attack_left': [pygame.transform.flip(surf, flip_x=True, flip_y=False) for surf in [pygame.transform.smoothscale(surf, (TILE_WIDTH,TILE_HEIGHT-8)) for surf in self.all_images_damaged[:10]]],
        'dead': self.all_images_damaged[10:20],
        'idle_left': [pygame.transform.smoothscale(surf, (TILE_WIDTH,TILE_HEIGHT-12)) for surf in self.all_images_damaged[20:30]],
        'idle_right': [pygame.transform.smoothscale(surf, (TILE_WIDTH-24,TILE_HEIGHT-12)) for surf in self.all_images_damaged[30:40]],
        'jump_attack': self.all_images_damaged[40:50],
        'jump_right': [pygame.transform.smoothscale(surf, (TILE_WIDTH-12,TILE_HEIGHT)) for surf in self.all_images_damaged[50:60]],
        'jump_left': [pygame.transform.flip(surf, flip_x=True, flip_y=False) for surf in [pygame.transform.smoothscale(surf, (TILE_WIDTH-24,TILE_HEIGHT-12)) for surf in self.all_images_damaged[50:60]]],
        'jump_throw': self.all_images_damaged[60:70],
        'run_right': [pygame.transform.smoothscale(surf, (TILE_WIDTH-24,TILE_HEIGHT-12)) for surf in self.all_images_damaged[71:81]],
        'run_left': [pygame.transform.flip(surf, flip_x=True, flip_y=False) for surf in [pygame.transform.smoothscale(surf, (TILE_WIDTH-24,TILE_HEIGHT-12)) for surf in self.all_images_damaged[71:81]]],
        'slide': self.all_images_damaged[81:91],
        'throw': self.all_images_damaged[91:]
      }
    }

    # The player surface/mask/rect for movement
    self.image = self.animations[self.state][self.current_action+'_right'][0]
    self.mask = pygame.mask.from_surface(self.image)
    self.rect = self.image.get_rect(topleft=position)
    self.hitbox = self.rect

    # Health & weapon
    self.health = 100
    self.kunai_total = 0
    
    # Sprites the player can collide with
    self.obstacle_sprites = obstacle_sprites
    self.enemy_sprites = enemy_sprites

  def apply_gravity(self):
    self.direction.y += GRAVITY
    self.rect.y += self.direction.y
  
  def check_player_input(self):
    keys = pygame.key.get_pressed()
    pressed = any(keys)
    action = self.current_action

    # Check for movement/actions
    if keys[pygame.K_LEFT]:
      self.direction.x = -1
      self.facing_right = False
      if keys[pygame.K_a] and not self.direction.y:
        self.direction.x = 0
        action = 'attack'
        self.image = self.animations[self.state][action+'_left'][int(self.attack_frame)]
        self.attacking = True
      else:
        action = 'run'
        self.image = self.animations[self.state][action+'_left'][int(self.image_frame)]
    elif keys[pygame.K_RIGHT]:
      self.direction.x = 1
      self.facing_right = True
      if keys[pygame.K_a] and not self.direction.y:
        self.direction.x = 0 
        action = 'attack'
        self.image = self.animations[self.state][action+'_right'][int(self.attack_frame)]
        self.attacking = True
      else:
        action = 'run'
        self.image = self.animations[self.state][action+'_right'][int(self.image_frame)]
    elif keys[pygame.K_a]: 
        self.direction.x = 0
        action = 'attack'
        if self.facing_right: self.image = self.animations[self.state][action+'_right'][int(self.attack_frame)] 
        else: self.image = self.animations[self.state][action+'_left'][int(self.attack_frame)]
        self.attacking = True
    else: 
      self.direction.x = 0


    if keys[pygame.K_SPACE] and not self.jumping:
      action = 'jump'
      if self.facing_right: self.image = self.animations[self.state][action+'_right'][int(self.jump_frame)] 
      else: self.image = self.animations[self.state][action+'_left'][int(self.jump_frame)]
      self.jump()
    
    self.image_frame += ANIMATION_SPEED
    if self.image_frame > 9: self.image_frame = 0

    self.jump_frame += ANIMATION_SPEED
    if self.jump_frame > 9: self.jump_frame = 0

    self.attack_frame += ANIMATION_SPEED
    if self.attack_frame > 9: self.attack_frame = 0

    self.mask = pygame.mask.from_surface(self.image)
    self.current_action = action

    if not keys[pygame.K_a]: self.attacking = False
    
    return pressed

  def jump(self):
    self.jumping = True
    self.direction.y += JUMP_VEL

  def reset(self, checkpoint_position):
    self.rect.bottomleft = checkpoint_position
    
  def update(self):
    if not self.check_player_input() and not self.jumping and not self.attacking: 
      action = self.current_action = 'idle'
      if self.facing_right: self.image = self.animations[self.state][action+'_right'][int(self.image_frame)]
      else: self.image = self.animations[self.state][action+'_left'][int(self.image_frame)]
