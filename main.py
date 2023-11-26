#Imports
import pygame as pyg
from sys import exit as sysexit
from classes import *
from other import pathfinding

pyg.init()
pyg.display.set_caption('isometric viszualization                                        |v2.8.2|')

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
    #Internal vars
    clock = pyg.time.Clock()
    inventory_toggle=False
    fall=False
    pan,panx,pany=False,0,0
    shiftx,shifty=0,0
    projectiles=[]
    tiles=[]
    player=iso_player((-0.2,-0.2),tw=TILE_WIDTH)
    #global enemy_d
    #enemy,enemy_d,enemy_ds=iso_player((3.8,3.8),tw=TILE_WIDTH),1,['north','east','south','west']
    #map_data=open_map('77')
    map_data=generate_map()
    for row_ind,row in enumerate(map_data):
        for column_ind,tile_data in enumerate(row):
            if tile_index[tile_data[0]] is not None:
                tiles.append(iso_tile((column_ind,row_ind),tile_data[1],TILE_WIDTH,SCREEN_WIDTH,tile_index[tile_data[0]]))
    tiles.sort(key=lambda x:x.vz)
    health=Health_Bar(5,200)
    hotbar=Hotbar(int(SCREEN_WIDTH-SCREEN_WIDTH/3),10,192,48,'assets/player/hotbar.png','assets/player/selected.png')#128 144
    inventory=Inventory(int(SCREEN_WIDTH/2-128),int(SCREEN_HEIGHT/2-144),256,288,'assets/player/inventory.png',hotbar)

    #Items and Item funcs
    def spawn_fireball():
        angs=[120,241,300,63.425]
        projectiles.append(Projectile((player.rect.centerx,player.rect.centery),32,32,8,angs[player.rotation],'fireball',5))
    it_fire=item('fire','assets/items/fire.png',10,spawn_fireball)
    it_apple=item('apple','assets/items/apple.png',5,lambda: health.heal(1))
    it_meat=item('meat','assets/items/meat.png',2,lambda: health.heal(3))

    #Giving items
    hotbar.add_item(it_fire)
    hotbar.add_item(it_apple)
    hotbar.add_item(it_meat)
    inventory.add_item(it_fire.diff_stack_size(5))
    inventory.add_item(item('sword','assets/items/crystal.png',func=lambda: health.damage(1)))

    #MAIN LOOP
    run = True
    while run:
        ###Inputs
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sysexit()
            if event.type == pyg.MOUSEBUTTONUP:
                if event.button == 1:
                    inventory.release_item()
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    hotbar.scroll(1)
                elif event.button == 5:
                    hotbar.scroll(-1)
                if event.button == 1:
                    if inventory_toggle:
                        inventory.pickup_item()
                    else:
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
                    #Screen shifting
                    if player.rect.centerx>=SCREEN_WIDTH-60:
                        shiftx-=TILE_WIDTH
                    if player.rect.centerx<=60:
                        shiftx+=TILE_WIDTH
                    if player.rect.centery>=SCREEN_HEIGHT-90:
                        shifty-=TILE_WIDTH
                    if player.rect.centery<=90:
                        shifty+=TILE_WIDTH
                if event.key == pyg.K_a:
                    player.rotate(-1)
                if event.key == pyg.K_d: 
                    player.rotate(1)
                if event.key == pyg.K_q:
                    if pan:
                        pan=False
                        shiftx,shifty=panx,pany
                    else:
                        pan=True
                        panx,pany=shiftx,shifty
                    print((round(player.vx,1),round(player.vy,1)),(player.rect.centerx,player.rect.centery),'\t\t',(round(player.on_x),round(player.on_y)),map_data[round(player.on_y)][round(player.on_x)],'\tpanning:',pan)
                if pan:
                    if event.key == pyg.K_RIGHT:
                        shiftx-=TILE_WIDTH
                    if event.key == pyg.K_LEFT:
                        shiftx+=TILE_WIDTH
                    if event.key == pyg.K_DOWN:
                        shifty-=TILE_WIDTH
                    if event.key == pyg.K_UP:
                        shifty+=TILE_WIDTH
                if event.key == pyg.K_e:
                    inventory_toggle=not inventory_toggle
        ###Mechanics
        run=health.update()
        #enemy pathfinding
        #enemy_p=pathfinding.get_path((round(enemy.vx),round(enemy.vy)),enemy_ds[enemy_d],(round(player.vx),round(player.vy)))
        def enemy_p_iter(p):
            global enemy_d
            if p=='left':
                enemy.rotate(-1)
                enemy_d-=1
            elif p=='right':
                enemy.rotate(1)
                enemy_d+=1
            elif p=='forward':
                if enemy.rotation==0:
                    enemy.vx+=1
                if enemy.rotation==2:
                    enemy.vx-=1
                if enemy.rotation==1:
                    enemy.vy+=1
                if player.rotation==3:
                    enemy.vy-=1
        #enemy_p_iter(enemy_p[0])
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
            
        #Drawing to screen
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
        #enemy.update(shiftx,shifty)
        #enemy.draw_img(SCREEN)

        player.update(shiftx,shifty)
        hotbar.draw(SCREEN,FONT2)
        health.draw(SCREEN)

        if inventory_toggle:
            inventory.update()
            inventory.draw(SCREEN)

        clock.tick(30)
        pyg.display.update()
    #DEATH SCREEN
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
