#!/usr/bin/env python
#
# Command Line usage:
#   xmas.py <input sequence> <audio file> <D|R Debug or Real>

import RPi.GPIO as GPIO, time
import sys
import time
import pygame
import random

set = bytearray(25 * 3)

# Defines the mapping of logical mapping to physical mapping
# 1 - 5 are lights from top to bottom on tree
# 6 = RED
# 7 = GREEN
# 8 = BLUE
logical_map = [0 for i in range(9)]
pin_map = [0,11,12,8,15,16,18,22,7]
rand = int(0)
star = [-190, 262,
         -90, 500,
          45, 724,
         123, 464,
         217, 272,
         442, 230,
         676, 210,
         509,  59,
         340,-122,
         355,-332,
         409,-562,
         209,-432,
           6,-337,
        -204,-459,
        -378,-539,
        -360,-349,
        -336,-116,
        -496,  70,
        -701, 227,
        -454, 241,
        -184,  60,
        -119,-143,
         107,-160,
         201,  60,
           5, 194]	 

#####################################################################
def starinit(n):
   for x in range(25):
     set[x*3  ] = gamma[0]
     set[x*3+1] = gamma[0]
     set[x*3+2] = gamma[0]
   spidev.write(set)
   spidev.flush()
   time.sleep(0.05)

#####################################################################
def star_vert(per,R1,G1,B1,R2,G2,B2):

   for x in range(25):
     if (float(star[x*2]) +701.0)/1377.0 > float(per)/100.0:
       set[x*3  ] = gamma[int(R1)]
       set[x*3+1] = gamma[int(G1)]
       set[x*3+2] = gamma[int(B1)]
     else:
       set[x*3  ] = gamma[int(R2)]
       set[x*3+1] = gamma[int(G2)]
       set[x*3+2] = gamma[int(B2)]

   spidev.write(set)
   spidev.flush()

#####################################################################
# Each itr = circle changes by 10 pixels up to 800, then back down
#   again.   Result in 160 itr per cycle
def star_expand(itr,R,G,B):

   bounding_circle = itr % 160
   if bounding_circle > 80:
     bounding_circle = 800 - ((itr % 160)-80)*10
   else:
     bounding_circle = (itr % 160)*10
 
   for x in range(25):
     dist = star[x*2]*star[x*2] + star[x*2+1]*star[x*2+1]
     dist = dist ** (0.5)
     if dist < bounding_circle:
       set[x*3  ] = gamma[R]
       set[x*3+1] = gamma[G]
       set[x*3+2] = gamma[B]
     elif dist - bounding_circle < 50:
       factor = (dist-bounding_circle)/50.0
       set[x*3  ] = gamma[R*factor]
       set[x*3+1] = gamma[G*factor]
       set[x*3+2] = gamma[B*factor]
   spidev.write(set)
   spidev.flush()
     

#####################################################################
def star_solid(R,G,B):

   for x in range(25):
       set[x*3  ] = gamma[int(R)]
       set[x*3+1] = gamma[int(G)]
       set[x*3+2] = gamma[int(B)]
   
   spidev.write(set)
   spidev.flush()

#####################################################################
def star_tips(Rt,Gt,Bt,R,G,B):

   for x in range(25):
       set[x*3  ] = gamma[int(R)]
       set[x*3+1] = gamma[int(G)]
       set[x*3+2] = gamma[int(B)]
   
   set[2*3  ] = gamma[int(Rt)]
   set[2*3+1] = gamma[int(Gt)]
   set[2*3+2] = gamma[int(Bt)]

   set[6*3  ] = gamma[int(Rt)]
   set[6*3+1] = gamma[int(Gt)]
   set[6*3+2] = gamma[int(Bt)]

   set[10*3  ] = gamma[int(Rt)]
   set[10*3+1] = gamma[int(Gt)]
   set[10*3+2] = gamma[int(Bt)]

   set[14*3  ] = gamma[int(Rt)]
   set[14*3+1] = gamma[int(Gt)]
   set[14*3+2] = gamma[int(Bt)]

   set[18*3  ] = gamma[int(Rt)]
   set[18*3+1] = gamma[int(Gt)]
   set[18*3+2] = gamma[int(Bt)]

   spidev.write(set)
   spidev.flush()

#####################################################################
def star_point1(R,G,B):

   set[0*3  ] = gamma[int(R)]
   set[0*3+1] = gamma[int(G)]
   set[0*3+2] = gamma[int(B)]

   set[1*3  ] = gamma[int(R)]
   set[1*3+1] = gamma[int(G)]
   set[1*3+2] = gamma[int(B)]

   set[2*3  ] = gamma[int(R)]
   set[2*3+1] = gamma[int(G)]
   set[2*3+2] = gamma[int(B)]

   set[3*3  ] = gamma[int(R)]
   set[3*3+1] = gamma[int(G)]
   set[3*3+2] = gamma[int(B)]

   set[4*3  ] = gamma[int(R)]
   set[4*3+1] = gamma[int(G)]
   set[4*3+2] = gamma[int(B)]

   set[24*3  ] = gamma[int(R)]
   set[24*3+1] = gamma[int(G)]
   set[24*3+2] = gamma[int(B)]
   
   spidev.write(set)
   spidev.flush()

#####################################################################
def star_point2(R,G,B):

   set[4*3  ] = gamma[int(R)]
   set[4*3+1] = gamma[int(G)]
   set[4*3+2] = gamma[int(B)]

   set[5*3  ] = gamma[int(R)]
   set[5*3+1] = gamma[int(G)]
   set[5*3+2] = gamma[int(B)]

   set[6*3  ] = gamma[int(R)]
   set[6*3+1] = gamma[int(G)]
   set[6*3+2] = gamma[int(B)]

   set[7*3  ] = gamma[int(R)]
   set[7*3+1] = gamma[int(G)]
   set[7*3+2] = gamma[int(B)]

   set[8*3  ] = gamma[int(R)]
   set[8*3+1] = gamma[int(G)]
   set[8*3+2] = gamma[int(B)]

   set[23*3  ] = gamma[int(R)]
   set[23*3+1] = gamma[int(G)]
   set[23*3+2] = gamma[int(B)]
   
   spidev.write(set)
   spidev.flush()

#####################################################################
def star_point3(R,G,B):

   set[8*3  ] = gamma[int(R)]
   set[8*3+1] = gamma[int(G)]
   set[8*3+2] = gamma[int(B)]

   set[9*3  ] = gamma[int(R)]
   set[9*3+1] = gamma[int(G)]
   set[9*3+2] = gamma[int(B)]

   set[10*3  ] = gamma[int(R)]
   set[10*3+1] = gamma[int(G)]
   set[10*3+2] = gamma[int(B)]

   set[11*3  ] = gamma[int(R)]
   set[11*3+1] = gamma[int(G)]
   set[11*3+2] = gamma[int(B)]

   set[12*3  ] = gamma[int(R)]
   set[12*3+1] = gamma[int(G)]
   set[12*3+2] = gamma[int(B)]

   set[22*3  ] = gamma[int(R)]
   set[22*3+1] = gamma[int(G)]
   set[22*3+2] = gamma[int(B)]
   
   spidev.write(set)
   spidev.flush()

#####################################################################
def star_point4(R,G,B):

   set[12*3  ] = gamma[int(R)]
   set[12*3+1] = gamma[int(G)]
   set[12*3+2] = gamma[int(B)]

   set[13*3  ] = gamma[int(R)]
   set[13*3+1] = gamma[int(G)]
   set[13*3+2] = gamma[int(B)]

   set[14*3  ] = gamma[int(R)]
   set[14*3+1] = gamma[int(G)]
   set[14*3+2] = gamma[int(B)]

   set[15*3  ] = gamma[int(R)]
   set[15*3+1] = gamma[int(G)]
   set[15*3+2] = gamma[int(B)]

   set[16*3  ] = gamma[int(R)]
   set[16*3+1] = gamma[int(G)]
   set[16*3+2] = gamma[int(B)]

   set[21*3  ] = gamma[int(R)]
   set[21*3+1] = gamma[int(G)]
   set[21*3+2] = gamma[int(B)]
   
   spidev.write(set)
   spidev.flush()

#####################################################################
def star_point5(R,G,B):

   set[0*3  ] = gamma[int(R)]
   set[0*3+1] = gamma[int(G)]
   set[0*3+2] = gamma[int(B)]

   set[19*3  ] = gamma[int(R)]
   set[19*3+1] = gamma[int(G)]
   set[19*3+2] = gamma[int(B)]

   set[18*3  ] = gamma[int(R)]
   set[18*3+1] = gamma[int(G)]
   set[18*3+2] = gamma[int(B)]

   set[17*3  ] = gamma[int(R)]
   set[17*3+1] = gamma[int(G)]
   set[17*3+2] = gamma[int(B)]

   set[16*3  ] = gamma[int(R)]
   set[16*3+1] = gamma[int(G)]
   set[16*3+2] = gamma[int(B)]

   set[20*3  ] = gamma[int(R)]
   set[20*3+1] = gamma[int(G)]
   set[20*3+2] = gamma[int(B)]
   
   spidev.write(set)
   spidev.flush()

#####################################################################
def star_inside_solid(R,G,B):

   for x in range(5):
       set[(x+20)*3  ] = gamma[int(R)]
       set[(x+20)*3+1] = gamma[int(G)]
       set[(x+20)*3+2] = gamma[int(B)]
   
   spidev.write(set)
   spidev.flush()

#####################################################################
#####################################################################


# Setup the board
GPIO.setmode(GPIO.BOARD)
for i in range(1,9):
  GPIO.setup(pin_map[i], GPIO.OUT)
time.sleep(2.0);
dev    = "/dev/spidev0.0"
spidev = file(dev,"wb")


# Calculate gamma correction
gamma = bytearray(256)
for i in range(256):
  gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0 + 0.5)

starinit(1)

# Open the setup config file and parse it
with open("/home/pi/xmas/setup.txt",'r') as f:
  data = f.readlines()
  for i in range(8):
    logical_map[i+1] = int(data[i])

# Current light states
lights = [False for i in range(8)]
while True :
  rand = random.randrange(1,8)
  if rand == 1:
    GPIO.output(pin_map[logical_map[1]],True)
    GPIO.output(pin_map[logical_map[2]],True)
    GPIO.output(pin_map[logical_map[3]],True)
    GPIO.output(pin_map[logical_map[4]],True)
    GPIO.output(pin_map[logical_map[5]],True)
    GPIO.output(pin_map[logical_map[6]],False)
    GPIO.output(pin_map[logical_map[7]],False)
    GPIO.output(pin_map[logical_map[8]],False)
    star_solid(255,255,255)
  if rand == 2:  
    GPIO.output(pin_map[logical_map[1]],False)
    GPIO.output(pin_map[logical_map[2]],False)
    GPIO.output(pin_map[logical_map[3]],False)
    GPIO.output(pin_map[logical_map[4]],False)
    GPIO.output(pin_map[logical_map[5]],False)
    GPIO.output(pin_map[logical_map[6]],True)
    GPIO.output(pin_map[logical_map[7]],False)
    GPIO.output(pin_map[logical_map[8]],False)
    star_solid(255,0,0)
  if rand == 3:
    GPIO.output(pin_map[logical_map[1]],False)
    GPIO.output(pin_map[logical_map[2]],False)
    GPIO.output(pin_map[logical_map[3]],False)
    GPIO.output(pin_map[logical_map[4]],False)
    GPIO.output(pin_map[logical_map[5]],False)
    GPIO.output(pin_map[logical_map[6]],True)
    GPIO.output(pin_map[logical_map[7]],True)
    GPIO.output(pin_map[logical_map[8]],False)
    star_solid(255,255,255)
  if rand == 4:  
    GPIO.output(pin_map[logical_map[1]],True)
    GPIO.output(pin_map[logical_map[2]],True)
    GPIO.output(pin_map[logical_map[3]],True)
    GPIO.output(pin_map[logical_map[4]],True)
    GPIO.output(pin_map[logical_map[5]],True)
    GPIO.output(pin_map[logical_map[6]],True)
    GPIO.output(pin_map[logical_map[7]],False)
    GPIO.output(pin_map[logical_map[8]],False)
    star_tips(200,200,200,255,0,0)
  if rand == 5:  
    GPIO.output(pin_map[logical_map[1]],False)
    GPIO.output(pin_map[logical_map[2]],False)
    GPIO.output(pin_map[logical_map[3]],False)
    GPIO.output(pin_map[logical_map[4]],False)
    GPIO.output(pin_map[logical_map[5]],False)
    GPIO.output(pin_map[logical_map[6]],False)
    GPIO.output(pin_map[logical_map[7]],False)
    GPIO.output(pin_map[logical_map[8]],True)
    star_solid(0,0,255)
  if rand == 6:  
    GPIO.output(pin_map[logical_map[1]],True)
    GPIO.output(pin_map[logical_map[2]],True)
    GPIO.output(pin_map[logical_map[3]],True)
    GPIO.output(pin_map[logical_map[4]],True)
    GPIO.output(pin_map[logical_map[5]],True)
    GPIO.output(pin_map[logical_map[6]],False)
    GPIO.output(pin_map[logical_map[7]],False)
    GPIO.output(pin_map[logical_map[8]],True)
    star_tips(200,200,200,0,0,255)
  if rand == 7:
    GPIO.output(pin_map[logical_map[1]],True)
    GPIO.output(pin_map[logical_map[2]],True)
    GPIO.output(pin_map[logical_map[3]],True)
    GPIO.output(pin_map[logical_map[4]],True)
    GPIO.output(pin_map[logical_map[5]],True)
    GPIO.output(pin_map[logical_map[6]],False)
    GPIO.output(pin_map[logical_map[7]],False)
    GPIO.output(pin_map[logical_map[8]],False)
    star_solid(255,215,0)
  if rand == 8:  
    GPIO.output(pin_map[logical_map[1]],False)
    GPIO.output(pin_map[logical_map[2]],False)
    GPIO.output(pin_map[logical_map[3]],False)
    GPIO.output(pin_map[logical_map[4]],False)
    GPIO.output(pin_map[logical_map[5]],False)
    GPIO.output(pin_map[logical_map[6]],True)
    GPIO.output(pin_map[logical_map[7]],False)
    GPIO.output(pin_map[logical_map[8]],True)
    star_vert(50,255,0,0,0,0,255)
  time.sleep(60.0)
