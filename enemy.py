import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):   
        super().__init__()
        self.path = "assets/boss_demon/Final/demon_"
        self.x =   x
        self.y =   y
        self.state = "idle"
        self.direction = 1  # Hướng nhân vật
        
        self.frame = 0
        self.animation = {}
        self.load_animation()
        self.image = self.animation[self.state][0]
        self.image = pygame.transform.scale(self.image, (400, 400))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
        #Khởi tạo trọng lực
        self.gravity = 1
        self.velocity = 0
        self.ground_level = y
        
        #kiểm tra attack 
        self.attack = False  
        self.hp = 100      
        self.attack_cooldown = 120  
        self.attack_range = 50   #Khoảng attack 
        self.detection_range = 600 
        self.speed = 2 
        self.attack_ready_to_damage = False 
        
        self.invincible = False
        self.invincible_cooldown = 0
        self.invincible_time = 60

        
    def load_animation(self):
        states = {
            "idle": 6,
            "walk": 12, 
            "cleave": 15,
            "death":  21,
            "take_hit": 5,
        }
        for states_name, num_frames in states.items():
            frames = []
            for i in range(num_frames):
                image_path = f"{self.path}{states_name}_{int(i)+1}.png"
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (400, 400))
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
        return False
            
    def take_damage(self, amount):
        if not self.invincible:
            self.hp -= amount 
            self.invincible = True 
            self.invincible_cooldown = self.invincible_time
            self.play_animation("take_hit")

    def update(self,player):
        animation_finished = False 
        if self.hp > 0:    
            if self.attack_cooldown > 0:
                    self.attack_cooldown -= 1
            
            # Kiểm tra khoảng cách với player
            distance_to_player = abs(player.rect.centerx - self.rect.centerx)
            
            if self.invincible:
                self.invincible_cooldown -= 1
            if self.invincible_cooldown <= 0:
                self.invincible = False

            if self.attack and distance_to_player > self.attack_range:
            # Hủy tấn công nếu player ra khỏi phạm vi giữa chừng
                self.attack = False
                self.play_animation("idle")  # Quay lại trạng thái idle

            if player.rect.centerx < self.rect.centerx:
                self.direction = -1
            else:
                self.direction = 1            
            # Nếu player trong phạm vi phát hiện
            if distance_to_player < self.detection_range and self.hp > 0:
                # Nếu đủ gần để tấn công
                if distance_to_player < self.attack_range and self.attack_cooldown == 0:
                    self.attack = True
                    self.attack_cooldown = 120  # 1 giây hồi chiêu (60 frames)
                    
                # Nếu đang tấn công
                if self.attack:
                    animation_finished = self.play_animation("cleave", 0.5)
                    if animation_finished:
                        self.attack = False
                        self.attack_ready_to_damage = True  # Animation kết thúc -> cho phép gây damage

                else:
                    # Di chuyển về phía player
                    if distance_to_player > self.attack_range / 2:  # Giữ một khoảng cách an toàn
                        if self.direction == -1:
                            self.rect.x -= self.speed
                        else:
                            self.rect.x += self.speed
                        self.play_animation("walk")
                    else:
                        self.play_animation("idle")
            else:
                self.play_animation("idle")
        else: 
            animation_finished = self.play_animation("death")
            if animation_finished:
                self.kill()
            
        # Áp dụng trọng lực
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # Kiểm tra va chạm với mặt đất
        if self.rect.bottom >= self.ground_level:
            self.rect.bottom = self.ground_level
            self.velocity = 0

        # Điều chỉnh hướng 
        raw_image = self.animation[self.state][int(self.frame)]
        if self.direction == 1:
            self.image = pygame.transform.flip(raw_image, True, False)
        else:
            self.image = raw_image    
            
        # Giới hạn không ra khỏi màn hình
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1000:
            self.rect.right = 1000
            
        
        # Gây damage sau khi animation đánh xong
        if self.attack_ready_to_damage:
            if self.rect.colliderect(player.rect): 
                player.take_damage(40,player)  
            self.attack_ready_to_damage = False  # Chỉ gây 1 lần mỗi đòn

        
        