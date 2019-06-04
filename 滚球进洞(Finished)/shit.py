import pygame
import sys
from random import *
from pygame.locals import *
import traceback

#继承自pygame的精灵类
class Ball(pygame.sprite.Sprite):
    def __init__(self,image,image2,position,speed,size,target):
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load(image).convert_alpha()
        self.image2=pygame.image.load(image2).convert_alpha()
        #获得小球位置
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=position

        #小球运动的速率
        self.speed=speed
        self.collide=False

        #表示用来控制球
        self.target=target
        self.control=False

        #背景图片尺寸
        self.width,self.height=size[0],size[1]

        #球的半径
        self.radius=self.rect.width/2

    def move(self):
        self.rect=self.rect.move(self.speed)

        #判断是否越界,如果越界则从另一个边界出来
        if self.rect.right<0:
            self.rect.left=self.width
        elif self.rect.left>self.width:
            self.rect.right=0
        elif self.rect.bottom<0:
            self.rect.top=self.height
        elif self.rect.top>self.height:
            self.rect.bottom=0

    def check(self,motion):
        if self.target<motion<self.target+5:
            return True
        else:
            return False

class Glass(pygame.sprite.Sprite):
    def __init__(self,glass_image,bg_size,mouse_image):
        #初始化动画精灵
        pygame.sprite.Sprite.__init__(self)

        self.glass_image=pygame.image.load(glass_image).convert_alpha()
        self.glass_rect=self.glass_image.get_rect()
        self.glass_rect.left,self.glass_rect.top=\
                    (bg_size[0]-self.glass_rect.width)//2,\
                    (bg_size[1]-self.glass_rect.height)

        self.mouse_image=pygame.image.load(mouse_image).convert_alpha()
        self.mouse_rect=self.mouse_image.get_rect()
        self.mouse_rect.left,self.mouse_rect.top=\
                    self.glass_rect.left,self.glass_rect.top

        #设置鼠标是否可见
        pygame.mouse.set_visible(False)

def main():
    pygame.init()
    #pygame.mixer.pre_init(44100,16,2,4096)

    ball_img='test.gif';ball_img2='shi.gif'
    bg_img='background.png';mouse_img='hand.png';glass_img='glass.png'

    running=True

    #添加背景音乐
    pygame.mixer.music.load('bg_music.ogg')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

    #添加音效
    loser_sound=pygame.mixer.Sound('loser.wav')
    laugh_sound=pygame.mixer.Sound('laugh.wav')
    winner_sound=pygame.mixer.Sound('winner.wav')
    hole_sound=pygame.mixer.Sound('hole.wav')

    #音乐播放完游戏结束
    GAMEOVER=USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)

    #根据背景图片设置游戏尺寸
    size=width,height=1024,681
    screen=pygame.display.set_mode(size)
    pygame.display.set_caption('滚屎进洞')
    background=pygame.image.load(bg_img).convert_alpha()

    #每个洞的范围(x1,x2,y1,y2)
    hole=[(115,120,195,202),(222,228,387,393),(500,506,318,324),\
          (695,702,190,195),(904,909,416,424)]
    msgs=[]

    #存放球
    balls=[]
    group=pygame.sprite.Group()

    #控制球的选装
    rotate_ball=0

    #设置每一个球
    for i in range(5):
        position=randint(0,width-100),randint(0,height-100)
        speed=[randint(-10,10),randint(-10,10)]
        ball=Ball(ball_img,ball_img2,position,speed,size,5*(i+1))

        #当球初始化碰见时改变位置
        while pygame.sprite.spritecollide(ball,group,False,pygame.sprite.collide_circle):
            ball.rect.left,ball.rect.top=randint(0,width-100),randint(0,height-100)
        balls.append(ball)
        group.add(ball)

    #初始化摩擦玻璃
    glass=Glass(glass_img,size,mouse_img)

    #记录鼠标每秒钟产生时间数量
    motion=0
    #计时器
    MYTIMER=USEREVENT+1
    pygame.time.set_timer(MYTIMER,1000)

    #key的重复操作,100毫秒后开始,每100毫秒响应一次
    pygame.key.set_repeat(100,100)

    #控制游戏帧率
    clock=pygame.time.Clock()

    #程序开始循环
    while running:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

            #当背景音乐播放完时,游戏停止
            if event.type==GAMEOVER:
                loser_sound.play()
                pygame.time.delay(2000)
                laugh_sound.play()
                running=False

            if event.type==MYTIMER:
                if motion:
                    for each in group:
                        if each.check(motion):
                            each.speed=[0,0]
                            each.control=True
                    motion=0

            if event.type==MOUSEMOTION:
                motion+=1

            #获得控制权后,控制球的移动
            if event.type==KEYDOWN:
                if event.key==K_w:
                    for each in group:
                        if each.control:
                            each.speed[1]-=1

                if event.key==K_s:
                    for each in group:
                        if each.control:
                            each.speed[1]+=1

                if event.key==K_a:
                    for each in group:
                        if each.control:
                            each.speed[0]-=1

                if event.key==K_d:
                    for each in group:
                        if each.control:
                            each.speed[0]+=1

                #判断球是否落入洞中
                if event.key==K_SPACE:
                    for each in group:
                        if each.control:
                            for i in hole:
                                if i[0]<=each.rect.left<=i[1] and \
                                   i[2]<=each.rect.top<=i[3]:
                                    hole_sound.play()
                                    each.speed=[0,0]
                                    group.remove(each)
                                    temp=balls.pop(balls.index(each))
                                    balls.insert(0,temp)
                                    hole.remove(i)

                            #当洞被填满时:
                            if not hole:
                                pygame.mixer.music.stop()
                                winner_sound.play()
                                pygame.time.delay(3000)
                                msg=pygame.image.load('win.png').convert_alpha()
                                msg_pos=(width-msg.get_width())//2,\
                                         (height-msg.get_height())//2
                                msgs.append((msg,msg_pos))
                                laugh_sound.play

        #绘制背景,然后绘制玻璃板
        screen.blit(background,(0,0))
        screen.blit(glass.glass_image,glass.glass_rect)

        #设置样式鼠标随着鼠标移动
        glass.mouse_rect.left,glass.mouse_rect.top=pygame.mouse.get_pos()
        if glass.mouse_rect.left<glass.glass_rect.left:
            glass.mouse_rect.left=glass.glass_rect.left
        if glass.mouse_rect.right>glass.glass_rect.right:
            glass.mouse_rect.right=glass.glass_rect.right
        if glass.mouse_rect.top<glass.glass_rect.top:
            glass.mouse_rect.top=glass.glass_rect.top
        if glass.mouse_rect.bottom>glass.glass_rect.bottom:
            glass.mouse_rect.bottom=glass.glass_rect.bottom
        
        #绘制样式鼠标
        screen.blit(glass.mouse_image,glass.mouse_rect)

        for each in balls:
            each.move()
              
            if each.collide:
                each.speed=[randint(-10,10),randint(-10,10)]
                each.collide=False
            if each.control:
                #被控制的时候画另一张图
                screen.blit(each.image2,each.rect)
            else:
                screen.blit(each.image,each.rect)

        for each in group:
            group.remove(each)
            
            #判断球是否相互碰撞
            if pygame.sprite.spritecollide(each,group,False,pygame.sprite.collide_circle):

                each.collide=True
                #如果球受控制,碰撞后失控
                if each.control:
                    each.control=False
                each.speed[0]=-each.speed[0]
                each.speed[1]=-each.speed[1]

            group.add(each)

        #当胜利时的画面
        for msg in msgs:
            screen.blit(msg[0],msg[1])

        #显示更新的界面
        pygame.display.flip()
        #帧率
        clock.tick(30)
        
if __name__=='__main__':
    try:
        main()
    except SystemError:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
