# (c) 0xC0DE Dec 2020
# example Python3 code for a bullet travelling from an enemy in the *general direction* of a player
# one time calculation of (stepx, stepy) needed to advance the bullet to the (old) location of the player
# written with a translation to 6502 asm code in mind

# PLEASE NOTE: I have since created a more accurate version in BBC BASIC. Consider this to be obsolete!!

import math

# example player and enemy coordinates (inverted y-axis!)
# Acorn screen MODE 5 is 160x256 wide pixels
mode5_enemy=(30, 10)
mode5_player=(6, 80)

# convert to actual coordinates as if square pixels
enemy=(mode5_enemy[0], mode5_enemy[1]//2)
player=(mode5_player[0], mode5_player[1]//2)

ex=enemy[0]
ey=enemy[1]
px=player[0]
py=player[1]

real_dx=px-ex
real_dy=py-ey

# determine in which quadrant the player is relative to the enemy
# quadrant bottom right = A, bottom left = B, top left = C, top right = D
if real_dy>=0:
  if real_dx>=0: quad=0 # A
  else: quad=1 # B
else:
  if real_dx>=0: quad=3 # D
  else: quad=2 # C

dx=abs(real_dx)
dy=abs(real_dy)

if dy>=dx: r=4
else: r=0
if r==0: dx, dy = dy, dx # swap and compensate for it later

# simple calculations, keeping 6502 asm code in mind here (bit shifts)
half_dx=dx//2
if dy>=4*dx+dx: d=3
elif dy>=2*dx+half_dx: d=2
elif dy>=dx+half_dx: d=1
else: d=0

#################### ALL STEPS IN 2 SMALL TABLES #####################################
# this generates the two small tables we actually need in our 6502 asm code later
# a bullet can go in 32 distinct directions
# is easily extended to e.g. 64 if more precise direction is needed

mode5_step_x=[0]*32
mode5_step_y=[0]*32
spd=4
for n in range(32):
  rad=(n/32)*2*math.pi # going clockwise(!) from x-axis
  real_step_x=spd*math.cos(rad)
  real_step_y=-spd*math.sin(rad) # inverted y-axis!
  mode5_step_x[n]=round(0.5*real_step_x) # remember: wide pixels
  mode5_step_y[n]=round(real_step_y)
print("stepx[]=", mode5_step_x)
print("stepy[]=", mode5_step_y)

#################### EXAMPLE STEP_X AND STEP_Y FOR PLAYER AND ENEMY COORDINATES GIVEN #####################################

dir=[3, 2, 1, 0,    4, 5, 6, 7,    12, 13, 14, 15,    11, 10, 9, 8,    19, 18, 17, 16,    20, 21, 22, 23,    28, 29, 30, 31,    27, 26, 25, 24]
idx=dir[8*quad+r+d]
print("stepx =", mode5_step_x[idx])
print("stepy =", mode5_step_y[idx])

