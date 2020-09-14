
import random, math
from tkinter import *

#Initiating variables
speed = 1

score = 0
lives = 10

moveInterval = 30

coinSize = 20
fireballSize = 20

cWidth = 580
cHieght = 800

levelInterval = 100
level = math.floor(score/100) + 1
#functions
def game():
    global score
    StartButton.destroy()
    def make_coins():
        xPos = random.randint(20,cWidth - 20)
        yPos = -20

        coin = c.create_image(xPos,yPos,image = coinImage)
        coin_list.append(coin)
        screen.after(random.randint(750,1250),make_coins)
    def make_healCoins():
        xPos = random.randint(20,cWidth - 20)
        yPos = -20
        healCoin = c.create_image(xPos,yPos,image = HealCoin)
        healCoin_list.append(healCoin)
        screen.after(random.randint(750,1250),make_healCoins)
    def make_megaCoins():
        xPos = random.randint(20,cWidth - 20)
        yPos = -20
        megaCoin = c.create_image(xPos,yPos,image = MegaCoin)
        megaCoin_list.append(megaCoin)
        screen.after(random.randint(2000,2500),make_megaCoins)
    def make_fireballs():
        xPos = random.randint(20,cWidth - 20)
        yPos = -20
        fireball = c.create_oval(xPos,yPos,xPos - fireballSize,yPos+fireballSize, fill = 'red')
        fireball_list.append(fireball)
        screen.after(random.randint(450,750),make_fireballs)

    def move_coins():
        for i in coin_list:
            c.move(i,0,(math.floor(score/levelInterval) +1)/speed)
            global lives
            if c.coords(i)[1] > 800:
                lives = lives-1
                lives_display.config(text = 'Lives: ' + str(lives))
                c.delete(i)
                coin_list.remove(i)
        screen.after(1,move_coins)
    def move_healCoins():
        for i in healCoin_list:
            c.move(i,0,(math.floor(score/levelInterval) +1.5)/speed)
            global lives
            if c.coords(i)[1] > 800:
                lives = lives-1
                lives_display.config(text = 'Lives: ' + str(lives))
                c.delete(i)
                healCoin_list.remove(i)
        screen.after(1,move_healCoins)
    def move_megaCoins():
        for i in megaCoin_list:
            c.move(i,0,(math.floor(score/levelInterval) +2)/speed)
            global lives
            if c.coords(i)[1] > 800:
                lives = lives-2
                lives_display.config(text = 'Lives: ' + str(lives))
                c.delete(i)
                megaCoin_list.remove(i)
        screen.after(1,move_megaCoins)
    def move_fireballs():
        for i in fireball_list:
            c.move(i,0,(math.floor(score/levelInterval) +1.5)/speed)
        screen.after(1,move_fireballs)
    def move_sprite(event):
        y = event.y
        x = event.x
        c.coords(sprite, x-10, y-10, x+10, y+10)

    def collision(item1, item2, distance):
        xdistance = abs(c.coords(item1)[0] - c.coords(item2)[0])
        ydistance = abs(c.coords(item1)[1] - c.coords(item2)[1])
        overlap = xdistance < distance  and ydistance < distance
        return overlap
    def check_collision():
        global score
        global lives
        for i in coin_list:
            if collision(i,sprite,20):
                c.delete(i)
                coin_list.remove(i)
                score = score + 10
        for i in fireball_list:
            if collision(i,sprite,20):
                c.delete(i)
                fireball_list.remove(i)
                lives = lives - 2
        for i in megaCoin_list:
            if collision(i,sprite,20):
                c.delete(i)
                megaCoin_list.remove(i)
                score = score+30
        for i in healCoin_list:
            if collision(i,sprite,20):
                c.delete(i)
                healCoin_list.remove(i)
                lives = lives + 1
            if lives <= 0:
                screen.after(1,end_game)
        lives_display.config(text = 'Lives: ' + str(lives))
        score_display.config(text = 'Score: ' + str(score))
        level = math.floor(score/100) +1
        level_display.config(text = 'Level: ' +str(level))
        screen.after(10,check_collision)

    
        
    #labels
    score_display = Label(screen, text = 'Score:' + str(score))
    score_display.pack()

    lives_display = Label(screen, text = 'Lives:' + str(lives))
    lives_display.pack()

    level_display = Label(screen, text = 'Level:' + str(level))
    level_display.pack()
    #creating the player

    sprite = c.create_rectangle(400,760,380,780, fill = 'cyan')
    c.bind_all('<Motion>',move_sprite) #use move_sprite for arrow keys
    coin_list = []
    fireball_list = []
    megaCoin_list = []
    healCoin_list = []

    #scheduling

    screen.after(3000,make_coins)
    screen.after(3000,make_fireballs)
    screen.after(3000,move_coins)
    screen.after(3000,move_fireballs)
    screen.after(3000,check_collision)
    screen.after(3000,move_megaCoins)
    screen.after(3000,make_megaCoins)
    screen.after(3000,make_healCoins)
    screen.after(3000,move_healCoins)

    def end_game():
        print('Your Score Is: ' + str(score))
        screen.destroy()


#screen and canvas

screen = Tk()
screen.title('Candy Catchers')

c = Canvas(screen, width = cWidth, height = cHieght, bg = 'navy blue')
c.pack()



StartButton = Button(screen, text = ' PLAY! ',command = game)
StartButton.pack()

coinImage = PhotoImage(file = 'coin.gif')
HealCoin = PhotoImage(file = 'HealCoin.gif')
MegaCoin = PhotoImage(file = 'MegaCoin.gif')

#loop
screen.mainloop()


