#!/usr/bin/python3
import pygame
import sys
import threading
import time
class Rect:

    def __init__(self, x: float, y: float, width: int, height: int):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__pyg_rect = pygame.Rect(
            int(self.__x), int(self.__y), self.__width, self.__height)

    def __str__(self):
        return 'x: {} y: {} width: {} height: {}'.format(self.__x, self.__y,
            self.__width, self.__height)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = float(x)
        self.__pyg_rect.x = int(self.__x)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = float(y)
        self.__pyg_rect.y = int(self.__y)

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def toPygame(self):
        return self.__pyg_rect

word=str(input("What is the word the challenger will have to find?"))
print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
lives=int(input("How many lives do you want the challenger to have? (int: 1-9)"))
hangmanList={}
hangmanList[9]=pygame.image.load("Hangman.png")
hangmanList[8]=pygame.image.load("Hangman2.png")
hangmanList[7]=pygame.image.load("Hangman3.png")
hangmanList[6]=pygame.image.load("Hangman4.png")
hangmanList[5]=pygame.image.load("Hangman5.png")
hangmanList[4]=pygame.image.load("Hangman6.png")
hangmanList[3]=pygame.image.load("Hangman7.png")
hangmanList[2]=pygame.image.load("Hangman8.png")
hangmanList[1]=pygame.image.load("Hangman9.png")
hangmanList[0]=pygame.image.load("Hangman10.png")

white=(255,255,255)
black=(0,0,0)

pygame.display.init()

screenWidth = 400
screenHeight = 400
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Hangman')

hangmanRect= Rect(screenWidth/2-75,10,150,150)
running = True
clock=pygame.time.Clock()



letterList=['']
guessList={}
wordList={}

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 14)
formatLetters=''
guessText = font.render(f'{formatLetters}', True, black, None)
guessWord=''
wordText=font.render(f'{guessWord}', True, black, None)
changeList=True

counter=0
for i in word:
    wordList[counter]=i
    guessList[counter]='_'
    counter+=1

addLetter = False
reduceLife=False
youWin = False

def render():
    global formatLetters, addLetter, guessWord

    screen.fill(white)
    if len(letterList)>0:
        formatLetters=''
        for i in letterList:
            formatLetters = formatLetters + i + ' '

    guessWord=''
    for key,letters in guessList.items():
        guessWord=guessWord+letters
    if youWin == True:
        winText=font.render('Yay! You Win', True, black, None)


    letterText=font.render(f'{guessWord}', True, black, None)
    guessText = font.render(f'{formatLetters}', True, black, None)

    screen.blit(letterText,(screenWidth/2-letterText.get_width()/2,screenHeight*1/2))
    screen.blit(guessText,(screenWidth/3,screenHeight*2/3))
    screen.blit(hangmanList[lives-1],hangmanRect.toPygame())

    pygame.display.update()

while running:
    render()

    counter=0
    if youWin == True:
        running=False
    inputLetter=str(input("What letter do you want to guess?"))
    while len(inputLetter) != 1:
        print('invalid input')
        inputLetter=str(input("What letter do you want to guess?"))

    reduceLife=True
    addList=True


    for key, letter in wordList.items():
        if inputLetter == letter:
            reduceLife=False
            guessList[key]=inputLetter
            addList=False

    if reduceLife==True:
        lives=lives
        #lives-=1
    if addList == True:
        letterList.append(inputLetter)
        
    for letter in letterList:
        counter+=1
        if letter == inputLetter and counter != len(letterList):
            changeList = False
    if changeList == False and len(letterList)>0:
        print('Letter Already Guessed')
        letterList.pop(-1)
        changeList =True
    if guessWord == word:
        youWin == True
    clock.tick(60)
sys.exit()
pygame.quit()