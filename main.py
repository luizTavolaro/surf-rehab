

import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 768
SCREEN_HEIGHT = 432

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bg_images = []

bg1 = pygame.image.load(f"img/background1_v2.png").convert_alpha()
bg2 = pygame.image.load(f"img/background2.png").convert_alpha()
ground = pygame.image.load(f"img/ground_background.png").convert_alpha()
waves =  pygame.image.load(f"img/wave_nobakground.png").convert_alpha()

bg_images.append(bg1)
bg_images.append(ground)
bg_images.append(bg2)
bg_images.append(waves)

bg_width = bg_images[0].get_width()

scroll = 0

def draw_bg():
  for x in range(5):
    speed = 1
    screen.blit(bg_images[0], ((x * bg_width) - scroll * 1, 0))
    screen.blit(bg_images[1], ((x * bg_width) - scroll * 2, 0))
    screen.blit(bg_images[2], ((x * bg_width) - scroll * 3, 0))
    screen.blit(bg_images[3], ((x * bg_width) - scroll * 1, 0))


run = True
while run:

  clock.tick(FPS)

  draw_bg()

  key = pygame.key.get_pressed()
  if key[pygame.K_LEFT] and scroll > 0:
    scroll -= 5
  if key[pygame.K_RIGHT] and scroll < 1000:
    scroll += 5

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()