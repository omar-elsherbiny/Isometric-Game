import math
from perlin_noise import PerlinNoise
from random import choice,randint

def pos_from_ang(center,angle,dist,rnd=False):
    cx,cy=center
    nx=math.cos(math.radians(angle-90))*dist+cx
    ny=math.sin(math.radians(angle-90))*dist+cy
    if rnd:
        return (round(nx),round(ny))
    return (nx,ny)

def two_point_ang(p1,p2):
    angle=int(math.degrees(math.atan2(p2[1]-p1[1],p2[0]-p1[0])))
    if angle<0:
        angle+=360
    return angle

def adjust(pos,tw):
    x,y=pos
    return (x-(tw/2),y)

def open_map(num='00'):
    data=[]
    with open(f'assets/maps/{num}.txt', 'r') as f:
        lines=f.readlines()
        for row_ind,row in enumerate(lines):
            row_data=[]
            for column_ind,tile in enumerate(row.split('\n')[0]):
                if row_ind<=column_ind:
                    z_axis=column_ind
                else:
                    z_axis=row_ind
                row_data.append((int(tile),z_axis))
            data.append(row_data)
    return data
def generate_map():
    noise=PerlinNoise(octaves=5)
    noise2=PerlinNoise(octaves=5)
    noise3=PerlinNoise(octaves=1)
    xpix, ypix = 60, 60
    perlin_map=[[0 if noise([i/xpix, j/ypix])<0 else 3 for j in range(xpix)] for i in range(ypix)]
    perlin_map2=[[0 if noise2([i/xpix, j/ypix])<0 else 4 for j in range(xpix)] for i in range(ypix)]
    perlin_map3=[[0 if noise3([i/xpix, j/ypix])<0 else 1 for j in range(xpix)] for i in range(ypix)]
    perlin_map[1][1]=5

    data=[]
    for row_ind,row in enumerate(perlin_map):
        row_data=[]
        for column_ind,tile in enumerate(row):
            if row_ind<=column_ind:
                z_axis=column_ind
            else:
                z_axis=row_ind
            if tile==0:
                if perlin_map2[row_ind][column_ind]==0:
                    tile=perlin_map3[row_ind][column_ind]
                else:
                    tile=perlin_map2[row_ind][column_ind]
            row_data.append((int(tile),z_axis))
        data.append(row_data)
    return data

def coords_from_grid_index(ind, grid_size, res='x/y'):
    result=(ind%grid_size[0], int(ind/grid_size[0]))
    if res=='x':
        return result[0]
    elif res=='y':
        return result[1]
    return result
def grid_index_from_coords(coords, grid_size):
    """x coord starts from 1, y starts from 0"""
    return coords[0]+(grid_size[0]*coords[1])

class iso_tile:
    def __init__(self, pos_xy, pos_z, tw=64, sw=600, image='assets/stone.png'):
        vx,vy=pos_xy
        x=(vx-vy)*(tw/2)
        y=(vx+vy)*(tw/4)
        self.rect=pyg.Rect(x+((sw/2)-(tw/2)),y/1.02+25,tw,tw)#+((sw-tw)/2) mid

        self.vx,self.vy=pos_xy
        self.vz=pos_z

        self.tw,self.sw=tw,sw## convert alpha???
        if isinstance(image,list):
            self.image=pyg.transform.scale(pyg.image.load(choice(image)).convert_alpha(),(tw,tw))
        else:
            self.image=pyg.transform.scale(pyg.image.load(image).convert_alpha(),(tw,tw))

        leng=self.tw/2
        self.middle=((self.tw/2)+self.rect.x,(self.tw/2)+self.rect.y)
        self.top=pos_from_ang(self.middle,0,leng)
        self.top_right=pos_from_ang(self.middle,63.435,leng*1.1185,True)
        self.top_left=pos_from_ang(self.middle,-63.435,leng*1.1185,True)
        self.bottom=pos_from_ang(self.middle,180,leng)
        self.bottom_right=pos_from_ang(self.bottom,63.435,leng*1.1185,True)
        self.bottom_left=pos_from_ang(self.bottom,-63.435,leng*1.1185,True)

    def special(self,img,w,h):
        self.image=pyg.transform.scale(pyg.image.load(img).convert_alpha(),(w,h))
        return self

    def shift_tile(self,shiftx=0,shifty=0):
        x=(self.vx-self.vy)*(self.tw/2)
        y=(self.vx+self.vy)*(self.tw/4)
        self.rect.x=x+((self.sw/2)-(self.tw/2))+shiftx
        self.rect.y=y/1.02+25+shifty
        leng=self.tw/2
        self.middle=((self.tw/2)+self.rect.x,(self.tw/2)+self.rect.y)
        self.top=pos_from_ang(self.middle,0,leng)
        self.top_right=pos_from_ang(self.middle,63.435,leng*1.1185,True)
        self.top_left=pos_from_ang(self.middle,-63.435,leng*1.1185,True)
        self.bottom=pos_from_ang(self.middle,180,leng)
        self.bottom_right=pos_from_ang(self.bottom,63.435,leng*1.1185,True)
        self.bottom_left=pos_from_ang(self.bottom,-63.435,leng*1.1185,True)
    
    def draw_hitbox(self,screen):
        pyg.draw.polygon(screen, (240,0,0), (self.top,self.top_right,self.middle,self.top_left))
        pyg.draw.polygon(screen, (0,240,0), (self.middle,self.top_right,self.bottom_right,self.bottom))
        pyg.draw.polygon(screen, (0,0,240), (self.middle,self.top_left,self.bottom_left,self.bottom))

    def draw_img(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def draw_back_box(self,screen):
        pyg.draw.rect(screen, (240,240,240), (self.rect.x, self.rect.y, self.rect.w, self.rect.h))

class iso_player(iso_tile):
    def __init__(self, pos_xy, tw=64, sw=600, image='assets/player/01.png'):
        super().__init__(pos_xy,1,tw,sw,image)
        self.rotation=0
        self.on_x=self.vx+1.2
        self.on_y=self.vy+1.2
        self.anim_duration=0
        self.anim_buffer=0

    def update(self,shiftx=0,shifty=0):
        self.on_x=self.vx+1.2
        self.on_y=self.vy+1.2
        x=(self.vx-self.vy)*(self.tw/2)
        y=(self.vx+self.vy)*(self.tw/4)
        self.rect.x=x+((self.sw/2)-(self.tw/2))+shiftx
        self.rect.y=y/1.02+25+shifty
        leng=self.tw/2
        self.middle=((self.tw/2)+self.rect.x,(self.tw/2)+self.rect.y)
        self.top=pos_from_ang(self.middle,0,leng)
        self.top_right=pos_from_ang(self.middle,63.435,leng*1.1185,True)
        self.top_left=pos_from_ang(self.middle,-63.435,leng*1.1185,True)
        self.bottom=pos_from_ang(self.middle,180,leng)
        self.bottom_right=pos_from_ang(self.bottom,63.435,leng*1.1185,True)
        self.bottom_left=pos_from_ang(self.bottom,-63.435,leng*1.1185,True)

        if self.rotation<=1:
            self.image=self.image=pyg.transform.scale(pyg.image.load(f'assets/player/{self.rotation}{self.anim_buffer}.png').convert_alpha(),(self.tw,self.tw))
        else:
            self.image=self.image=pyg.transform.scale(pyg.image.load(f'assets/player/{self.rotation}0.png').convert_alpha(),(self.tw,self.tw))

        if self.anim_duration>0:
            self.anim_duration-=1
        else:
            self.anim_buffer+=1
        if self.anim_buffer>=4:
            self.anim_duration=randint(50,100)
            self.anim_buffer=0

    def rotate(self,val):
        self.rotation=(self.rotation+val)%4

    def draw_hitbox(self, screen):
        pyg.draw.polygon(screen, (240,0,0), (self.top,self.top_right,self.middle,self.top_left),1)
        pyg.draw.polygon(screen, (0,240,0), (self.middle,self.top_right,self.bottom_right,self.bottom),1)
        pyg.draw.polygon(screen, (0,0,240), (self.middle,self.top_left,self.bottom_left,self.bottom),1)
        if self.rotation==0:
            eye_pos=((self.middle[0]+self.top_right[0])/2,(self.middle[1]+self.top_right[1])/2)
            ang=120
        elif self.rotation==1:
            eye_pos=((self.middle[0]+self.top_left[0])/2,(self.middle[1]+self.top_left[1])/2)
            ang=-120
        elif self.rotation==2:
            eye_pos=((self.top[0]+self.top_left[0])/2,(self.top[1]+self.top_left[1])/2)
            ang=-60
        elif self.rotation==3:
            eye_pos=((self.top[0]+self.top_right[0])/2,(self.top[1]+self.top_right[1])/2)
            ang=60
        pyg.draw.line(screen, (0,255,160), eye_pos, pos_from_ang(eye_pos,ang,100),3)
        onx=(round(self.on_x)-round(self.on_y))*(self.tw/2)
        ony=(round(self.on_x)+round(self.on_y))*(self.tw/4)
        onpos=(onx+(self.sw/2),ony+(self.tw/4))
        pyg.draw.circle(screen, (255,0,160), [int(pos) for pos in onpos],5)
        pyg.draw.circle(screen, (160,0,255), (self.rect.centerx,self.rect.centery),5)
        pyg.draw.line(screen, (0,160,255), (0,self.sw-90), (self.sw,self.sw-90),3)
        pyg.draw.line(screen, (0,160,255), (0,20), (self.sw,20),3)
        pyg.draw.line(screen, (0,160,255), (60,0), (60,self.sw),3)
        pyg.draw.line(screen, (0,160,255), (self.sw-60,0), (self.sw-60,self.sw),3)

class item:
    def __init__(self, id, icon, count=None, func=lambda *args: None):
        self.id=id
        self.icon=icon
        self.count=count
        self.func=func
    def diff_stack_size(self, count):
        return item(self.id,self.icon,count,self.func)
class Hotbar:
    def __init__(self, x, y, w, h, img, selector_img):
        self.rect = pyg.Rect(x, y, w, h)
        self.selectx=x+round(w/64)
        self.selecty=y+round(h/16)
        self.item_ind=0
        self.items=[]

        self.image=pyg.transform.scale(pyg.image.load(img).convert_alpha(),(w,h))
        self.selector=pyg.transform.scale(pyg.image.load(selector_img).convert_alpha(),(round(w*0.21875),round(h*0.875)))

    def scroll(self,num):
        if num>0 and self.item_ind<4:
            self.item_ind+=num
            self.selectx+=round(self.rect.w/64)*12
        elif num<0 and self.item_ind>0:
            self.item_ind+=num
            self.selectx-=round(self.rect.w/64)*12
        elif num>0 and self.item_ind>=4:
            self.item_ind=0
            self.selectx=self.rect.x+round(self.rect.w/64)
        elif num<0 and self.item_ind<=0:
            self.item_ind=4
            self.selectx=self.rect.x+round(self.rect.w/64)+round(self.rect.w/64)*12*4

    def use_item(self):
        if self.item_ind+1 <= len(self.items):
            self.items[self.item_ind].func()
            if self.items[self.item_ind].count is not None: 
                if self.items[self.item_ind].count>1:
                    self.items[self.item_ind].count-=1
                else:
                    self.items.pop(self.item_ind)

    def add_item(self, item):
        if len(self.items)<5:
            if item.id in [i.id for i in self.items] and item.count is not None:
                self.items[[i.id for i in self.items].index(item.id)].count+=item.count
            else:
                self.items.append(item)

    def draw(self,screen,font):
        if self.item_ind+1 <= len(self.items):
            if self.items[self.item_ind].count is not None:
                countNum=font.render(f'{self.items[self.item_ind].count}', False, (46,230,116),(24,24,26))
            else:
                countNum=font.render('', False, (46,230,116),(24,24,26))
            countRect=countNum.get_rect(center=(self.rect.x+(round(self.rect.w/64)*13*(self.item_ind+1)-round(self.rect.w/64)*7), self.selecty+round(self.rect.h/16)*18))
            screen.blit(countNum, countRect)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        for ind,item in enumerate(self.items):
            ico=pyg.transform.scale(pyg.image.load(item.icon).convert_alpha(),(round(self.rect.w*0.21875),round(self.rect.h*0.875)))
            screen.blit(ico, (self.rect.x+round(self.rect.w/64)+round(self.rect.w/64)*12*ind, self.selecty))
        screen.blit(self.selector, (self.selectx, self.selecty))
class Inventory:
    def __init__(self, x, y, w, h, img, hotbar):
        self.rect = pyg.Rect(x, y, w, h)
        self.item_ind=0
        self.items=[]
        self.hotbar=hotbar
        self.holding=None

        self.image=pyg.transform.scale(pyg.image.load(img).convert_alpha(),(w,h))

    def update(self):
        mx,my=pyg.mouse.get_pos()#round((mx-mx%(self.rect.w/5))+(self.rect.x%(self.rect.w/5)))
        sx,sy=round(mx-((mx-self.rect.x)%(self.rect.w/5))),round(my-((my-self.rect.y)%(self.rect.h/5)))
        if self.rect.left<=sx<=self.rect.right and self.rect.left<=mx<=self.rect.right and self.rect.top<=sy<=self.rect.bottom and self.rect.top<=my<=self.rect.bottom:
            ix,iy=round(sx/(self.rect.w/5)-self.rect.x/(self.rect.w/5)),round(sy/(self.rect.h/5)-self.rect.y/(self.rect.h/5))
            self.item_ind=grid_index_from_coords((ix,iy), (5,5))
    
    def pickup_item(self):
        if self.item_ind<len(self.items):
            self.holding=self.items[self.item_ind]
            self.items.pop(self.item_ind)
        elif self.item_ind>=20 and self.item_ind-20<len(self.hotbar.items):
            self.holding=self.hotbar.items[self.item_ind-20]
            self.hotbar.items.pop(self.item_ind-20)

    def release_item(self):
        if self.holding!=None:
            if self.item_ind<=19:
                if len(self.items)<20:
                    if self.holding.id in [i.id for i in self.items] and self.holding.count is not None:
                        self.items[[i.id for i in self.items].index(self.holding.id)].count+=self.holding.count
                    else:
                        self.items.insert(self.item_ind, self.holding)
                else:
                    self.hotbar.items.append(self.holding)
            elif len(self.hotbar.items)<5:
                if self.holding.id in [i.id for i in self.hotbar.items] and self.holding.count is not None:
                    self.hotbar.items[[i.id for i in self.hotbar.items].index(self.holding.id)].count+=self.holding.count
                else:
                    self.hotbar.items.insert(self.item_ind-20, self.holding)
            else:
                self.items.append(self.holding)
            self.holding=None

    def add_item(self, item):
        if len(self.items)<20:
            if item.id in [i.id for i in self.items] and item.count is not None:
                self.items[[i.id for i in self.items].index(item.id)].count+=item.count
            else:
                self.items.append(item)

    def draw(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        for ind,item in enumerate(self.items):
            ico=pyg.transform.scale(pyg.image.load(item.icon).convert_alpha(),(round(self.rect.w*0.21875),round(self.rect.h*0.19445)))
            screen.blit(ico, (self.rect.x+round(self.rect.w/64)+round(self.rect.w/64)*12*coords_from_grid_index(ind,(5,5),'x'), round(self.rect.y+(self.rect.h/64)+(self.rect.h/64)*11.65*coords_from_grid_index(ind,(5,5),'y'))))
        for ind,item in enumerate(self.hotbar.items):
            ico=pyg.transform.scale(pyg.image.load(item.icon).convert_alpha(),(round(self.rect.w*0.21875),round(self.rect.h*0.19445)))
            screen.blit(ico, (self.rect.x+round(self.rect.w/64)+round(self.rect.w/64)*12*coords_from_grid_index(ind+20,(5,5),'x'), round(self.rect.y+(self.rect.h/64)+(self.rect.h/64)*12.4*coords_from_grid_index(ind+20,(5,5),'y'))))
        if self.holding!=None:
            ico=pyg.transform.scale(pyg.image.load(self.holding.icon).convert_alpha(),(round(self.rect.w*0.21875),round(self.rect.h*0.19445)))
            screen.blit(ico, (pyg.mouse.get_pos()[0]-round(self.rect.w*0.21875/2),pyg.mouse.get_pos()[1]-round(self.rect.h*0.19445/2)))

class Health_Bar:
    def __init__(self, max_health, bar_w, death_func=None, bar_h=25, bar_x=10, bar_y=10, color=(240, 240, 240)):
        self.x = bar_x
        self.y = bar_y
        self.h = bar_h
        self.max_bar_len = bar_w

        self.color1 = (0, 200, 0)
        self.color2 = color
        self.color2_og = color
        self.outer_og = 2
        self.outer = self.outer_og

        self.func = death_func
        self.max = max_health
        self.current = max_health

    def heal(self, amount):
        if self.current + amount < self.max:
            self.current += amount
            if self.outer <=10:
                self.outer += 6
            self.color2 = (0, 240, 0)
        elif self.current <= self.max:
            self.current = self.max
            if self.outer <=10:
                self.outer += 6
            self.color2 = (0, 240, 0)

    def damage(self, amount):
        if self.current - amount >= 0:
            self.current -= amount
            if self.outer <=10:
                self.outer += 6
            self.color2 = (240, 0, 0)
        elif self.current >= 0:
            self.current = 0
            if self.outer <=10:
                self.outer += 6
            self.color2 = (240, 0, 0)

    def regenerate(self, regeneration_percent):
        if self.current == self.max * regeneration_percent / 100:
            self.heal(self.max-self.current)

    def update(self):
        if self.outer > self.outer_og:
            self.outer -= 1
        if self.outer == self.outer_og:
            self.color2 = self.color2_og

        if self.current <= self.max / 4.5:
            self.color1 = (200, 0, 0)
        elif self.current <= self.max / 2:
            self.color1 = (220, 200, 0)
        else:
            self.color1 = (0, 200, 0)

        if self.current <= 0:
            return False
        return True

    def draw(self, screen):
        pyg.draw.rect(screen, self.color1, (self.x, self.y, self.current / (self.max / self.max_bar_len), self.h))
        pyg.draw.rect(screen, self.color2, (self.x - 1, self.y, self.max_bar_len, self.h), self.outer)

class Projectile:
    def __init__(self,origin,w,h,speed,direction,image,frames):
        self.ogx,self.ogy=origin
        self.rect=pyg.Rect(self.ogx,self.ogy,w,h)

        self.dist=0
        self.angle=direction
        self.speed=speed

        self.anim=0
        self.frames=frames
        self.image_name=image
        self.image=pyg.transform.rotate(pyg.transform.scale(pyg.image.load(f'assets/items/{image}0.png').convert_alpha(),(w,h)),(-direction+90)+180)
    def draw_update(self,screen):
        self.rect.centerx,self.rect.centery=pos_from_ang((self.ogx,self.ogy),self.angle,self.dist,True)
        self.dist+=self.speed

        self.anim+=0.2
        if self.anim>=(self.frames-1):
            self.anim=0
        self.image=pyg.transform.rotate(pyg.transform.scale(pyg.image.load(f'assets/items/{self.image_name}{round(self.anim)}.png').convert_alpha(),(self.rect.w,self.rect.h)),(-self.angle+90)+180)
        screen.blit(self.image, (self.rect.x, self.rect.y))

if __name__ =='__main__':
    map_data=generate_map()