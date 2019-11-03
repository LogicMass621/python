#!/usr/bin/python3
import turtle
import random
t = turtle.Turtle()
angles = ['40','36','45','51','60']
colors = ['red','orange','cyan','blue','magenta','green','purple','yellow']
x = random.randint(80,120)
counter = 0
angle = random.choice(angles)
angle = int(angle)
sides = 360/angle
t.pensize(4)
speed = -5
while counter < x:
    angle = random.choice(angles)
    angle = int(angle)
    sides = 360/angle
    t.color(random.choice(colors))
    t.up()
    t.lt(random.randint(1,360))
    t.fd(random.randint(200,275))
    t.down()
    counter2 = 0
    fd = random.randint(20,60)
    while counter2 < sides:
        t.fd(fd)
        t.lt(angle)
        counter2 = counter2 +1
