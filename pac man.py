from threading import Timer
from tkinter import*
import time
from random import*
root=Tk()
root.title("pac-man")

f1=Frame(root,bg="white")
f1.grid(row=0,column=0)
#-------------------------------------先定義空Timer，防止第一次執行副程式時出錯
def nothing():
    pass
t=Timer(0.01,nothing)
t.start()
g=Timer(0.01,nothing)
g.start()
l=Timer(0.01,nothing)
l.start()
#---------------------------------------------------------------------各單位初始位置
pacman_place=402
ghost1_place=195
ghost2_place=262
ghost3_place=264
ghost4_place=266
ghost_place_array=[195,262,264,266]
#----------------------------------------------------------------------移動參數、
sleep=0.246
gsleep=0.264
lw=0.05
move=0
move_r=0
move_l=0
move_u=0
move_d=0
#----------------------------------------------------------------------地圖大小
max_x=23
max_y=23
#-----------------------------------------------------------------------匯入圖片
ball=PhotoImage(file="wall.jpg")
pacman=PhotoImage(file="pacman2.jpg")
pacmanl=PhotoImage(file="pacmanl.png")
pacmanu=PhotoImage(file="pacmanu.png")
pacmand=PhotoImage(file="pacmand.png")
ghost1=PhotoImage(file="pinky.jpg")
ghost2=PhotoImage(file="inky.jpg")
ghost3=PhotoImage(file="clyde.jpg")
ghost4=PhotoImage(file="linky.jpg")
#=========================================================================================建立地圖
#---------------------------------------------------------------------------代表牆壁的Label編號
wall_array=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,\
            23,34,45,\
            46,48,49,50,52,53,54,55,57,59,60,61,62,64,65,66,68,\
            69,71,72,73,75,76,77,78,80,82,83,84,85,87,88,89,91,\
            92,117,118,119,121,123,124,125,126,127,128,129,131,133,134,135,137,\
            114,115,144,149,154,160,\
            138,162,163,164,165,167,168,169,170,172,174,175,176,177,179,180,181,182,183,\
            161,185,186,187,188,190,200,202,203,204,205,206,\
            184,208,209,210,211,213,215,216,217,219,220,221,223,225,226,227,228,229,\
            207,238,244,\
            253,254,255,256,257,259,261,267,269,271,272,273,274,275,\
            276,277, 278, 279, 280, 282, 284, 285, 286, 287, 288, 289, 290, 292, 294, 295, 296, 297,298,\
            299,300, 301, 302, 303, 305, 315, 317, 318, 319, 320,321,\
            322,323, 324, 325, 326, 328, 330, 331, 332, 333, 334, 335, 336, 338, 340, 341, 342, 343,344,\
            345,356,367,\
            368,370, 371, 372, 374, 375, 376, 377, 379, 381, 382, 383, 384, 386, 387, 388,390,\
            391,395, 409,413,\
            414,415, 416, 418, 420, 422, 423, 424, 425, 426, 427, 428, 430, 432, 434, 435,436,\
            437,443, 448, 453,459,\
            460,462, 463, 464, 465, 466, 467, 468, 469, 471, 473, 474, 475, 476, 477, 478, 479, 480,482,\
            483,505,\
            506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528]
#--------------------------------------------------------------------------中間籠子內的空間
box=[218,239,240,241,242,243,262,263,264,265,266]
wall_collision=[]
ghost1_wall=[]
ghost2_wall=[]
ghost3_wall=[]
ghost4_wall=[]
label=[]

#--------------------------------------------------------------------------所有座標初始值為"-"
for wc in range(23*23):
    wall_collision.append("-")
    ghost1_wall.append("-")
    ghost2_wall.append("-")
    ghost3_wall.append("-")
    ghost4_wall.append("-")
#--------------------------------------------------------------------------在各座標上建立Label
for i in range(0,max_x):
    for j in range(0,max_y):
        
        label.append(Label(f1,width=0,height=0))
        label[i*max_x+j].grid(row=i,column=j)
        label[i*max_x+j].config(text="●",bg="white",fg="pink")#-----------在所有Label顯示"●"
        for w in wall_array:#---------------------------------------------若Label的座標 等於 牆壁陣列的編號，將Label的圖片更該為牆壁的圖片
            if(i*max_x+j==w):
                label[i*max_x+j].config(bg="skyblue",text="",image=ball)
                wall_collision[w]=1
                ghost1_wall[w]=1
                ghost2_wall[w]=1
                ghost3_wall[w]=1
                ghost4_wall[w]=1
for b in box:#------------------------------------------------------------將籠子內的"●"清除
    label[b].config(text="●",fg="white",bg="white")


#-------------------------------------------------------------------------放置小精靈和鬼魂的圖片，並編號
label[pacman_place].config(image=pacman)
wall_collision[pacman_place]="p"
label[ghost1_place].config(text="",image=ghost1)
#wall_collision[ghost1_place]="g"
label[ghost2_place].config(text="",image=ghost2)
#wall_collision[ghost2_place]="g"
label[ghost3_place].config(text="",image=ghost3)
#wall_collision[ghost3_place]="g"
label[ghost4_place].config(text="",image=ghost4)
#wall_collision[ghost4_place]="g"
#-------------------------------------------------------------------------偷懶用的陣列
a=[wall_collision[pacman_place+1],wall_collision[pacman_place-1],\
   wall_collision[pacman_place-23],wall_collision[pacman_place+23]]
#-------------------------------------------------------------------------檢查編號用的含式
def test_wall():
    global wall_collision,ghost_wall
    for a in range(0,23):
        for b in range(0,23):
            print(wall_collision[a*23+b],end="")
        print("\n")
    
    g.cancel()

#===============================================================================================地圖建立
def eat():
    global wall_collision,pacman_place,move
    for i in range(23*23):
        if(wall_collision[i]!="-" and wall_collision[i]!="p" and wall_collision[i]!=1):
            label[i].config(image="",text="")
  
def lose():
    
    global ghost_place_array,pacman_place,gsleep,lw
    for i in ghost_place_array:
        if(i==pacman_place):
            f1.destroy()
            
            f2=Frame(root)
            label_lose=Label(f2,text="GAME OVER")
            label_lose.grid(row=0,column=0)
            label_lose.config(font=("algerian",100,"underline"))
            f2.grid(row=0,column=0)
            lw=1000000
            
    dd=[]
    for j in wall_collision:
        if(j=="x"):
            dd.append(0)
   
    
    if(len(dd)==228):
        f1.destroy()
        f3=Frame(root)
        label_win=Label(f3,text="YOU WIN")
        label_win.grid(row=0,column=0)
        label_win.config(font=("algerian",100,"underline"))
        f3.grid(row=0,column=0)
        
        
        lw=1000000
    l=Timer(lw,lose)
    l.start()

lose()    
#=====================================================================小精靈移動 ***
def pacman_moveright(none):
    global pacman_place,stopmove,move,move_r,move_l,move_u,move_d,t
    
 
    
    move=1
    if(wall_collision[pacman_place+move]!=1):
        t.cancel()
    
    if(pacman_place==252):
        wall_collision[pacman_place]="x"
        label[pacman_place].config(image="",text="")
        pacman_place=230
        
        wall_collision[pacman_place]="p"
        label[pacman_place].config(image=pacman)
        t=Timer(sleep,pacman_moveright,[0])
        eat()
        
        t.start()
    elif(wall_collision[pacman_place+move]!=1):
        
        wall_collision[pacman_place]="x"
        label[pacman_place].config(image="",text="●",fg="pink")
        pacman_place+=move
        
        wall_collision[pacman_place]="p"
        label[pacman_place].config(image=pacman)
        
        t=Timer(sleep,pacman_moveright,[0])
        eat()
        
        t.start()
    
def pacman_moveleft(none):
    global pacman_place,stopmove,move,move_r,move_l,move_u,move_d,t
    
    
    
    move=-1
    if(wall_collision[pacman_place+move]!=1):
        t.cancel()
   
    if(pacman_place==230):
        wall_collision[pacman_place]="x"
        label[pacman_place].config(image="",text="")
        pacman_place=252
        
        wall_collision[pacman_place]="p"
        label[pacman_place].config(image=pacmanl)
        t=Timer(sleep,pacman_moveleft,[0])
        eat()
        
        t.start()
    elif(wall_collision[pacman_place+move]!=1):
        
        wall_collision[pacman_place]="x"
        label[pacman_place].config(image="",text="●",fg="pink")
        pacman_place+=move
        
        wall_collision[pacman_place]="p"
        label[pacman_place].config(image=pacmanl)
        t=Timer(sleep,pacman_moveleft,[0])
        eat()
        
        t.start()
    
def pacman_moveup(none):
    global pacman_place,stopmove,move,move_r,move_l,move_u,move_d,t
    
   
    
    move=-23
    if(wall_collision[pacman_place+move]!=1):
         t.cancel()
    
    if(wall_collision[pacman_place+move]!=1):
        
        wall_collision[pacman_place]="x"
        label[pacman_place].config(image="",text="●",fg="pink")
        pacman_place+=move
       
        wall_collision[pacman_place]="p"
        label[pacman_place].config(image=pacmanu)
        t=Timer(sleep,pacman_moveup,[0])
        eat()
        
        t.start()
        
def pacman_movedown(none):
    global pacman_place,stopmove,move,move_r,move_l,move_u,move_d,t
    
    
    
    move=23
    if(wall_collision[pacman_place+move]!=1):
        t.cancel()
    
    if(wall_collision[pacman_place+move]!=1):
        
        wall_collision[pacman_place]="x"
        label[pacman_place].config(image="",text="●",fg="pink")
        pacman_place+=move
        
        wall_collision[pacman_place]="p"
        label[pacman_place].config(image=pacmand)
        t=Timer(sleep,pacman_movedown,[0])
        eat()
        
        t.start()
        
#===================================================================鬼魂移動  so lag

g1="g"
g1_code=0
g2="h"
g2_code=1
g3="o"
g3_code=2
g4="s"
g4_code=3
ghost_wall=[ghost1_wall,ghost2_wall,ghost3_wall,ghost4_wall]

dont_back=[25,25,25,25]
count=1
count_out=0
def ghost_move(ghost_place,ghost_image,g,g_code):
    
    global ghost_wall,count,wall_collision,dont_back,gsleep,ghost_place_array,count_out
        
    a=[ghost_wall[g_code][ghost_place+1],ghost_wall[g_code][ghost_place-1],\
        ghost_wall[g_code][ghost_place+23],ghost_wall[g_code][ghost_place-23]]
    b=[1,-1,23,-23]
    move_ran=[]
    ghost_wall[g_code][ghost_place]=g
    
        
    if(wall_collision[ghost_place]!="-"):
        label[ghost_place].config(image="",text="",bg="white")
      
    else:
        label[ghost_place].config(image="",text="●",fg="pink")
    for j in box:
        label[j].config(text="")
    if(count_out>=5):
        wall_collision[218]=1
        label[218].config(image="",text="一",fg="skyblue")
    if(ghost_place==241 or ghost_place==218 ):#------------------------出籠子的情況
        move_ran.append(b[3])
        count_out+=1
        print(count_out)
    else:
        for i in range(0,4):
            if(a[i]!=1 and a[i]!=g):
                move_ran.append(b[i])
#-----------------------------------------------------
    if(ghost_place==230):                           #穿
        if(count==1):                               #過
            move_ran.append(22)                     #通
            count=0                                 #道
        else:                                       #的
            count=1                                 #特
                                                    #殊
    if(ghost_place==252):                           #狀
        if(count==1):                               #況
            move_ran.append(-22)
            count=0
        else:
            count=1
#-----------------------------------------------------
    ghost_wall[g_code][dont_back[g_code]]="-"
    if(ghost_place==195):
        ghost_wall[g_code][218]=1
    x=len(move_ran)
    gmove=randint(0,x-1)
    
        
    ghost_place+=move_ran[gmove]
    
    
        
    
        
        
    ghost_wall[g_code][ghost_place-move_ran[gmove]]=1
    ghost_wall[g_code][ghost_place]=g
    dont_back[g_code]=ghost_place-move_ran[gmove]
    
    label[ghost_place].config(image=ghost_image)
    ghost_place_array[g_code]=ghost_place
    '''print(ghost_place-move_ran[gmove])
    print(ghost_place)
    print(move_ran)
    print(b[gmove])
    print(x)'''
    
    g=Timer(gsleep,ghost_move,[ghost_place,ghost_image,g,g_code])
    g.start()
#-------------------------------------------------------按鍵事件
root.bind("<KeyRelease-Up>",lambda none=0:pacman_moveup(none))
root.bind("<KeyRelease-Down>",lambda none=0:pacman_movedown(none))
root.bind("<KeyRelease-Right>",lambda none=0:pacman_moveright(none))
root.bind("<KeyRelease-Left>",lambda none=0:pacman_moveleft(none))

ghost_move(ghost1_place,ghost1,g1,g1_code)
ghost_move(ghost2_place,ghost2,g2,g2_code)
ghost_move(ghost3_place,ghost3,g3,g3_code)
ghost_move(ghost4_place,ghost4,g4,g4_code)

    

#-----------------------------------------------------------------測試用視窗
#test=Tk()
#Button(test,text="test_wall",command=lambda :test_wall()).grid(row=0,column=0)


root.mainloop()
