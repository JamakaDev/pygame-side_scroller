import pygame
from math import ceil
from settings import *


class Background(pygame.sprite.Sprite):
  def __init__(self, position, groups, file):
    super().__init__(groups)
    self.image = pygame.image.load(f'./graphics/tileset/BG/{file}.png').convert_alpha()
    self.image = pygame.transform.smoothscale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    self.rect = self.image.get_rect(topleft=position)
    self.hitbox = self.rect


  def update(self, shift):
    self.rect.x += shift


class Bush(pygame.sprite.Sprite):
  def __init__(self, position, groups, file):
    super().__init__(groups)
    self.offset = pygame.math.Vector2(0,TILE_HEIGHT)
    
    self.image = pygame.image.load(f'./graphics/tileset/Object/{file}.png').convert_alpha()
    self.mask = pygame.mask.from_surface(self.image)
    # self.image = pygame.transform.smoothscale(self.image, (TILE_WIDTH, TILE_HEIGHT))

    self.rect = self.image.get_rect(bottomleft=position+self.offset)
    self.hitbox = self.rect


  def update(self, shift):
    self.rect.x += shift


class Crate(pygame.sprite.Sprite):
  def __init__(self, position, groups, file, number):
    super().__init__(groups)
    self.offset = pygame.math.Vector2(0,TILE_HEIGHT)
    
    self.image = pygame.image.load(f'./graphics/tileset/Object/{file}.png').convert_alpha()
    self.mask = pygame.mask.from_surface(self.image)
    self.image = pygame.transform.smoothscale(self.image, (self.image.get_width()//5*3, self.image.get_height()//5*3))
    self.rect = self.image.get_rect(bottomleft=position+self.offset)
    self.hitbox = self.rect


  def update(self, shift):
    self.rect.x += shift


class Mushroom(pygame.sprite.Sprite):
  def __init__(self, position, groups, file):
    super().__init__(groups)
    self.offset = pygame.math.Vector2(0,TILE_HEIGHT)
    
    self.image = pygame.image.load(f'./graphics/tileset/Object/{file}.png').convert_alpha()
    self.image = pygame.transform.smoothscale(self.image, (self.image.get_width()//2, self.image.get_height()//2))
    self.mask = pygame.mask.from_surface(self.image)

    self.rect = self.image.get_rect(bottomleft=position+self.offset)
    self.hitbox = self.rect


  def update(self, shift):
    self.rect.x += shift


class Kunai(pygame.sprite.Sprite):
  def __init__(self, position, groups):
    super().__init__(groups)
    self.offset = pygame.math.Vector2(0,TILE_HEIGHT)

    self.image = pygame.image.load('./graphics/ninja/Kunai.png').convert_alpha()
    self.image = pygame.transform.smoothscale(self.image, (40, 8))
    self.mask = pygame.mask.from_surface(self.image)
    self.rect = self.image.get_rect(bottomleft=position+self.offset)
    self.hitbox = self.rect

  def update(self, shift):
    self.rect.x += shift


class Sign(pygame.sprite.Sprite):
  def __init__(self, position, groups, file):
    super().__init__(groups)
    self.offset = pygame.math.Vector2(0,TILE_HEIGHT)
    
    self.image = pygame.image.load(f'./graphics/tileset/Object/{file}.png').convert_alpha()
    self.mask = pygame.mask.from_surface(self.image)
    # self.image = pygame.transform.smoothscale(self.image, (TILE_WIDTH, TILE_HEIGHT))

    self.rect = self.image.get_rect(bottomleft=position+self.offset)
    self.hitbox = self.rect


  def update(self, shift):
    self.rect.x += shift


class Stone(pygame.sprite.Sprite):
  def __init__(self, position, groups, file):
    super().__init__(groups)
    self.offset = pygame.math.Vector2(0,TILE_HEIGHT)
    
    self.image = pygame.image.load(f'./graphics/tileset/Object/{file}.png').convert_alpha()
    self.mask = pygame.mask.from_surface(self.image)
    # self.image = pygame.transform.smoothscale(self.image, (TILE_WIDTH, TILE_HEIGHT))

    self.rect = self.image.get_rect(bottomleft=position+self.offset)
    self.hitbox = self.rect


  def update(self, shift):
    self.rect.x += shift


class Platform(pygame.sprite.Sprite):
  def __init__(self, position, groups, file):
    super().__init__(groups)
    self.image = pygame.image.load(f'./graphics/tileset/Tiles/{file}.png').convert_alpha()
    self.image = pygame.transform.smoothscale(self.image, (TILE_WIDTH, TILE_HEIGHT))
    self.rect = self.image.get_rect(topleft=position)
    self.hitbox = self.rect
    self.mask = pygame.mask.from_surface(self.image)


  def update(self, shift):
    self.rect.x += shift


class Tree(pygame.sprite.Sprite):
  def __init__(self, position, groups, file, offset_x=0):
    super().__init__(groups)
    
    self.offset = pygame.math.Vector2(offset_x, TILE_HEIGHT)
    
    self.image = pygame.image.load(f'./graphics/tileset/Object/{file}.png').convert_alpha()

    self.rect = self.image.get_rect(bottomleft=position+self.offset)
    self.hitbox = self.rect


  def update(self, shift):
    self.rect.x += shift


class Water(pygame.sprite.Sprite):
  def __init__(self, position, groups, index):
    super().__init__(groups)
 
    # Index for the frame animation
    self.frame_index = index
    
    # List of images/surfaces to create the wave animation
    self.images = [pygame.image.load(f'./graphics/tileset/Water/{i}.png').convert_alpha() for i in range(1,5)]
    self.image = self.images[self.frame_index]
    self.mask = pygame.mask.from_surface(self.image)
    
    #  Image Rect & hitbox for movement
    self.rect = self.image.get_rect(topleft=position) 
    

  # Applying the animation of the waves
  def apply_waves(self): 
    self.image = self.images[ceil(self.frame_index)%4]
    self.frame_index += (ANIMATION_SPEED*.25)
    if self.frame_index > 1_000_000_000: self.frame_index %= 4

  # Override on the update method
  def update(self, shift):
    self.apply_waves()
    self.rect.x += shift
  

