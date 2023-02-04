import pygame

from settings import *

pygame.font.init()


def db_show_grid():
  window = pygame.display.get_surface()
  text_font = pygame.font.SysFont('arial', TILE_WIDTH//4)

  for i in range(window.get_width()//TILE_WIDTH): 
        for j in range(window.get_height()//TILE_HEIGHT): 
          
          text_surf = text_font.render(f'[{i},{j}]',True,(255,0,0))
          text_rect = text_surf.get_rect(topleft=(i*TILE_WIDTH+5,j*TILE_HEIGHT))
          pygame.draw.rect(window,(0,0,0), (i*TILE_WIDTH,j*TILE_HEIGHT,TILE_WIDTH,TILE_HEIGHT), 2, 5)
          window.blit(text_surf,text_rect)


