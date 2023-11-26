#Imports
import pygame as pyg
import sys
from classes import *
from random import randint,choice

pyg.init()

#Globals
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600
SCREEN = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pyg.font.Font("freesansbold.ttf", 15)

class Blast:
    def __init__(self,origin,acceleration,image=None,frames=None):
        self.ogx,self.ogy=origin
        self.acceleration=acceleration
        self.expand=1
        self.radius=64#5
    def draw_update(self,screen):
        self.radius-=self.expand#+
        self.expand+=self.acceleration
        pyg.draw.circle(screen,(240,64+self.radius*3,240),(self.ogx,self.ogy),abs(self.radius),5)

class Weapon:
    def __init__(self,origin,w,h,rotational_speed,image,frames):
        self.ogx,self.ogy=origin
        self.rect=pyg.Rect(self.ogx,self.ogy,w,h)

        self.angle=0
        self.speed=rotational_speed
        self.tmpx=self.ogx-(self.rect.h/90)*(270-180)
        self.tmpy=self.ogy-(self.rect.w/90)*(270-180)

        self.anim=0
        self.frames=frames
        self.image_name=image
        self.image=pyg.transform.rotate(pyg.transform.scale(pyg.image.load(f'assets/items/{image}.png').convert_alpha(),(w,h)),0)
    def draw_update(self,screen):
        self.angle+=self.speed
        self.anim+=0.2
        if self.anim>=(self.frames-1):
            self.anim=0

        rotated=pyg.transform.rotate(pyg.transform.scale(pyg.image.load(f'assets/items/{self.image_name}.png').convert_alpha(),(self.rect.w,self.rect.h)),self.angle)
        rotated_rect=rotated.get_rect(center = self.image.get_rect(center = (self.ogx, self.ogy)).center)

        #self.image=pyg.transform.rotate(pyg.transform.scale(pyg.image.load(f'assets/items/{self.image_name}{round(self.anim)}.png').convert_alpha(),(self.rect.w,self.rect.h)),(-self.angle+90)+180)
        screen.blit(rotated,rotated_rect)

#Main
def main():
    clock = pyg.time.Clock()
    def spawn_projectile():
        ang=((two_point_ang((300,300),pyg.mouse.get_pos())-270)+360)%360
        projectiles.append(Projectile(pyg.mouse.get_pos(),64,64,8,ang,'fireball',5))
    def crystal_blast():
        #Weapon((300,300),192,26,20,'blade',1)
        blasts.append(Blast(pyg.mouse.get_pos(),1))

    inv_toggle=False
    projectiles=[]
    blasts=[]
    bar=Hotbar(20,100,256,64,'assets/player/hotbar.png','assets/player/selected.png')
    bar.add_item(item('fire','assets/items/fire.png',10,spawn_projectile))
    bar.add_item(item('bottle','assets/items/water.png'))
    bar.add_item(item('sword','assets/items/crystal.png',func=crystal_blast))
    inv=Inventory(250,200,256,288,'assets/player/inventory.png',bar)
    inv.add_item(item('fire','assets/items/fire.png',5,spawn_projectile))
    for i in range(23):
        inv.add_item(item(str(randint(0,100)),choice(['assets/items/apple.png','assets/items/meat.png','assets/items/crystal.png','assets/items/water.png'])))
    

    #MAIN LOOP
    run = True
    while run:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    bar.scroll(1)
                elif event.button == 5:
                    bar.scroll(-1)
                if event.button == 1:
                    if inv_toggle:
                        inv.pickup_item()
                    else:
                        bar.use_item()
            if event.type == pyg.MOUSEBUTTONUP:
                if event.button == 1:
                    inv.release_item()
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_e:
                    inv_toggle=not inv_toggle

        SCREEN.fill((30, 30, 30))
        bar.draw(SCREEN,FONT)
        pyg.draw.circle(SCREEN,(240,240,240),(300,300),3)

        for ind,projectile in enumerate(projectiles):
            projectile.draw_update(SCREEN)
            if projectile.rect.centerx>SCREEN_WIDTH or projectile.rect.centerx<0 or projectile.rect.centery>SCREEN_HEIGHT or projectile.rect.centery<0:
                projectiles.pop(ind)
        for ind,blast in enumerate(blasts):
            blast.draw_update(SCREEN)
            if blast.radius<=10:
                blasts.pop(ind)

        if inv_toggle:
            inv.draw(SCREEN)
            inv.update()

        clock.tick(30)
        pyg.display.update()

main()