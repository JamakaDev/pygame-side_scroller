import pygame
from random import randint


from map_data import LEVELS_MAP_DATA 
from settings import *

class MapNode(pygame.sprite.Sprite):
  def __init__(self, position, groups, locked, level_number):
    super().__init__(groups)
    self.locked = locked == 'locked'

    # Creating Surface & Rect
    self.image = pygame.image.load(f'./graphics/map/level_{level_number}.png').convert_alpha()
    self.image = pygame.transform.smoothscale(self.image, (500,200))
    self.rect = self.image.get_rect(center=position)  
  
  def update(self):
    if self.locked:
      tint_surf = self.image.copy()
      tint_surf.fill('black',None,pygame.BLEND_RGBA_MULT)
      self.image.blit(tint_surf,(0,0))

class MapIcon(pygame.sprite.Sprite):
  def __init__(self, position, groups):
    super().__init__(groups)
    self.image = pygame.image.load('./graphics/ninja/Run__003.png').convert_alpha()
    self.image_right = pygame.transform.smoothscale(self.image, (TILE_WIDTH, TILE_HEIGHT))
    self.image_left = pygame.transform.flip(self.image_right, True, False)
    self.image = self.image_right
    self.rect = self.image.get_rect(center=position)
    self.pos = position  
    self.facing_left = False
    
  def update(self):
    self.rect.center = self.pos
    if self.facing_left: self.image = self.image_left
    else: self.image = self.image_right
    

class Map:
  def __init__(self, current_level=0, max_level=0):
    self.display_surface = pygame.display.get_surface()
    
    # Level data
    self.current_level = current_level
    self.max_level = max_level

    # Sprite Groups
    self.node_sprites = pygame.sprite.Group()
    self.icon_sprite = pygame.sprite.GroupSingle()

    # Variables to assist icon movement
    self.allow_input = False
    self.moving = False
    self.moving_direction = pygame.math.Vector2(0,0)
    self.velocity = 5

    self.start_time = pygame.time.get_ticks()
    self.timer_length = 420

    self.draw_map()
    self.draw_paths()
   
  def draw_map(self):
    self.icon = MapIcon(LEVELS_MAP_DATA[self.current_level]['position'],[self.icon_sprite])
    
    for i, node in LEVELS_MAP_DATA.items():
      if i <= self.max_level: 
        MapNode(node['position'], [self.node_sprites], 'unlocked', i)
      else: 
        MapNode(node['position'], [self.node_sprites], 'locked', i)
 
  def draw_paths(self):
    if self.max_level: 
      nodes_positions = [node['position'] for idx, node in LEVELS_MAP_DATA.items() if idx <= self.max_level]
      pygame.draw.lines(self.display_surface, 'navy', False, nodes_positions, 10)    

  def block_user_input(self):
    if not self.allow_input:
      current_time = pygame.time.get_ticks()
      if current_time - self.start_time >= self.timer_length:
        self.start_time = pygame.time.get_ticks()
        self.allow_input = True

  def check_user_input(self):
    keys = pygame.key.get_pressed()

    if not self.moving and self.allow_input:
      if keys[pygame.K_LEFT] and self.current_level > 0: 
        self.moving_direction = self.get_icon_direction('prev')
        self.current_level -= 1
        self.moving = True
      elif keys[pygame.K_RIGHT] and self.current_level < self.max_level:
        self.moving_direction = self.get_icon_direction('next')
        self.current_level += 1
        self.moving = True
      elif keys[pygame.K_RETURN]:
        pass

  def get_icon_direction(self, direction):
    source = pygame.math.Vector2(self.node_sprites.sprites()[self.current_level].rect.center)
    
    if direction == 'next':
      destination = pygame.math.Vector2(self.node_sprites.sprites()[self.current_level+1].rect.center)  
      self.icon.facing_left = False
    else: 
      destination = pygame.math.Vector2(self.node_sprites.sprites()[self.current_level-1].rect.center)
      self.icon.facing_left = True
      
    
    return (destination - source).normalize()

  def move_icon(self):
    if self.moving and self.moving_direction:
      self.icon.pos += self.moving_direction * self.velocity

      icon = pygame.Rect(self.icon.pos, (8,8))
      if icon.collidepoint(self.node_sprites.sprites()[self.current_level].rect.center):
        self.moving_direction = pygame.math.Vector2(0,0)
        self.moving = False       
       
  def update(self, level_number):
    self.current_level = level_number
    self.draw_map()

  def run(self):
    self.block_user_input()
    self.check_user_input()
    self.move_icon()
    
    self.node_sprites.update()
    self.icon_sprite.update()

    self.draw_paths()
    self.node_sprites.draw(self.display_surface)
    self.icon_sprite.draw(self.display_surface)
    




