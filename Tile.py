import pygame

class Tilesheet:
    def __init__(self, filename, width, height, row, col):
        image = pygame.image.load(filename).convert_alpha()
        self.tile_table = []
        for tile_x in range(0, col):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, row):
                rect = (tile_x * width, tile_y * height, width, height)
                line.append(image.subsurface(rect))
        self.plaform_rect = []
    def get_tile(self,x,y):
        return self.tile_table[x][y]
    
    
    def draw(self, screen):
        for tile_x in range(0, len(self.tile_table)):
            for tile_y in range(0, len(self.tile_table[tile_x])):
                screen.blit(self.tile_table[tile_x][tile_y], (tile_x * 150, tile_y * 150))