import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):   
        super().__init__()
        self.path = "assets/Individual_Sprites/adventurer-"
        self.x =   x
        self.y =   y
        self.state = "idle"
        self.direction = -1  # Hướng nhân vật
        
        self.frame = 0
        self.animation = {}
        self.load_animation()
        self.image = self.animation[self.state][0]
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
        #Khởi tạo trọng lực
        self.gravity = 1
        self.velocity = 0
        self.ground_level = y
        #kiểm tra attack 
        self.attack = False  
        self.hp = 100      
    def load_animation(self):
        states = {
            "idle": 2,
            "idle-2": 2,
            "run":     5, 
            "jump":    3,
            "fall":    1,
            "stand":   2,
            "attack1": 4,
            "attack2": 5,
            "attack3": 5,
            "crnr-grb":3,
            "die":     6,
            "hurt":    2,
        }
        for states_name, num_frames in states.items():
            frames = []
            for i in range(num_frames):
                image_path = f"{self.path}{states_name}-{i:02}.png"
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (100, 100))
                frames.append(image)
            self.animation[states_name] = frames
                
    def play_animation(self, animation_name, speed_animation=0.1):
        if self.state != animation_name:
            self.state = animation_name
            self.frame = 0
        self.frame += speed_animation
        if self.frame >= len(self.animation[self.state]):
            self.frame = 0
            
    def update(self, keys, platforms):
        moving = False 
        
        if self.attack: 
            self.play_animation("attack1")
            if self.frame >= len(self.animation["attack1"]) - 1:
                self.attack = False
        else:
            if keys [pygame.K_z]:
                self.attack = True
                self.play_animation("attack1")
            if keys [pygame.K_x]:
                self.play_animation("attack2") 
            else:
                if keys [pygame.K_LEFT]:
                    moving = True
                    self.direction = 1 
                    self.rect.x -= 5
                    self.play_animation("run")
                    if keys [pygame.K_LSHIFT]:
                        self.play_animation("stand")
                        self.rect.x -= 10
                if keys [pygame.K_RIGHT]:
                    moving = True
                    self.direction = -1
                    self.play_animation("run")
                    self.rect.x += 5
                    if keys [pygame.K_LSHIFT]:
                        self.play_animation("stand")
                        self.rect.x += 10
                if keys [pygame.K_SPACE]:
                    self.play_animation("jump")
                    self.rect.y -= 17
                elif moving == False and self.velocity == 0:
                    self.play_animation("idle")
        
        
        self.velocity += self.gravity
        self.rect.y += self.velocity


        if self.rect.bottom >= self.ground_level:
            self.rect.bottom = self.ground_level
            self.velocity = 0

        #Điều chỉnh hướng 
        raw_image = self.animation[self.state][int(self.frame)]
        if self.direction == 1:
            self.image = pygame.transform.flip(raw_image, True, False)
        else:
            self.image = raw_image    
            
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1000:
            self.rect.right = 1000
        if self.hp == 0: 
            self.play_animation("die")    
            
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity > 0:
                    self.rect.bottom = platform.top
                    self.velocity = 0 
        
        
        