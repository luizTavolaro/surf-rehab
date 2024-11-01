

import pygame
from pygame.locals import *
import random

pygame.init()

SCREEN_WIDTH = 768
SCREEN_HEIGHT = 432

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bg_images = []

clouds = pygame.image.load(f"img/clouds.png").convert_alpha()
sun = pygame.image.load(f"img/sun.png").convert_alpha()
sea = pygame.image.load(f"img/sea.png").convert_alpha()

bg_images.append(clouds)
bg_images.append(sun)
bg_images.append(sea)

bg_width = bg_images[0].get_width()

TOP_LIMT = 200
BOTTOM_LIMT = SCREEN_HEIGHT - 50

LANE_HEIGHT = (BOTTOM_LIMT - TOP_LIMT) // 3

LANE_Y_POSITIONS = [
    TOP_LIMT,
    TOP_LIMT + LANE_HEIGHT,
    TOP_LIMT + 2 * LANE_HEIGHT,
    BOTTOM_LIMT
]

class Surfer(pygame.sprite.Sprite):
    def __init__(self, name):
        super(Surfer, self).__init__()
        self.name = name
        self.alive = True
        self.position = pygame.math.Vector2(100, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.image = pygame.image.load(f"img/surfer.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70,LANE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[K_UP] and self.position.y > TOP_LIMT:
            self.position.y -= self.speed
        elif keys[K_DOWN] and self.position.y < BOTTOM_LIMT:
            self.position.y += self.speed

        self.rect.center = self.position

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, lane_y):
        super(Obstacle, self).__init__()
        self.image = pygame.image.load(f"img/sharkfin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, LANE_HEIGHT * 0.8)) 
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = lane_y

    def update(self):
        self.rect.x -= 7 
        if self.rect.right < 0:
            self.kill()  

def draw_bg(scroll = 0):
    for x in range(50):
        screen.blit(bg_images[0], ((x * bg_width) - scroll * 1, 0))
        screen.blit(bg_images[2], ((x * bg_width) - scroll * 2, 0))
    screen.blit(sun, (SCREEN_WIDTH - sun.get_width(), 0))
    
    for y in LANE_Y_POSITIONS:
        pygame.draw.line(screen, (255, 0, 0), (0, y), (SCREEN_WIDTH, y), 2) 


def main():
    surfer = Surfer("Luiz")
    all_sprites = pygame.sprite.Group()
    all_sprites.add(surfer)
    scroll = 0
    max_scroll = bg_width * 5 - SCREEN_WIDTH 

    obstacle_timer = 0
    obstacle_interval = 2000
    obstacles = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        scroll = min(scroll + 2, max_scroll)

        obstacle_timer += clock.get_time()
        if obstacle_timer >= obstacle_interval:
            obstacle_timer = 0

            lanes = random.sample(LANE_Y_POSITIONS[:-1], 2)
            for lane_y in lanes:
                obstacle = Obstacle(lane_y)
                obstacles.add(obstacle)
                all_sprites.add(obstacle)

        if pygame.sprite.spritecollideany(surfer, obstacles):
            running = False

        draw_bg(scroll=scroll)
        all_sprites.update()
        all_sprites.draw(screen)    
        
        pygame.display.flip()
        clock.tick(60)
  
    pygame.quit()

if __name__ == "__main__":
    main()
