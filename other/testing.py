lst=[16*(i+1) for i in range(20)]
print(lst)
#Imports
import pygame as pyg
from sys import exit as sysexit
from classes import *

pyg.init()
pyg.display.set_caption('isometric viszualization                                        |v2.7.3|')

#Globals
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600
SCREEN = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pyg.font.Font("freesansbold.ttf", 20)
FONT2 = pyg.font.Font("freesansbold.ttf", 15)
tile_index={0:None,1:'assets/blocks/stone.png',2:'assets/blocks/brick.png',3:[f'assets/blocks/grass{i}.png' for i in range(4)],4:'assets/blocks/dirt.png',5:'assets/blocks/glass.png',6:'assets/bed.png'}
TILE_WIDTH=64

#Main
def main():
    clock = pyg.time.Clock()
    fall=False
    lock=False
    shiftx,shifty,tmp=0,0,0
    projectiles=[]
    tiles=[]
    player=iso_player((-0.2,-0.2),tw=TILE_WIDTH)
    #map_data=open_map('77')
    map_data=generate_map()
    for row_ind,row in enumerate(map_data):
        for column_ind,tile_data in enumerate(row):
            if tile_index[tile_data[0]] is not None:
                tiles.append(iso_tile((column_ind,row_ind),tile_data[1],TILE_WIDTH,SCREEN_WIDTH,tile_index[tile_data[0]]))
    tiles.sort(key=lambda x:x.vz)
    health=Health_Bar(5,200)
    hotbar=Hotbar(int(SCREEN_WIDTH-SCREEN_WIDTH/3),10,192,48,'assets/player/hotbar.png','assets/player/selected.png')

    def spawn_fireball():
        angs=[120,241,300,63.425]
        projectiles.append(Projectile((player.rect.centerx,player.rect.centery),32,32,8,angs[player.rotation],'fireball',5))
    hotbar.add_item('fire','assets/items/fire.png',10,spawn_fireball)
    hotbar.add_item('apple','assets/items/apple.png',5,lambda: health.heal(1))
    hotbar.add_item('meat','assets/items/meat.png',2,lambda: health.heal(3))
    hotbar.add_item('sword','assets/items/crystal.png',func=lambda: health.damage(1))
    #MAIN LOOP
    run = True
    while run:
        ###inputs
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sysexit()
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    hotbar.scroll(1)
                elif event.button == 5:
                    hotbar.scroll(-1)
                if event.button == 1:
                    hotbar.use_item()
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_w and not fall:
                    if player.rotation==0:
                        player.vx+=1
                    if player.rotation==2:
                        player.vx-=1
                    if player.rotation==1:
                        player.vy+=1
                    if player.rotation==3:
                        player.vy-=1
                    player.update(shiftx,shifty)
                if event.key == pyg.K_a:
                    player.rotate(-1)
                if event.key == pyg.K_d: 
                    player.rotate(1)
                if event.key == pyg.K_q:
                    lock=not lock
                if event.key == pyg.K_e:
                    shiftx=tmp
                    print((round(player.vx,1),round(player.vy,1)),(player.rect.centerx,player.rect.centery),'\t\t',(round(player.on_x),round(player.on_y)),map_data[round(player.on_y)][round(player.on_x)])
        ###mechanics
        run=health.update()
        if lock:
            tmp+=-(player.rect.centerx-(SCREEN_WIDTH/2))
            print(tmp)
        #falling
        if len(map_data[0])>round(player.on_x) and len(map_data)>round(player.on_y) and round(player.on_x)>=0 and round(player.on_y)>=0:
            current_block_data=map_data[round(player.on_y)][round(player.on_x)]
        else:
            current_block_data=(0,-1)
        if tile_index[current_block_data[0]] is None:
            fall=True
        if fall:
            if player.rect.y>SCREEN_HEIGHT and current_block_data[1]==-1:
                run=False
            else:
                player.vx+=0.3
                player.vy+=0.3
        else:
            player.vz=current_block_data[1]
        ###drawing to screen
        SCREEN.fill((30, 30, 30))

        bf_tiles=[t for t in tiles if t.vz<= player.vz]
        af_tiles=[t for t in tiles if t.vz> player.vz]
        for tile in bf_tiles:
            tile.shift_tile(shiftx,shifty)
            tile.draw_img(SCREEN)
        player.draw_img(SCREEN)
#player.draw_hitbox(SCREEN)
        for tile in af_tiles:
            tile.shift_tile(shiftx,shifty)
            tile.draw_img(SCREEN)

        for ind,projectile in enumerate(projectiles):
            projectile.draw_update(SCREEN)
            if projectile.rect.centerx>SCREEN_WIDTH or projectile.rect.centerx<0 or projectile.rect.centery>SCREEN_HEIGHT or projectile.rect.centery<0:
                projectiles.pop(ind)

        player.update(shiftx,shifty)
        hotbar.draw(SCREEN,FONT2)
        health.draw(SCREEN)

        clock.tick(30)
        pyg.display.update()
    blinkR=False
    blink=255
    while True:
        for event in pyg.event.get():
            if event.type == pyg.QUIT or event.type == pyg.KEYDOWN or event.type == pyg.MOUSEBUTTONDOWN:
                pyg.quit()
                sysexit()
        pyg.draw.polygon(SCREEN,(20,20,20),((int(SCREEN_WIDTH/3.5),int(SCREEN_HEIGHT/2.4)),(SCREEN_WIDTH-int(SCREEN_WIDTH/3.5),int(SCREEN_HEIGHT/2.4)),(SCREEN_WIDTH-int(SCREEN_WIDTH/3.5),SCREEN_HEIGHT-int(SCREEN_HEIGHT/3)),(int(SCREEN_WIDTH/3.5),SCREEN_HEIGHT-int(SCREEN_HEIGHT/3))))

        if blinkR:
            blink+=2
        else:
            blink-=2
        if blink<=30:
            blinkR=True
        elif blink>=250:
            blinkR=False
        txt1=FONT.render('You died.', True, (240,240,240))
        txt2=FONT.render('Press any key to quit...', True, (blink,blink,blink))
        txtRect1=txt1.get_rect(center=(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2)))
        txtRect2=txt2.get_rect(center=(int(SCREEN_WIDTH/2), 50+int(SCREEN_HEIGHT/2)))
        SCREEN.blit(txt1, txtRect1)
        SCREEN.blit(txt2, txtRect2)

        clock.tick(30)
        pyg.display.update()

main()