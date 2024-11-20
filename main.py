import pygame
from pygame.locals import *
import random

pygame.init()

SCREEN_WIDTH = 768
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
sun2 = pygame.image.load(f"img/sun2.png").convert_alpha()
sun2 = pygame.transform.scale(sun2, (SCREEN_WIDTH, SCREEN_HEIGHT))
sun3 = pygame.image.load(f"img/sun3.png").convert_alpha()
sun3 = pygame.transform.scale(sun3, (SCREEN_WIDTH, SCREEN_HEIGHT))
background2 = pygame.image.load(f"img/background2.png").convert_alpha()
background2 = pygame.transform.scale(background2, (SCREEN_WIDTH, SCREEN_HEIGHT))
background3 = pygame.image.load(f"img/background3.png").convert_alpha()
background3 = pygame.transform.scale(background3, (SCREEN_WIDTH, SCREEN_HEIGHT))
clouds2 = pygame.image.load(f"img/clouds2.png").convert_alpha()
clouds2 = pygame.transform.scale(clouds2, (SCREEN_WIDTH, SCREEN_HEIGHT))
clouds3 = pygame.image.load(f"img/clouds3.png").convert_alpha()
clouds3 = pygame.transform.scale(clouds3, (SCREEN_WIDTH, SCREEN_HEIGHT))

bg_images.append(clouds)
bg_images.append(sun)
bg_images.append(sea)
bg_images.append(background)

bg_width = bg_images[0].get_width()

TOP_LIMT = 170
BOTTOM_LIMT = SCREEN_HEIGHT - 80

LANE_HEIGHT = (BOTTOM_LIMT - TOP_LIMT) // 3

FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 72)

LANE_Y_POSITIONS = [
    TOP_LIMT,
    TOP_LIMT + LANE_HEIGHT,
    TOP_LIMT + 2 * LANE_HEIGHT,
    BOTTOM_LIMT
]

# Cores
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def start_screen():
    running = True
    while running:
        SCREEN.fill(BLUE)
        draw_text("Surf Game", BIG_FONT, WHITE, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text("Pressione ENTER para Iniciar", FONT, WHITE, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Pressione ESC para Sair", FONT, WHITE, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:  # ENTER para iniciar
                    running = False
                elif event.key == K_ESCAPE:  # ESC para sair
                    pygame.quit()
                    exit()

        pygame.display.flip()

def pause_screen():
    paused = True
    while paused:
        SCREEN.fill((0, 0, 0))  # Fundo preto
        draw_text("Jogo Pausado", BIG_FONT, WHITE, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text("Pressione ENTER para Continuar", FONT, WHITE, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Pressione ESC para Sair", FONT, WHITE, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:  # ENTER para continuar
                    paused = False
                elif event.key == K_ESCAPE:  # ESC para sair
                    pygame.quit()
                    exit()

        pygame.display.flip()


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
    def __init__(self, lane_y, w, h):
        super().__init__()
        self.images = [
            pygame.image.load(f"img/seagul1.png").convert_alpha(),
            pygame.image.load(f"img/seagul2.png").convert_alpha()
        ]
        self.images = [pygame.transform.scale(img, (w, int(h))) for img in self.images]
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

def draw_bg(level=1, scroll=0, speed=1):
    if level == 1:
        sun_img = sun
        background_img = background
        clouds_img = clouds
    elif level == 2:
        sun_img = sun2
        background_img = background2
        clouds_img = clouds2
    elif level == 3:
        sun_img = sun3
        background_img = background3
        clouds_img = clouds3

    # Ajuste do movimento do fundo
    SCREEN.blit(background_img, (0, 0))
    SCREEN.blit(sun_img, (SCREEN_WIDTH - sun_img.get_width(), 0))
    
    # Desenhando as nuvens e o mar com movimento
    for x in range(50):
        SCREEN.blit(clouds_img, ((x * bg_width) - scroll * speed, 0))
        SCREEN.blit(sea, ((x * bg_width) - scroll * 2 * speed, 0))


def main():
    start_screen()
    level = 1
    surfer = Surfer("Luiz")
    all_sprites = pygame.sprite.Group()
    all_sprites.add(surfer)
    scroll = 0
    max_scroll = bg_width * 10 - SCREEN_WIDTH 

    obstacle_timer = 0
    obstacle_interval = 2000
    obstacle_passed_count = 0
    obstacles = pygame.sprite.Group()
    obstacle_w = 30
    obstacle_h = LANE_HEIGHT * 0.4

    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # ESC para pausar
                    pause_screen()
        
        # Atualizando o movimento do fundo com base na velocidade
        if scroll == max_scroll:
            max_scroll += 100
        scroll = min(scroll + 2, max_scroll)

        # Atualiza obstáculos
        obstacle_timer += clock.get_time()
        if obstacle_timer >= obstacle_interval:
            obstacle_timer = 0
            lanes = random.sample(LANE_Y_POSITIONS[:-1], 2)
            for lane_y in lanes:
                obstacle = Obstacle(lane_y + LANE_HEIGHT // 2, obstacle_w, obstacle_h)
                obstacles.add(obstacle)
                all_sprites.add(obstacle)

        # Verificando colisões com obstáculos
        if pygame.sprite.spritecollideany(surfer, obstacles):
            running = False

        # Removendo obstáculos que passaram
        for obstacle in obstacles:
            if obstacle.rect.right < surfer.rect.left:
                obstacle_passed_count += 1
                obstacle.kill()

        # Atualizando e desenhando o fundo
        draw_bg(level=level, scroll=scroll, speed=(level))  # Passando o nível para controlar a velocidade

        # Atualiza e desenha todos os sprites
        all_sprites.update()
        all_sprites.draw(SCREEN) 

        # Exibindo pontuação e nível
        score_color = (0, 0, 0)
        if obstacle_passed_count // 2 >= 3:
            level = 3
        elif obstacle_passed_count // 2 >= 2: 
            level = 2
        if level == 3:
            score_color = (255, 255, 255)

        level_text = FONT.render(f"Nível: {level}", True, score_color)
        score_text = FONT.render(f"{obstacle_passed_count // 2}", True, score_color)
        SCREEN.blit(level_text, (10, 10))
        SCREEN.blit(score_text, (10, 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
