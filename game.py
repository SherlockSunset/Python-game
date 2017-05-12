# -*- coding: utf-8 -*-
import pygame
from sys import exit
from pygame.locals import *   #This module contains various constants used by pygame
from gameRole import *
import random


# Initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Star Wars')
healthvalue = 194
exitcode = 0
t = pygame.time.get_ticks()  # to record the time
n =3

# Load sound
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(1, 0.0)  # playback of the music: play(loops=0, start=0.0)
pygame.mixer.music.set_volume(0.25)
hit = pygame.mixer.Sound("resources/sound/explod.wav")
specialhit = pygame.mixer.Sound("resources/sound/shoot.wav")
specialbulletimg = pygame.image.load('resources/image/specialbullet.png')

# load background
background = pygame.image.load('resources/image/background1.jpg')
background1 = pygame.image.load('resources/image/background2.jpg')

game_over = pygame.image.load('resources/image/gameover.png')
you_win = pygame.image.load("resources/image/youwin.png")

filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)

healthbar = pygame.image.load("resources/image/healthbar.png")
health = pygame.image.load("resources/image/health.png")

# set parameters
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        # player picture
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # exploded player picture
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]

player = Player(plane_img, player_rect, player_pos)  # call class Player

# get the picture of bullet
bullet_rect = pygame.Rect(1004, 987, 8, 20)   #Rect(left, top, width, height)
bullet_img = plane_img.subsurface(bullet_rect)#to create a new image object

# get the picture of the special bullet
bullet_rect1 = pygame.Rect(826, 694, 30, 52)
bullet_img1 = plane_img.subsurface(bullet_rect1)

# get the picture of enemy 定义敌机对象使用的surface相关参数
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies1 = pygame.sprite.Group()#A container class to hold and manage multiple Sprite objects

# 存储被击毁的飞机，用来渲染击毁精灵动画
enemies_down = pygame.sprite.Group()

shoot_frequency = 0
enemy_frequency = 0

player_down_index = 16

score = 0

clock = pygame.time.Clock()  #create an object to help track time

running = True

specialbullet = 0

#specialbullets = []
while running:
    # frame rate 90
    clock.tick(60)

    # shoot the bullets
    if not specialbullet:
        if shoot_frequency % 15 == 0:
            bullet_sound.play()
            player.shoot(bullet_img) # call fuction
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0
    else:
        specialhit.play()
        player.shoot(bullet_img1)
        n = n - 1
    # ennemies
    if pygame.time.get_ticks()<=60000:
        if enemy_frequency % 25 == 0:  
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            # call class
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)  
            enemies1.add(enemy1)
        enemy_frequency += 1
        if enemy_frequency >= 100:
            enemy_frequency = 0
    else:
        if enemy_frequency % 15 == 0:  #different frequency
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        enemy_frequency += 1
        if enemy_frequency >= 100:
            enemy_frequency = 0

    # move bullet, if exceeds the range, delete it
    for bullet in player.bullets:
        bullet.move()                   # call move fuction
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    # move enemies, if exceed the range, delete
    for enemy in enemies1:
        enemy.move()                    # call move function
        #Collision detection between two sprites, using circles
        if pygame.sprite.collide_circle(enemy, player):  
            hit.play()
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            healthvalue -= random.randint(5, 20)
            if healthvalue <=0:
                player.is_hit = True
                game_over_sound.play()
                exitcode = 1
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies1.remove(enemy)

    # 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
    #Find all sprites that collide between two groups
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # draw background
    if pygame.time.get_ticks()<=60000:
        screen.fill(0)
        screen.blit(background1, (0, 0))
    else:
        screen.fill(0)
        screen.blit(background, (0, 0))

    # draw player
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # animated player
        player.img_index = shoot_frequency // 8   # 0 and 1 (float number division)
    else:
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        # within the range of player.image, 6 images in total
        if player_down_index > 47:   
            running = False

    # destroy animation
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 300000
            
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1
        
    ### draw bullets and enemies
    player.bullets.draw(screen)
    enemies1.draw(screen)

    # Draw score
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (255, 0, 0))
    text_rect = score_text.get_rect()
    text_rect.topleft = [5, 30]
    screen.blit(score_text, text_rect)


    # Draw clock
    font = pygame.font.Font(None, 36)
    survivedtext = font.render(str((120000-pygame.time.get_ticks())/60000)+":"+str((60000-pygame.time.get_ticks())/1000%60).zfill(2), True, (255, 0, 0))
    textRect = survivedtext.get_rect()
    textRect.topright = [475, 5]
    screen.blit(survivedtext, textRect)
    if pygame.time.get_ticks()>=120000:
        game_over_sound.play()
        exitcode = 0
        break
    
    # draw healthbar
    screen.blit(healthbar, (5, 5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1 + 8, 8))
    if score >= 3000:
        exitcode = 0
        break
        
    # 更新屏幕
    pygame.display.update()
    
    # quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # monitor the keyboard
    key_pressed = pygame.key.get_pressed()
    # does not work once player is dead
    if not player.is_hit:
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()
        if key_pressed[K_j] and pygame.time.get_ticks() - t > 4000 :
            specialbullet = 1
            
        #t = pygame.time.get_ticks()
        #if pygame.time.get_ticks() - t > 9000 :    ###############################
        #    screen.blit(bullet_img1, (443, 745))
        if pygame.time.get_ticks() - t > 9000:
            specialbullet = 0
            t =pygame.time.get_ticks()
    
# end the game         
if exitcode:
    font = pygame.font.Font(None, 48)
    text = font.render('Score: '+ str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(game_over, (0, 0))
    screen.blit(text, text_rect)
else:
    font = pygame.font.Font(None, 48)
    text = font.render('Score: '+ str(score), True, (0, 255, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(you_win, (0, 0))
    screen.blit(text, text_rect)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()



