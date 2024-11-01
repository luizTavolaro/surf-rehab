

import pygame
from pygame.locals import *
import random

pygame.init()

SCREEN_WIDTH = 768
SCREEN_HEIGHT = 432

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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

FONT = pygame.font.Font(None, 36)

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
    def __init__(self, y):
        super(Obstacle, self).__init__()
        self.image = pygame.image.load(f"img/sharkfin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, LANE_HEIGHT * 0.6)) 
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.center = (SCREEN_WIDTH, y)

    def update(self):
        self.rect.x -= 7 
        if self.rect.right < 0:
            self.kill()  

def draw_bg(scroll = 0):
    for x in range(50):
        SCREEN.blit(bg_images[0], ((x * bg_width) - scroll * 1, 0))
        SCREEN.blit(bg_images[2], ((x * bg_width) - scroll * 2, 0))
    SCREEN.blit(sun, (SCREEN_WIDTH - sun.get_width(), 0))

def main():
    surfer = Surfer("Luiz")
    all_sprites = pygame.sprite.Group()
    all_sprites.add(surfer)
    scroll = 0
    max_scroll = bg_width * 10 - SCREEN_WIDTH 

    obstacle_timer = 0
    obstacle_interval = 2000
    obstacle_passed_count = 0
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
                obstacle = Obstacle(lane_y + LANE_HEIGHT // 2)
                obstacles.add(obstacle)
                all_sprites.add(obstacle)

        if pygame.sprite.spritecollideany(surfer, obstacles):
            running = False

        for obstacle in obstacles:
            if obstacle.rect.right < surfer.rect.left:
                obstacle_passed_count += 1
                obstacle.kill()

        draw_bg(scroll=scroll)
        all_sprites.update()
        all_sprites.draw(SCREEN)    

        score_text = FONT.render(f"{obstacle_passed_count // 2}", True, (0, 0, 0))
        SCREEN.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
  
    pygame.quit()

if __name__ == "__main__":
    main()
