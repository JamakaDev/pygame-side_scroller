import pygame
import sys
import debug
from settings import *
from level import Level
from map import Map

class Game():      
  def __init__(self, surface):
    # Screen and Frame rate setup
    self.window = surface
    self.width = surface.get_width()
    self.height = surface.get_height()
    
    # Level & Map instances for the game to toggle    
    self.level = Level()
    self.map = Map()
    
    # Variables to help the flow of the game
    self.running = True
    self.playing = False
    self.past_checkpoint = False
    self.player_lives = 3
    self.level.update_player_lives(self.player_lives)
    
  def run(self, debug_mode=False):
    if debug_mode: 
      debug.db_show_grid()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False

    # Check for input from user
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: 
      self.playing = True

    if keys[pygame.K_HOME]: 
      self.map.update(self.level.current_level)
      self.playing = False

    if keys[pygame.K_RETURN] and not self.playing:
      self.playing = True
      if self.level.current_level == self.map.current_level:
        if self.past_checkpoint: self.level.reset_at_checkpoint()
        # else: self.level = Level(self.map.current_level)
      else:
        self.level = Level(self.map.current_level)
        self.past_checkpoint = False


    # Ability to switch between Map and Levels 
    if self.playing: self.level.run()
    else: self.map.run()

    if self.level.check_if_finished_level() and self.level.kunai_total > 2: 
      self.map.max_level += 1 if self.map.max_level < 5 else 0
      self.level.current_level += 1
      if self.level.current_level < 6: self.level = Level(self.level.current_level); self.past_checkpoint = False; self.level.update_player_lives(self.player_lives)
      else: self.level.current_level -= 1; self.map.update(self.level.current_level); self.playing = False
    
    if self.level.check_if_past_checkpoint(): self.past_checkpoint = True

    if self.level.check_if_drown() or self.level.check_if_dead() and self.playing: 
      self.playing = False
      self.player_lives -= 1
      self.level.reset_player_at_checkpoint(self.past_checkpoint)
      self.level.update_player_lives(self.player_lives)
      self.map.update(self.level.current_level)

    if self.player_lives == 0: self.running = False
    

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.RESIZABLE); pygame.display.set_caption('Ninja Ninja')
clock = pygame.time.Clock()
game = Game(screen) 

while game.running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	screen.fill('#abcdef')
	game.run()

	pygame.display.update()
	clock.tick(FPS)