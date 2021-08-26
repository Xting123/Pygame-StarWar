import pygame
from pygame import image
from pygame import draw
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP
import random
import os

height, width = 600, 500
title = "Star War"
FPS = 60

# color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((width, height))   #視窗大小
pygame.display.set_caption(title)   #標題名稱
clock = pygame.time.Clock()

pygame.mixer.init()
# 載入音效
shoot_sound = pygame.mixer.Sound(os.path.join('sound', 'shoot.wav'))  # 射擊
explosion_sounds = [      # 爆炸
    pygame.mixer.Sound(os.path.join('sound', 'expl0.wav')),
    pygame.mixer.Sound(os.path.join('sound', 'expl1.wav'))
]
player_explosion_sound = pygame.mixer.Sound(os.path.join('sound', 'rumble.ogg'))  # 飛機爆炸
# 背景音樂
pygame.mixer.music.load(os.path.join('sound', 'background.ogg'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)


# 載入圖片
background_img = pygame.image.load(os.path.join('img', 'background.png')).convert()
player_img = pygame.image.load(os.path.join('img', 'player.png')).convert()
bullet_img = pygame.image.load(os.path.join('img', 'bullet.png')).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join('img', f'rock{i}.png')).convert() )
# 爆炸圖片
explosion_dict = {}
explosion_dict['big_explosion'] = []
explosion_dict['small_explosion'] = []
explosion_dict['player_explosion'] = [] # 飛機爆炸圖片
for i in range(9): 
    explosion_img = pygame.image.load(os.path.join('img', f'expl{i}.png')).convert()
    explosion_img.set_colorkey(BLACK)
    explosion_dict['big_explosion'].append(pygame.transform.scale(explosion_img, (60, 60)))
    explosion_dict['small_explosion'].append(pygame.transform.scale(explosion_img, (20, 20)))

    player_explosion_img = pygame.image.load(os.path.join('img', f'player_expl{i}.png')).convert()
    player_explosion_img.set_colorkey(BLACK)
    explosion_dict['player_explosion'].append(player_explosion_img)
mini_player_img = pygame.image.load(os.path.join('img', 'player.png')).convert()
mini_player_img.set_colorkey(BLACK)
mini_player_img = pygame.transform.scale(mini_player_img, (40, 28))
# 寶物
treasure_dict = {}
treasure_dict['shield'] = pygame.image.load(os.path.join('img', 'shield.png')).convert()
treasure_dict['gun'] = pygame.image.load(os.path.join('img', 'gun.png')).convert()
circle_img = pygame.image.load(os.path.join('img', 'circle.png')).convert()

# 分數
score = 0
def draw_Score(text, font_size, x, y):
    score_font = pygame.font.Font('font.ttf', font_size)
    score_font.set_bold(True)
    score_surface = score_font.render(text, True, WHITE)
    screen.blit(score_surface, (x, y))

def draw_text(text, font_size, x, y):
    text_font = pygame.font.Font('font.ttf', font_size)
    text_font.set_bold(True)
    text_surface = text_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    screen.blit(text_surface, text_rect)

def draw_Healthy(hp, x, y):
    if hp < 0:
        hp = 0
    Bar_lengh = 100
    Bar_heigh = 10
    origin_hp_rect = pygame.Rect(x, y, Bar_lengh, Bar_heigh)
    fill_hp_rect = pygame.Rect(x, y, hp, Bar_heigh)
    pygame.draw.rect(screen, WHITE, origin_hp_rect)
    pygame.draw.rect(screen, GREEN, fill_hp_rect)

def Add_Rock():
    rock = Rock()
    allsprite.add(rock)
    rocks.add(rock)

def mini_player(live, image, x, y):
    for i in range(live):
        screen.blit(image, (x,y))
        x -= 50

def draw_init():
    screen.blit(background_img, (0, 0))
    screen.blit(player.image, player.rect)
    draw_text('Star War', 50, width/2, height/6)
    draw_text('↑↓←→ 控制飛船', 20, width/2, height/2.5)
    draw_text('空白鍵發射子彈', 20, width/2, height/2)
    draw_text('請按任意鍵開始遊戲', 20, width/2, height/1.5)
    pygame.display.update()
    wait = True
    while(wait):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                wait = False
    # name
    
    # how to play
    # how to start

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = ((width/2, (height-30)))
        self.speedx = 10
        self.healthy = 100
        self.live = 3
        self.hidden = False
        self.treasure_gun = 1
    
    def update(self):
        if self.treasure_gun > 1 and pygame.time.get_ticks() - self.gun_time > 5000:
            self.treasure_gun = 1
        if self.hidden == True and pygame.time.get_ticks()-self.hide_time > 2000:
            self.rect.center = ((width/2, (height-30)))
            if self.live == 0:
                self.hidden = True
            else:
                self.hidden = False
        if self.hidden == False:
            if pygame.key.get_pressed()[K_LEFT]:
                self.rect.x -= self.speedx
            if pygame.key.get_pressed()[K_RIGHT]:
                self.rect.x += self.speedx
            if pygame.key.get_pressed()[K_UP]:
                self.rect.y -= self.speedx
            if pygame.key.get_pressed()[K_DOWN]: 
                self.rect.y += self.speedx
            # player 移動範圍
            if(self.rect.right > width):
                self.rect.right = width
            if(self.rect.left < 0):
                self.rect.left = 0
            if(self.rect.bottom > height):
                self.rect.bottom = height
            if(self.rect.top < 0):
                self.rect.top = 0
    
    def shoot(self):
        if self.hidden != True:
            if self.treasure_gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top-1)
                allsprite.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.treasure_gun > 1:
                bullet1 = Bullet(self.rect.left, self.rect.top-1)
                bullet2 = Bullet(self.rect.right, self.rect.top-1)
                allsprite.add(bullet1)
                allsprite.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
        
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (width/2, 700)
        # if self.live == 0 and self.hidden == True:
        #     self.rect.top = height + 100

    def Treasure_shield(self):
        self.healthy += 10
        if self.healthy > 100:
            self.healthy = 100
    def Treasure_gun(self):
        self.treasure_gun += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = random.choice(rock_imgs)
        self.image_origin.set_colorkey(BLACK)
        self.image = self.image_origin.copy()
        self.rect = self.image.get_rect()  #取得畫布區塊
        self.radius = int(self.rect.width *0.8 /2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, (width - self.rect.width))
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 10)
        # rock rotate
        self.totall_rotate_degree = 0
        self.rotate_degree = random.randint(-3, 3)
    
    def rotate(self):
        self.totall_rotate_degree += self.rotate_degree
        self.totall_rotate_degree = self.totall_rotate_degree % 360
        self.image = pygame.transform.rotate(self.image_origin, self.totall_rotate_degree)
        center = self.rect.center   # get self center before rotate
        self.rect = self.image.get_rect()   # get self center after rotate
        self.rect.center = center   # reset center

    def update(self):
        self.rotate()
        # rock move
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # rock 移動範圍
        if(self.rect.right > width + 100 or self.rect.left < 0 - 100 or self.rect.top > height):
            self.rect.x = random.randrange(0, (width - self.rect.width))
            self.rect.y = random.randrange(-10, 50)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y): # 這裡的self = bullet
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  #取得畫布區塊
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if(self.rect.bottom < 0):
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, size, center): # 這裡的self = dict
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_dict[self.size][0]
        self.rect = self.image.get_rect()  #取得畫布區塊
        self.rect.center = center
        self.frame = 0 #imge
        self.lastframe = pygame.time.get_ticks()
        self.rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.lastframe > self.rate:
            self.lastframe = now
            self.frame += 1
            if self.frame == len(explosion_dict[self.size]):
                self.kill()
            else:
                self.image = explosion_dict[self.size][self.frame]
                center = self.rect.center   # get self center before rotate
                self.rect = self.image.get_rect()   # get self center after rotate
                self.rect.center = center   # reset center

class Treasure(pygame.sprite.Sprite):
    def __init__(self, center): # 這裡的self = dict
        pygame.sprite.Sprite.__init__(self)
        self.key = random.choice(['shield', 'gun'])
        self.image = treasure_dict[self.key]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  #取得畫布區塊
        self.rect.center = center
        self.speedy = 3
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height:
            self.kill()

allsprite = pygame.sprite.Group()
player = Player()
bullets = pygame.sprite.Group()
allsprite.add(player)
rocks = pygame.sprite.Group()
for i in range(8):
    Add_Rock()
treasures = pygame.sprite.Group()

running = True
show_init = True
while running:
    clock.tick(FPS)
    
    if show_init == True:
        draw_init()
        show_init = False
        score = 0
        allsprite = pygame.sprite.Group()
        player = Player()
        bullets = pygame.sprite.Group()
        allsprite.add(player)
        rocks = pygame.sprite.Group()
        for i in range(8):
            Add_Rock()
        treasures = pygame.sprite.Group()
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[K_SPACE]:
                player.shoot()

    #更新畫面
    allsprite.update()

    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:  # hit == rock
        explosion = Explosion('big_explosion', hit.rect.center)
        allsprite.add(explosion)
        
        random.choice(explosion_sounds).play()
        score += hit.radius
        Add_Rock()
        if random.random() < 0.03:
            treasure = Treasure(hit.rect.center)
            allsprite.add(treasure)
            treasures.add(treasure)
        
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)   
    for hit in hits:  # hit == rock
        player.healthy -= hit.radius 
        Add_Rock()
        if player.healthy < 0:
            explosion = Explosion('player_explosion', player.rect.center)
            allsprite.add(explosion)
            player_explosion_sound.play()
            player.live -= 1
            player.healthy = 100
            player.hide()
        if player.live == 0 and explosion.alive() == False:
            show_init = True
        explosion = Explosion('small_explosion', hit.rect.center)
        allsprite.add(explosion)

    hits = pygame.sprite.spritecollide(player, treasures, True)
    for hit in hits:
        if hit.key == 'shield':
            player.Treasure_shield()
        if hit.key == 'gun':
            player.Treasure_gun()
     #畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    allsprite.draw(screen)
    screen.blit(player.image, player.rect)  #強制把player放在最上面
    draw_Score('Score : %s' % str(score), 20, 15, 35)
    draw_Healthy(player.healthy, 15, 20)
    mini_player(player.live, mini_player_img, 445, 25)
    pygame.display.update()

pygame.quit()
