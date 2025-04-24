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
        self.attack_ready_to_damage = False 
        
        #Cơ chế bất tử 
        self.invincible = False 
        self.invincible_time = 60 
        self.invincible_cooldown = 0 
        self.knock_back = 0 
        
        
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
        return True
            
    def take_damage(self, amount,enemy):
        if not self.invincible and self.hp > 0:
            self.hp -= amount
            self.invincible = True
            self.invincible_cooldown = self.invincible_time
            self.image.fill((255, 255, 255), special_flags=pygame.BLEND_ADD) 
        if self.rect.centerx < enemy.rect.centerx:
            self.knock_back = -10 
        else:
            self.knock_back = 10 
        
        if self.hp > 0: 
            self.play_animation("hurt", speed_animation=0.5)
    
    def update(self, keys, platforms,enemy):
        moving = False 
        if self.hp > 0:        
            # Áp dụng đẩy lùi nếu đang bị knockback
            if self.knock_back != 0:
                self.rect.x += self.knock_back
                # Giảm dần hiệu ứng đẩy lùi
                if self.knock_back > 0:
                    self.knock_back -= 1
                elif self.knock_back < 0:
                    self.knock_back += 1

            
            if self.invincible:
                self.invincible_cooldown -= 1 
                if self.invincible_cooldown <= 0:
                    self.invincible = False
                    self.image.set_alpha(255)
                if self.invincible_cooldown % 10 < 5:
                    self.image.set_alpha(150)
                else:
                    self.image.set_alpha(255)
            else: 
                self.image.set_alpha(255)
                
                
            if self.attack: 
                self.play_animation("attack1")
                if self.frame >= len(self.animation["attack1"]) - 1:
                    self.attack = False
                    self.attack_ready_to_damage = False
                elif self.frame >= 1 and not self.attack_ready_to_damage:
                    self.attack_ready_to_damage = True
                if self.attack_ready_to_damage and self.rect.colliderect(enemy.rect):
                    enemy.take_damage(10)
                    self.attack_ready_to_damage = False 
            else:
                if keys [pygame.K_z]:
                    self.attack = True
                    self.play_animation("attack1")
                    self.attack_ready_to_damage = False
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
        else: 
            animation_finished = self.play_animation("die")
            animation_finished
            
        
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
            
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity > 0:
                    self.rect.bottom = platform.top
                    self.velocity = 0 
        
        if self.rect.colliderect(enemy.rect) and enemy.attack_ready_to_damage:
            self.take_damage(10, enemy)
            enemy.attack_ready_to_damage = False  

        

