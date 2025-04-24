import pygame
from src.player import Player
from src.background import Background
from src.background import Tilesheet
from src.enemy import Enemy


pygame.init()
pygame.mixer.music.load('Sound/2000_Battle1.ogg')
#pygame.mixer.music.play(-1)
#Set chiều rộng chiều cao
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Arena")

player = Player(100,770)
enemy = Enemy(700,770)
background = Background()
tilesheet1 = Tilesheet("assets/Final/tiles.png", 80, 80, 3, 4)
all_sprites = pygame.sprite.Group(player,enemy)

running = True
game_over = False 
winner = None 

HP_BAR_WIDTH = 200
HP_BAR_HEIGHT = 20
HP_BAR_MARGIN = 20 

def draw_game_over(surface,winner_name):
    font = pygame.font.SysFont(None, 64)
    text = f"{winner_name} WINNER!"
    text_surface = font.render(text, True, (255, 215, 0))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    surface.blit(text_surface, text_rect)
    
    font_small = pygame.font.SysFont(None, 36)
    retry_text = "Press R to reset or ESC to escape !"
    retry_surface = font_small.render(retry_text, True, (255, 255, 255))
    retry_rect = retry_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    surface.blit(retry_surface, retry_rect)
    
def draw_health_bar(surface,x,y,current_hp,max_hp,is_player=True):
    ratio = current_hp/max_hp
    if is_player:
        fill_color = (0,255,0)
    else: 
        fill_color = (255,0,0)
    background_color = (50,50,50)
    
    pygame.draw.rect(surface, background_color,(x,y, HP_BAR_WIDTH, HP_BAR_HEIGHT))

    filler_width = int(HP_BAR_WIDTH * ratio)
    pygame.draw.rect(surface, fill_color, (x,y, filler_width,HP_BAR_HEIGHT))
    
    pygame.draw.rect(surface, (255,255,255),(x,y,HP_BAR_WIDTH,HP_BAR_HEIGHT),2)
    
    font = pygame.font.SysFont(None,24)
    text = f"{current_hp}/{max_hp}"
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + HP_BAR_WIDTH//2, y + HP_BAR_HEIGHT//2))
    surface.blit(text_surface, text_rect)
    
    
    
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30, 30, 30))
    background.draw(screen)
    if not game_over:
        keys = pygame.key.get_pressed()
        player.update(keys, background.platform(), enemy)
        enemy.update(player)

        if player.hp <= 0:
            game_over = True
            winner = "Enemy"
        elif enemy.hp <= 0:
            game_over = True
            winner = "You"
    else:
        draw_game_over(screen, winner)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game
            player = Player(100, 770)
            enemy = Enemy(700, 770)
            all_sprites = pygame.sprite.Group(player, enemy)
            game_over = False
            winner = None
        elif keys[pygame.K_ESCAPE]:
            running = False



    #tilesheet1.draw(screen)          #check xem tilesheet đã được in hay chưa 
    #tilesheet2.draw(screen)
    all_sprites.draw(screen)
    draw_health_bar(screen, HP_BAR_MARGIN, HP_BAR_MARGIN, player.hp, 100, True)
    draw_health_bar(screen, SCREEN_WIDTH - HP_BAR_WIDTH - HP_BAR_MARGIN, HP_BAR_MARGIN, enemy.hp, 100, False)
    pygame.display.flip()

pygame.quit()

