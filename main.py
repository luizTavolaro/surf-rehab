

import pygame
from pygame.locals import *
import random

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 432

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bg_images = []

clouds = pygame.image.load(f"img/clouds.png").convert_alpha()
clouds = pygame.transform.scale(clouds, (SCREEN_WIDTH, SCREEN_HEIGHT))
sun = pygame.image.load(f"img/sun.png").convert_alpha()
sun = pygame.transform.scale(sun, (SCREEN_WIDTH, SCREEN_HEIGHT))
sea = pygame.image.load(f"img/sea.png").convert_alpha()
sea = pygame.transform.scale(sea, (SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load(f"img/background.png").convert_alpha()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

bg_images.append(clouds)
bg_images.append(sun)
bg_images.append(sea)
bg_images.append(background)

bg_width = bg_images[0].get_width()

TOP_LIMT = 170
BOTTOM_LIMT = SCREEN_HEIGHT - 80

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
        self.image = pygame.transform.scale(self.image, (70, LANE_HEIGHT + 10))
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
        super().__init__()
        self.images = [
            pygame.image.load(f"img/seagul1.png").convert_alpha(),
            pygame.image.load(f"img/seagul2.png").convert_alpha()
        ]
        self.images = [pygame.transform.scale(img, (30, int(LANE_HEIGHT * 0.6))) for img in self.images]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = lane_y
        
        self.animation_index = 0
        self.animation_timer = 0
        self.animation_interval = 2000  

    def update(self):
        self.rect.x -= 7
        if self.rect.right < 0:
            self.kill()

        self.animation_timer += 100
        if self.animation_timer >= self.animation_interval:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]

def draw_bg(scroll = 0):
    SCREEN.blit(background, (0, 0))
    SCREEN.blit(sun, (SCREEN_WIDTH - sun.get_width(), 0))
    for x in range(50):
        SCREEN.blit(clouds, ((x * bg_width) - scroll * 1, 0))
        SCREEN.blit(sea, ((x * bg_width) - scroll * 2, 0))


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
        
        if scroll == max_scroll:
            max_scroll += 100
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
