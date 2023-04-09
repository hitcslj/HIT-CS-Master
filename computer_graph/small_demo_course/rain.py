import pygame
import random

# 初始化
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("雨景模拟")

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 雨滴类
class Raindrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(-20, screen_height)

    def update(self):
        self.rect.y += 5
        if self.rect.y > screen_height:
            self.rect.y = random.randint(-20, -1)
            self.rect.x = random.randint(0, screen_width)

# 雨滴精灵组
raindrops = pygame.sprite.Group()

# 创建雨滴
for _ in range(100):
    raindrop = Raindrop()
    raindrops.add(raindrop)

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    raindrops.update()
    raindrops.draw(screen)
    pygame.display.flip()

pygame.quit()
