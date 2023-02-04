import pygame
import sys
from random import randint

from settings import *
from level_utils import *
from enemy import Enemy
from player import Player
from tiles import Background, Bush, Crate, Mushroom, Kunai, Sign, Stone, Platform, Tree, Water


class Level():
  def __init__(self, level_number=0):
    self.display_surface = pygame.display.get_surface()
    self.current_level = level_number
    self.background_shift = 0
    self.timer_length = 3000
    self.start_time = pygame.time.get_ticks()

    # Background & HUD Sprite Groups
    self.background_sprites = pygame.sprite.Group()
    self.hud_sprites = pygame.sprite.Group()

    # Player & winning object Sprite Groups
    self.player_sprite = pygame.sprite.GroupSingle()
    self.win_sprite = pygame.sprite.GroupSingle()
    self.kunai_sprites = pygame.sprite.Group()
    
    # Terrain Sprite Groups
    self.bush_sprites = pygame.sprite.Group()
    self.crate_sprites = pygame.sprite.Group()
    self.mushroom_sprites = pygame.sprite.Group()
    self.platform_sprites = pygame.sprite.Group()
    self.sign_sprites = pygame.sprite.Group()
    self.stone_sprites = pygame.sprite.Group()
    self.tree_sprites = pygame.sprite.Group()
    self.water_sprites = pygame.sprite.Group()
    
    # Collidable Sprite Group
    self.checkpoint_sprite = pygame.sprite.GroupSingle()
    self.obstacle_sprites = pygame.sprite.Group()
    
    # Enemy Sprite Groups
    self.enemy_sprites = pygame.sprite.Group()
    self.enemy_list = pygame.sprite.Group()

    # HUD variables
    self.status_bar_icon = pygame.sprite.Sprite()
    self.status_bar_icon.image = pygame.image.load('./graphics/tileset/Status/status_bar_icon.png').convert_alpha()
    self.status_bar_icon.image = pygame.transform.smoothscale(self.status_bar_icon.image, (48,48))
    self.status_bar_icon.rect = self.status_bar_icon.image.get_rect(center=(32,32))
    
    self.kunai_icon =  pygame.sprite.Sprite()
    self.kunai_icon.image = pygame.image.load('./graphics/ninja/kunai.png').convert_alpha()
    self.kunai_icon.image = pygame.transform.smoothscale(self.kunai_icon.image, (96,16))
    self.kunai_icon.rect = self.kunai_icon.image.get_rect(center=(112, 48))
    
    self.kunai_total = 0
    self.kunai_count = pygame.sprite.Sprite()
    self.kunai_font = pygame.font.SysFont('Rage', 24)
    self.kunai_count.image = self.kunai_font.render(f'Kunai: {self.kunai_total}',True, 'black')
    self.kunai_count.rect = self.kunai_count.image.get_rect(topright=(self.kunai_icon.rect.right+96, self.kunai_icon.rect.y))

    self.life_count = 3
    self.player_life = pygame.sprite.Sprite()
    self.player_life_font = pygame.font.SysFont('Rage', 32)
    self.player_life.image = self.player_life_font.render('Lives:', True, 'black')
    self.player_life.rect = self.player_life.image.get_rect(topright=(self.kunai_icon.rect.x+20, self.kunai_icon.rect.y+self.kunai_icon.rect.height+20))


    self.player_life_icon = pygame.sprite.Sprite()
    self.life_image = pygame.image.load('./graphics/ninja/Attack__005.png').convert_alpha()
    self.player_life_icon.image = pygame.transform.smoothscale(self.life_image, (32,32))
    self.player_life_icon.rect = self.player_life_icon.image.get_rect(topright=(self.player_life.rect.right+40, self.player_life.rect.y))

    self.player_life_icon2 = pygame.sprite.Sprite()
    self.player_life_icon2.image = pygame.transform.smoothscale(self.life_image, (32,32))
    self.player_life_icon2.rect = self.player_life_icon2.image.get_rect(topright=(self.player_life_icon.rect.right+40, self.player_life.rect.y))
    
    self.player_life_icon3 = pygame.sprite.Sprite()
    self.player_life_icon3.image = pygame.transform.smoothscale(self.life_image, (32,32))
    self.player_life_icon3.rect = self.player_life_icon3.image.get_rect(topright=(self.player_life_icon2.rect.right+40, self.player_life.rect.y))


    self.hud_sprites.add(self.status_bar_icon)
    self.hud_sprites.add(self.kunai_icon)
    self.hud_sprites.add(self.kunai_count)
    self.hud_sprites.add(self.player_life)
    self.hud_sprites.add(self.player_life_icon)
    self.hud_sprites.add(self.player_life_icon2)
    self.hud_sprites.add(self.player_life_icon3)
    
    
    self.generate_level(self.current_level)

  def background_scroll(self):
    player = self.player
    player_x = player.rect.x
    direction_x = player.direction.x

    if player_x < SCREEN_WIDTH//4 and direction_x < 0:
      if sorted(self.platform_sprites, key=lambda spr: spr.rect.x)[0].rect.x > -5:
        self.background_shift = 0
        player.velocity = 5
        if player_x - player.velocity < 0:
          player_x = self.player.velocity
          player.velocity = 0
      else:
        self.background_shift = 5
        player.velocity = 0
    elif player_x > SCREEN_WIDTH//4*3 and direction_x > 0:
      platform = sorted(self.platform_sprites, key=lambda spr: spr.rect.x)[-1]
      if platform.rect.x + platform.rect.width < SCREEN_WIDTH + 5:
        self.background_shift = 0
        player.velocity = 5
        if player_x + player.rect.width + player.velocity > SCREEN_WIDTH:
          player_x = SCREEN_WIDTH - player.rect.width - 5
          player.velocity = 0
      else:
        self.background_shift = -5
        player.velocity = 0
    else:
      self.background_shift = 0
      player.velocity = 5

  def check_if_dead(self):
    return self.player.health <= 0

  def check_if_drown(self):
    for water in self.water_sprites:
      if pygame.sprite.collide_mask(self.player, water):
        return True
    
    return False

  def check_if_finished_level(self):
    return pygame.sprite.collide_mask(self.player, self.win)

  def check_if_past_checkpoint(self):
    return self.player.rect.right >= self.checkpoint.rect.left

  def generate_background(self, level_number=0):
    for i in range(3):
      Background((i * SCREEN_WIDTH,0), [self.background_sprites], 'BG')
    
    level_data = import_level_data(level_number)[0]
    for i, row in enumerate(level_data):
      for j, col in enumerate(row):
        x, y = j * TILE_WIDTH, i * TILE_HEIGHT
        if col == '0':  Platform((x,y), [self.platform_sprites], 1)
        if col == '1':  Platform((x,y), [self.platform_sprites], 2)
        if col == '2':  Platform((x,y), [self.platform_sprites], 3)
        if col == '3':  Platform((x,y), [self.platform_sprites], 4)
        if col == '4':  Platform((x,y), [self.platform_sprites], 5)
        if col == '5':  Platform((x,y), [self.platform_sprites], 6)
        if col == '6':  Platform((x,y), [self.platform_sprites], 7)
        if col == '7':  Platform((x,y), [self.platform_sprites], 8)
        if col == '8':  Platform((x,y), [self.platform_sprites], 9)
        if col == '9':  Platform((x,y), [self.platform_sprites], 10)
        if col == '10': Platform((x,y), [self.platform_sprites], 11)
        if col == '11': Platform((x,y), [self.platform_sprites], 12)
        if col == '12': Platform((x,y), [self.platform_sprites], 13)
        if col == '13': Platform((x,y), [self.platform_sprites], 14)
        if col == '14': Platform((x,y), [self.platform_sprites], 15)
        if col == '15': Platform((x,y), [self.platform_sprites], 16)
        if col == '20': Bush((x,y), [self.bush_sprites], 'Bush_1')
        if col == '21': Bush((x,y), [self.bush_sprites], 'Bush_2')
        if col == '22': Bush((x,y), [self.bush_sprites], 'Bush_3')
        if col == '23': Bush((x,y), [self.bush_sprites], 'Bush_4')
        if col == '24': Crate((x,y), [self.crate_sprites], 'Crate', int(col))
        if col == '25': Mushroom((x,y), [self.mushroom_sprites], 'Mushroom_1')
        if col == '26': Mushroom((x,y), [self.mushroom_sprites], 'Mushroom_2')
        if col == '27': self.checkpoint = Sign((x,y), [self.checkpoint_sprite], 'Sign_1')
        if col == '28': Sign((x,y), [self.sign_sprites], 'Sign_2')
        if col == '29': Stone((x,y), [self.stone_sprites], 'Stone')
        if col == '30': Tree((x,y), [self.tree_sprites], 'Tree_1')
        if col == '31': Tree((x,y), [self.tree_sprites], 'Tree_2', -10)
        if col == '32': Tree((x,y), [self.tree_sprites], 'Tree_3', -10)

  def generate_foreground(self, level_number=0):
    level_data = import_level_data(level_number)[1]
    for i, row in enumerate(level_data):
      for j, col in enumerate(row):
        x, y = j * TILE_WIDTH, i * TILE_HEIGHT
        if col == '0':  Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 1)
        if col == '1':  Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 2)
        if col == '2':  Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 3)
        if col == '3':  Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 4)
        if col == '4':  Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 5)
        if col == '5':  Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 6)
        if col == '6':  Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 7)
        if col == '7':  Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 8)
        if col == '8':  Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 9)
        if col == '9':  Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 10)
        if col == '10': Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 11)
        if col == '11': Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 12)
        if col == '12': Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 13)
        if col == '13': Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 14)
        if col == '14': Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 15)
        if col == '15': Platform((x,y), [self.platform_sprites, self.obstacle_sprites], 16)
        if col == '20': Bush((x,y), [self.bush_sprites], 'Bush_1')
        if col == '21': Bush((x,y), [self.bush_sprites], 'Bush_2')
        if col == '22': Bush((x,y), [self.bush_sprites], 'Bush_3')
        if col == '23': Bush((x,y), [self.bush_sprites], 'Bush_4')
        if col == '24': Crate((x,y), [self.crate_sprites, self.obstacle_sprites], 'Crate', int(col))
        if col == '25': self.win = Mushroom((x,y), [self.win_sprite], 'Mushroom_1')
        if col == '26': Mushroom((x,y), [self.mushroom_sprites], 'Mushroom_2')
        if col == '27': self.checkpoint = Sign((x,y), [self.checkpoint_sprite], 'Sign_1')
        if col == '28': Sign((x,y), [self.sign_sprites], 'Sign_2')
        if col == '29': Stone((x,y), [self.stone_sprites], 'Stone')
        if col == '30': Tree((x,y), [self.tree_sprites], 'Tree_1')
        if col == '31': Tree((x,y), [self.tree_sprites], 'Tree_2', -10)
        if col == '32': Tree((x,y), [self.tree_sprites], 'Tree_3', -10)
        if col == '33': self.player = Player((x, y), [self.player_sprite], self.obstacle_sprites, self.enemy_sprites)
        if col == '34': self.enemy = Enemy((x, y), [self.enemy_sprites, self.enemy_list], 'Walk', self.obstacle_sprites)
        if col == '35': Kunai((x,y),[self.kunai_sprites])

  def generate_hud(self):
    pygame.draw.rect(self.display_surface, 'black', (TILE_WIDTH-2, TILE_HEIGHT//4-2, self.player.health*2+4, 16+4), 2, 5)
    if 75 < self.player.health <= 100:  pygame.draw.rect(self.display_surface, 'green', (TILE_WIDTH, TILE_HEIGHT//4, self.player.health*2, 16), 0, 5)
    elif 50 < self.player.health <= 75: pygame.draw.rect(self.display_surface, 'yellow', (TILE_WIDTH, TILE_HEIGHT//4, self.player.health*2, 16), 0, 5)
    elif 0 < self.player.health <= 50:  pygame.draw.rect(self.display_surface, 'red', (TILE_WIDTH, TILE_HEIGHT//4, self.player.health*2, 16), 0, 5)

  def generate_level(self, level_number=0):
      self.generate_background(level_number)
      self.generate_foreground(level_number)
      self.generate_water(level_number)

  def generate_water(self, level_number=0):  
    level_data = import_level_data(level_number)[-1]
    for i, row in enumerate(level_data):
      for j, col in enumerate(row):
        x, y = j * TILE_WIDTH, i * TILE_HEIGHT
        if col != '-1': Water((x,y), [self.water_sprites], int(col))

  def horizontal_collision(self):
    player = self.player
    player.hitbox.x += player.direction.x * player.velocity
    for sprite in self.obstacle_sprites:
      if player.rect.colliderect(sprite.rect):
        if player.direction.x > 0: 
          player.hitbox.right = sprite.hitbox.left 
          player.direction.x = 0
        elif player.direction.x < 0: 
          player.hitbox.left = sprite.hitbox.right 
          player.direction.x = 0

    player.rect.center = player.hitbox.center

  def reset_camera(self, past_checkpoint):
    if past_checkpoint: self.background_shift = abs(self.player.rect.centerx - self.checkpoint.rect.centerx)
    else: self.background_shift = abs(self.player.rect.x - self.player.reset_position[0]) - 400

  def reset_at_checkpoint(self):
    level_data = import_level_data(self.current_level)[1]
    for i, row in enumerate(level_data):
      for j, col in enumerate(row):
        x, y = j * TILE_WIDTH, i * TILE_HEIGHT
        if col == '34': self.enemy = Enemy((x, y), [self.enemy_sprites, self.enemy_list], 'Walk', self.obstacle_sprites)

  def reset_player_at_checkpoint(self, past_checkpoint):
    self.reset_camera(past_checkpoint)
    self.player.health = 100
    if not past_checkpoint: self.player.reset(self.player.reset_position);
    else: self.player.rect.move(-self.background_shift, 0); self.player.rect.bottom = self.checkpoint.rect.bottom

  def reset_players_recovery(self):
    if self.player.recovering:
      current_time = pygame.time.get_ticks()
      if current_time - self.start_time >= self.timer_length:
        self.start_time = current_time
        self.player.recovering = False 

  def run(self):
    self.reset_players_recovery()
    self.update_damage()
    self.update_health()
    self.update_kunai_count()
    self.vertical_collision()
    self.horizontal_collision()
        
    # Terrain Sprites
    self.background_sprites.update(self.background_shift)
    self.background_sprites.draw(self.display_surface)
  
    self.water_sprites.update(self.background_shift)
    self.water_sprites.draw(self.display_surface)

    self.platform_sprites.update(self.background_shift)
    self.platform_sprites.draw(self.display_surface)
    
    self.bush_sprites.update(self.background_shift)
    self.bush_sprites.draw(self.display_surface)
    
    self.sign_sprites.update(self.background_shift)
    self.sign_sprites.draw(self.display_surface)

    self.stone_sprites.update(self.background_shift)
    self.stone_sprites.draw(self.display_surface)

    self.tree_sprites.update(self.background_shift)
    self.tree_sprites.draw(self.display_surface)

    # Health Sprites
    self.mushroom_sprites.update(self.background_shift)
    self.mushroom_sprites.draw(self.display_surface)
    
    # Sprites that when collided with help unlock next level or checkpoint
    self.checkpoint_sprite.update(self.background_shift)
    self.checkpoint_sprite.draw(self.display_surface)
    
    self.crate_sprites.update(self.background_shift)
    self.crate_sprites.draw(self.display_surface)

    self.kunai_sprites.update(self.background_shift)
    self.kunai_sprites.draw(self.display_surface)

    self.win_sprite.update(self.background_shift)
    self.win_sprite.draw(self.display_surface)

    # Character/Enemy Sprites  
    self.player_sprite.update() 
    self.player_sprite.draw(self.display_surface)

    self.enemy_sprites.update(self.background_shift, self.player)
    self.enemy_sprites.draw(self.display_surface)  

    self.hud_sprites.update()
    self.hud_sprites.draw(self.display_surface)
    self.generate_hud()
    self.background_scroll()

  def update_damage(self):
      if self.player.attacking and pygame.sprite.spritecollide(self.player, self.enemy_sprites, True, pygame.sprite.collide_mask):
        self.player.attacking = False
      elif not self.player.attacking and not self.player.recovering and pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
        self.player.state = 'damage'
        self.player.health -= randint(5,10)
        self.player.recovering = True
      else:   
        if not pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
          self.player.state = 'normal' 
        else: 
          self.player.state = 'damage'

  def update_health(self):
    if pygame.sprite.spritecollide(self.player, self.mushroom_sprites, True):
      self.player.recovering = True
      self.player.health += randint(5,15)
      if self.player.health > 100: self.player.health = 100
 
  def update_kunai_count(self):
    if pygame.sprite.spritecollide(self.player, self.kunai_sprites, dokill=True, collided=pygame.sprite.collide_mask):
      self.kunai_total += 1
      self.player.kunai_total += 1
      self.kunai_count.image = self.kunai_font.render(f'Kunai: {self.kunai_total}',True, 'black')

  def update_player_lives(self, lives_left):
    self.life_count = lives_left
    if lives_left == 3: 
      self.player_life.image = self.player_life_font.render('Lives:', True, 'black')
    elif lives_left == 2: 
      self.player_life.image = self.player_life_font.render('Lives:', True, 'black')
      self.hud_sprites.remove(self.player_life_icon3)
    elif lives_left == 1: 
      self.player_life.image = self.player_life_font.render('Lives:', True, 'black')
      self.hud_sprites.remove(self.player_life_icon3)
      self.hud_sprites.remove(self.player_life_icon2)

  def update(self, level_number):
    self.current_level = level_number
    self.generate_level(self.current_level)

  def vertical_collision(self):
      player = self.player
      player.apply_gravity()

      for sprite in self.obstacle_sprites: 
        if sprite.hitbox.colliderect(player.hitbox):
          if player.direction.y > 0: 
            player.hitbox.bottom = sprite.hitbox.top
            player.direction.y = 0
            player.jumping = False
          elif player.direction.y < 0: 
            player.hitbox.top = sprite.hitbox.bottom 
            player.direction.y = 0



      player.rect.center = player.hitbox.center
      if player.rect.y > SCREEN_HEIGHT:
        pygame.QUIT
        sys.exit()






# class YSortCameraGroup(pygame.sprite.Group):
#   def __init__(self):
#       super().__init__()
#       self.display_surface = pygame.display.get_surface()
#       self.half_width = self.display_surface.get_size()[0] // 2
#       self.half_height = self.display_surface.get_size()[1] // 2
#       self.offset = pygame.math.Vector2()
  

#   def custom_draw(self, player):
#       self.offset.x = player.rect.centerx - self.half_width
#       self.offset.y = player.rect.centery - self.half_height

#       for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
#           offset_position = sprite.rect.topleft - self.offset
#           self.display_surface.blit(sprite.image, sprite.rect)

# print(pygame.font.get_fonts())