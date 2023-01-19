#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 05:21:39 2023

@author: spot
"""

#Airhockey:
    #Hi, as per your advice, I have tried making this project. In this, I have 
    #tried to make an game that mimics behaviour of AirHockey (not excatly, but
    #that can be fine tuned later). To do so, I have used 'PyGame' and further 
    #I have also extended this with use of 'PyQt' interface that help in 
    #controlling the parameters of this game.

#Information about this game:
    #It's a one player game in which the player gets a bar to control and 
    #defend the puck from going behind it. Whenever the puck would hit the bar
    #opposite to player bar, it would get reflected with some degree of 
    #randomness in direction of puck from the natural one(i.e. the one 
    #described by the laws of momentum, thus giving an real-life senario to 
    #some extent. Similarly, whenever the puck will hit playe bar, it will get 
    #reflected, but this time it won't be random, rather it will be with some 
    #degree sphericity(i.e. If the puck would hit the edge of player bar it 
    #would get deviated from laws of reflection by a given value of  
    #max. deviation. But, when the puck would hit the centre of bar it would 
    #just follow the laws of reflection(i.e. zero deviation). The more away the
    #puck hits a point from the centre on the player bar, the more it deviates.
    #(Just like a circular airhockey stick).

    #Further, I have tried to integrate PyQt and PyGame to control in game 
    #parameters like "Player speed", "Puck Speed", "screen width", 
    #"screen height", "Deviation range on opponent side", "Maximum deviation 
    #on player's side" and also to control operations like "Restart", "Quit".
    
#Gameplay and Game controls:
    #To play the game, you just have to run the below code. Once runned, it
    #would prompt you to game controls screen. Click continue and then the game
    #will start. You can change the parameter from the parameter window. To 
    #start the gameplay, press "SPACEBAR" and the gameplay will start. (Don't 
    #for to clik on the pygame window. You can control player bar with "LEFT" 
    #and "RIGHT" keys. To pause the game press "SPACEBAR" again.

    
    
#Note: 
    #The changes in "puck's speed" is based on loops/sec. So, if incase any 
    #kind of lag is seen in the puck's motion after increasing the speed then 
    #try dereasing the screen size from game parameters. 
    
    #p.s. If you want to see what kind of deviations I have applied, try 
    #keeping either side's deviation as 0 in order to obser opposite sides 
    #deviation mechanism. i.e. for seeing deviation mechanism on player's 
    #side, leep opponent'sside deviation as 0 and then see the way puck moves 
    #next time it hits the player bar (not move player bar so that the ball 
    #hits the edges. And similarly for seeing kind of deviation on opponent 
    #side, keep the payer side's deviation as 0.
    



##Note:
    #You will need PyGame, PyQt5 to run this game. Following are the 
    #'pip codes' for installing this, incase you don't have them already 
    #installed.
    
    #!pip install pygame
    #!pip install PyQt5
    
#----------------------------------------------------------------------------------------------


#Libraries
import random as rand
import numpy as np
import sys
from PyQt5.QtWidgets import (QLineEdit,QSlider,QPushButton,QVBoxLayout,QApplication, QWidget)
from PyQt5.QtCore import Qt
import pygame as pg
from pygame import *
import multiprocessing
from ctypes import c_bool
from multiprocessing import Value


#Defining some funtions and variables to ease things out:
pi=np.pi

def cos(x):
    f=np.cos(x)
    return f

def sin(x):
    f=np.sin(x)
    return f

def atan(x):
    f=np.arctan(x)
    return f

def rdev(x):
    f=rand.uniform(-x,x)
    return(f)

#Some colors:
orange=(255,100,0)
magenta=(250,50,250)
white=(255,255,255)
blue=(50,100,250)
grey=(200,200,200)
greend=(0,80,50)
red=(255,0,0)
green=(0,255,0)

#Defining some variables to be used---------------------------------------------------------------------------------------

#Defining controllabe initial variables:
bs=6     #Puck's speed
ps=20    #Player_speed
td=pi/4    #Deviation in angle at the edges of bar on player's side
md=pi/6      #Maximum range of randomness in deviation of opposite bar
sw=400      #screen-width
sh=600     #screen-height
fs=30      #loops per second

#Parameters of static elements of the game:
off=5      #Offset from edges
hpbar=10      #height of bar
wpbar=sw/3      #width of player's bar
wsbar=7     #Width of side bar
hsbar=sh-hpbar-2*off   #Height of side bar
hobar=7     #Height of opposite bar
wobar=sw-2*wsbar-2*off    #width of opposite bar

#Positioning of these elements:
#(x,y,width,height)
sbar1=(off,off,wsbar,hsbar)
sbar2=(sw-wsbar-off,off,wsbar,hsbar)
obar=(sw/2-wobar/2,off,wobar,hobar)




#-------------------------------------------------------------------------------------------------------------------






#PyQt5: 

#Qt Window at game start:------------------------------------------------------------------------------------------

class start(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        
        box=QVBoxLayout()
        
        self.pcl=QLineEdit()         
        self.pcl.setText('Player Control: use LEFT and RIGHT keys')
        self.pcl.setReadOnly(True)
        box.addWidget(self.pcl)
        
        self.pl=QLineEdit()         
        self.pl.setText('Pause and/or Resume: press SPACEBAR')
        self.pl.setReadOnly(True)
        box.addWidget(self.pl)
        
        self.p=QLineEdit()         
        self.p.setText('Game Parameter: Change from parameter window')
        self.p.setReadOnly(True)
        box.addWidget(self.p)
        
        self.q=QLineEdit()         
        self.q.setText('Quit: press ESCAPE')
        self.q.setReadOnly(True)
        box.addWidget(self.pl)
        
        self.con=QPushButton('Continue')
        self.con.clicked.connect(self.close)
        box.addWidget(self.con)
        
        self.setLayout(box)
        self.setWindowTitle('Game Controls')
        self.setGeometry(250,250, 400, 200)
        self.show()
        
def game_controls():
    
    app=QApplication(sys.argv)
    a=start()
    app.exec_()    
    del app
    
        
        
        
          


#Qt Window for Game Parameters:---------------------------------------------------------------------------------------


swg=Value('i',sw)             #================> C language variable. (Shared variables.)
shg=Value('i',sh)
psg=Value('i',ps)
bsg=Value('i',fs)
tdg=Value('i',int(td*180/pi))
mdg=Value('i',int(md*180/pi))
wpbarg=Value('d',wpbar)
restart=Value('i',0)
quit=Value(c_bool,False)

class par(QWidget):
    def __init__(self):
        super().__init__()
        self.para()
        
    def para(self):
        
        box=QVBoxLayout()
        
        self.swl=QLineEdit()          #1
        self.swl.setText('Screen Width: '+str(swg.value))
        self.swl.setReadOnly(True)
        self.sws=QSlider(Qt.Horizontal)
        self.sws.setMinimum(100)
        self.sws.setMaximum(800)
        self.sws.setValue(swg.value)
        self.sws.setTickInterval(25)
        self.sws.setTickPosition(QSlider.TicksBelow)
        self.sws.valueChanged.connect(self.s_w)
        box.addWidget(self.swl)
        box.addWidget(self.sws)
      
        self.shl=QLineEdit()           #2
        self.shl.setText('Screen Height: '+str(shg.value))
        self.shl.setReadOnly(True)
        self.shs=QSlider(Qt.Horizontal)
        self.shs.setMinimum(100)
        self.shs.setMaximum(800)
        self.shs.setValue(shg.value)
        self.shs.setTickInterval(25)
        self.shs.setTickPosition(QSlider.TicksBelow)
        self.shs.valueChanged.connect(self.s_h)
        box.addWidget(self.shl)
        box.addWidget(self.shs)
        
        self.psl=QLineEdit()           #3
        self.psl.setText('Player Speed: '+str(psg.value))
        self.psl.setReadOnly(True)
        self.pss=QSlider(Qt.Horizontal)
        self.pss.setMinimum(1)
        self.pss.setMaximum(int(wpbarg.value))
        self.pss.setValue(psg.value)
        self.pss.setTickInterval(5)
        self.pss.setTickPosition(QSlider.TicksBelow)
        self.pss.valueChanged.connect(self.p_s)
        box.addWidget(self.psl)
        box.addWidget(self.pss)
        
        self.bsl=QLineEdit()           #4
        self.bsl.setText('Puck Speed: '+str(bsg.value))
        self.bsl.setReadOnly(True)
        self.bss=QSlider(Qt.Horizontal)
        self.bss.setMinimum(10)
        self.bss.setMaximum(60)
        self.bss.setValue(bsg.value)
        self.bss.setTickInterval(5)
        self.bss.setTickPosition(QSlider.TicksBelow)
        self.bss.valueChanged.connect(self.b_s)
        box.addWidget(self.bsl)
        box.addWidget(self.bss)
        
        self.tdl=QLineEdit()           #5
        self.tdl.setText('Max. Dev.(Player side): '+str(tdg.value)+' deg.')
        self.tdl.setReadOnly(True)
        self.tds=QSlider(Qt.Horizontal)
        self.tds.setMinimum(0)
        self.tds.setMaximum(90)
        self.tds.setValue(tdg.value)
        self.tds.setTickInterval(5)
        self.tds.setTickPosition(QSlider.TicksBelow)
        self.tds.valueChanged.connect(self.t_d)
        box.addWidget(self.tdl)
        box.addWidget(self.tds)
        
        self.mdl=QLineEdit()           #6
        self.mdl.setText('Max. Dev.(Opponent side): '+str(mdg.value)+' deg.')
        self.mdl.setReadOnly(True)
        self.mds=QSlider(Qt.Horizontal)
        self.mds.setMinimum(0)
        self.mds.setMaximum(90)
        self.mds.setValue(mdg.value)
        self.mds.setTickInterval(5)
        self.mds.setTickPosition(QSlider.TicksBelow)
        self.mds.valueChanged.connect(self.m_d)
        box.addWidget(self.mdl)
        box.addWidget(self.mds)
        
        self.qu=QPushButton('Quit')
        self.qu.setCheckable(True)
        self.qu.clicked.connect(self.quit_wish)
        box.addWidget(self.qu)
        
        self.setLayout(box)
        self.setWindowTitle('Game Parameters:')
        self.setGeometry(75,250, 400, 400)
        self.show()
        
    def s_w(self):
        swg.value=self.sws.value()
        self.swl.setText('Screen Width: '+str(swg.value))
        return swg.value
    
    def s_h(self):
        shg.value=self.shs.value()
        self.shl.setText('Screen Height: '+str(shg.value))
        return shg.value
            
    def p_s(self):
        psg.value=self.pss.value()
        self.psl.setText('Player Speed: '+str(psg.value))
        return psg.value
        
    def b_s(self):
        bsg.value=self.bss.value()
        self.bsl.setText('Puck Speed: '+str(bsg.value))
        return bsg.value
    
    def t_d(self):
        tdg.value=self.tds.value()
        self.tdl.setText('Max. Dev.(Player side): '+str(tdg.value)+' deg.')
        return tdg.value
    
    def m_d(self):
        mdg.value=self.mds.value()
        self.mdl.setText('Max. Dev.(Opponent side): '+str(mdg.value)+' deg.')
        return mdg.value
    
    def quit_wish(self):
        self.close()
        quit.value=self.qu.isChecked()       
   

def parameters():
    
    app=QApplication(sys.argv)
    a=par()
    app.exec_()
    
    del app








#Qt Window for game over:---------------------------------------------------------------------------------------

class over(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        global scoreg
        box=QVBoxLayout()
        
        self.setLayout(box)
        self.setWindowTitle('Game Over!') 
        self.setGeometry(400,250, 300, 200)
        self.show()
        
        self.gol=QLineEdit()         
        self.gol.setText('Game Over!')
        self.gol.setReadOnly(True)
        box.addWidget(self.gol)
        
        self.thl=QLineEdit()         
        self.thl.setText('You defended the puck '+str(scoreg)+' times.')
        self.thl.setReadOnly(True)   
        box.addWidget(self.thl)
        
        self.qu=QPushButton('Quit')
        self.qu.setCheckable(True)
        self.qu.clicked.connect(self.quit_wish)
        box.addWidget(self.qu)
                         
        self.rest=QPushButton('Restart')
        self.rest.setCheckable(True)
        self.rest.clicked.connect(self.restart_wish)
        box.addWidget(self.rest)
                         
    def restart_wish(self):
        self.close()
        return self.rest.isChecked()
        
    
    def quit_wish(self):
        self.close()
        return self.qu.isChecked()

def gameover(score,first):
    global scoreg
    scoreg=score
                         
    app=QApplication(sys.argv)
    a=over()
    app.exec_()
    
    restart=a.restart_wish()
    quit=a.quit_wish()
    
    del app
    
    begin=False
    play=True
    score=score
    
    if restart:
        begin=True
        score=0
        first=True
    if quit:
        play=False
    
    return play,begin,score,first









#PyGame:===========================================================================================================

pg.init()

fr=pg.time.Clock()    #For controlling the framerate

#Initial parameters of movable elements:
#for player's bar:
px=sw/2-wpbar/2
py=sh-hpbar-off

#for puck:
rad=6
o=pi/2   #initial angle of motion
cx=px+wpbar/2    #initial coordinates of centre
cy=sh-off-hpbar-rad
dx=bs*cos(o)
dy=-bs*sin(o)


a=4*md/(wpbar+2*rad)**2 #-------------------------->This parameter can be
                                #tuned to what ever we want. Here I have made
                                #a quadratic function to meet my requirements.
            

play=True
begin=True
first=True
pause=0
score=0


shp=sh
game_controls()

param=multiprocessing.Process(target=parameters)
param.start()

while play:
    try:
        sw,sh,ps,fs,td,md,wpbar=(swg.value,shg.value,psg.value,bsg.value,tdg.value,mdg.value,wpbarg.value)
    
        if quit.value==True:
            play=False
            bs=6     #Puck's speed
            ps=20    #Player_speed
            td=pi/4    #Deviation in angle at the edges of bar on player's side
            md=pi/6      #Maximum range of randomness in deviation of opposite bar
            sw=400      #screen-width
            sh=600     #screen-height
            begin=True
            first=True
            
            
        pg.display.set_caption("AirHockey: Score="+str(score))
        
        #Parameters of static elements of the game:
        off=5      #Offset from edges
        hpbar=8      #height of bar
        wpbar=sw/4      #width of player's bar
        wsbar=7     #Width of side bar
        hsbar=sh-hpbar-2*off   #Height of side bar
        hobar=7     #Height of opposite bar
        wobar=sw-2*wsbar-2*off    #width of opposite bar

        #Positioning of these elements:
        #(x,y,width,height)
        sbar1=(off,off,wsbar,hsbar)
        sbar2=(sw-wsbar-off,off,wsbar,hsbar)
        obar=(sw/2-wobar/2,off,wobar,hobar)
    
        scr=pg.display.set_mode((sw,sh))  
        scr.fill(greend)
        pg.draw.rect(scr,grey,sbar1)   #side bars
        pg.draw.rect(scr,grey,sbar2)
        pg.draw.rect(scr,orange,obar)     #opposite bar
        pg.draw.rect(scr,white,(px,py,wpbar,hpbar))   #player bar      
        pg.draw.circle(scr,magenta,(cx,cy),rad)       #puck
        
        if cx>sw-off-wsbar:
            cx=sw/2
        if shp-sh!=0:
            if cy>sh-off-hpbar:
                cy=sh-off-hpbar
            shp=sh
        if px>sw:
            px=sw-wpbar
        if py>sh or py<sh-off-hpbar:
            py=sh-off-hpbar
        
        if begin:
            if first:
                px=sw/2-wpbar/2
                py=sh-hpbar-off
                o=pi/2   #initial angle of motion
                cx=px+wpbar/2    #initial coordinates of centre
                cy=sh-off-hpbar-rad
                pause=0
                first=False
            
        #Movement of puck:       
        if begin==False and pause%2!=0:
            if cx<off+wsbar+rad or cx>sw-off-wsbar-rad:      #Ball hitting sidewalls
                if dx<0:
                    cx=off+wsbar+rad     
                    o=atan(dy/dx)
                if dx>0:
                    cx=sw-off-wsbar-rad
                    o=atan(dy/dx)+pi
               
            if cy<off+hobar+rad or cy>sh-off-hpbar-rad:
                if dy<0:
                    cy=off+hobar+rad
                    if dx<0:
                        o=atan(dy/dx)+pi
                        l=rdev(td)             #Gives a feeling of reality
                    if dx>0:
                        o=atan(dy/dx)
                        l=-rdev(td)           #Opponent has some randomness
                    o=o+l
                if dy>0:
                    if cx>(px-rad) and cx<(px+wpbar+rad) and cy<(sh-off-hpbar):
                        cy=sh-off-hpbar-rad
                        if dx<0:
                            o=atan(dy/dx)+pi
                        if dx>0:
                            o=atan(dy/dx)
                            
                        if cx<=(px+wpbar/2):
                            l=a*(cx-(px+wpbar/2))**2       #to partially give sphericity to player bar
                        if cx>px+wpbar/2:
                            l=-a*(cx-(px+wpbar/2))**2
                        o=o+l
                        score+=1
            
            dx=bs*cos(o)
            dy=-bs*sin(o)
            cx=cx+dx
            cy=cy+dy  
        
        if pause%2==0:
            pg.draw.circle(scr,red,(px+wpbar/2,sh-hpbar/2),6)
            pg.draw.circle(scr,red,(px,sh-hpbar/2),6)
            pg.draw.circle(scr,red,(px+wpbar,sh-hpbar/2),6)

        else:
            pg.draw.circle(scr,blue,(px+wpbar/2,sh-hpbar/2),6)
            pg.draw.circle(scr,blue,(px,sh-hpbar/2),6)
            pg.draw.circle(scr,blue,(px+wpbar,sh-hpbar/2),6)
        if cy>sh+10*off:
            play,begin,score,first=gameover(score,first)           
            
        for event in pg.event.get():
            if event.type==QUIT:     #i.e. turn off the game on click on cross key of this window
                play=False
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    play=False
                if event.key==K_SPACE:
                    pause+=1
                    begin=False
                    continue
                        
                #Movement of player:
                if px>off+wsbar and px<sw-off-wsbar-wpbar:
                    move={K_LEFT:-ps, K_RIGHT:ps}          
                    if event.key in move:
                        dpx=move[event.key]
                        px=px+dpx         #changing the old position to new position        
                else:
                    if px<off+wsbar:      #to restrict the motion to outside of the screen
                        px=px+ps
                    else:
                        px=px-ps
        if begin:
            cx=px+wpbar/2
            cy=sh-off-hpbar-rad
            
        pg.display.flip()
        fr.tick(fs)
        
    except:
        play=False
        print('There was an error')
    
pg.quit()

print('Thank you![^.../\...^]')




#Note: 
    #If in case the above code shows any error like "pygame.numpy does not have 
    #any attribute "pi" or something like that, then move the last two lines of
    #libraries (the ones related to pygame) below the "#PyGame" comment.