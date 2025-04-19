import pygame
from src.player import Player
from src.background import Background
from src.background import Tilesheet


pygame.init()
pygame.mixer.music.load('Sound/2000_Battle1.ogg')
pygame.mixer.music.play(-1)
#Set chiều rộng chiều cao
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Arena")

player = Player(100,770)
background = Background()
tilesheet1 = Tilesheet("assets/Final/tiles.png", 80, 80, 3, 4)
tilesheet2 = Tilesheet("assets/Final/brush.png", 80, 80, 2, 2)
all_sprites = pygame.sprite.Group(player)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30, 30, 30))



    keys = pygame.key.get_pressed()
    player.update(keys, background.platform())




    background.draw(screen)
    #tilesheet1.draw(screen)          #check xem tilesheet đã được in hay chưa 
    #tilesheet2.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()

