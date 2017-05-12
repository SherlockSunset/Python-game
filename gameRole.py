# -*- coding: utf-8 -*-

import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

# Bullet class
class Bullet(pygame.sprite.Sprite):   #pygame.sprite.Sprite: Simple base class for visible game objects 
    def __init__(self, bullet_img, init_pos):  #initial function
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):                         # move function
        self.rect.top -= self.speed

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # To store the list of the player pictures
        for i in range(len(player_rect)):
            #self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
            self.image.append(plane_img.subsurface(player_rect[i]))
        self.rect = player_rect[0]                      # Initialize the picture
        self.rect.topleft = init_pos                    # attributes: the topleft of self.rect is at init_pos
        self.speed = 10                                  # Initialize the speed of the player
        self.bullets = pygame.sprite.Group()            # set of bullets
        self.img_index = 0                              # index of images
        self.is_hit = False                             # player is dead or not

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    #def specialshoot(self, bullet_img):
        

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed
    

# 敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs   # attacked image
       self.speed = 2
       self.down_index = 0

    def move(self):
        self.rect.top += self.speed
