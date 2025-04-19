import pygame 
from src.Tile import Tilesheet

class Background(pygame.sprite.Sprite,Tilesheet):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.image1,self.rect1 = self.load_image("assets/Final/Background_0.png")
        self.image2,self.rect2 = self.load_image("assets/Final/Background_1.png",(1000,500))
        self.image3,self.rect3 = self.load_image("assets/Final/Grass_background_1.png")
        self.image4,self.rect4 = self.load_image("assets/Final/Grass_background_2.png")
        self.tile_sheet = Tilesheet("assets/Final/tiles.png", 80, 80, 4, 4)
        self.tile_sheet2 = Tilesheet("assets/Final/brush.png",112,92,2,2)
        self.platform_rect = []
        
        
        
    def load_image(self, name_image, scale=(1000, 800)):
        image = pygame.image.load(name_image).convert_alpha()
        image = pygame.transform.scale(image, scale)
        rect = image.get_rect()
        rect.topleft = (self.x, self.y)
        return image, rect
        
        
    def draw(self, screen):
        screen.blit(self.image1, (0,0))
        screen.blit(self.image2, (0,300))
        #screen.blit(self.image3, (self.rect3.x, self.rect3.y))
        #screen.blit(self.image4, (self.rect4.x, self.rect4.y))
        # for i in range(4):
        #     for j in range(4):
        #         screen.blit(self.tile_sheet.get_tile(i,j), (250*j, 100*i))
        
        # screen.blit(self.tile_sheet2.get_tile(0,1),(100,700))
        # for i in range(20):
        #     screen.blit(self.tile_sheet.get_tile(3,3),(50*i,750))
        
        screen.blit(self.tile_sheet.get_tile(1,3),(400,600))
    def platform(self):
        if not self.platform_rect: 
            # for i in range(3):
            #     rect = self.tile_sheet.get_tile(i,3).get_rect(topleft=(200*i , 600))
            #     self.platform_rect.append(rect)
            rect = self.tile_sheet.get_tile(1,3).get_rect(topleft=(400,600))    
            self.platform_rect.append(rect)
        return self.platform_rect

