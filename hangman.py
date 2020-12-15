#!/usr/bin/python3
import pygame
import sys
import threading
import time
import random
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

#word=str(input("What is the word the challenger will have to find?"))
lives=9
word=''

hangmanList={}
for i in range(9):
    hangmanList[i]=pygame.image.load('Hangman'+str(9-i)+'.png')

white=(255,255,255)
black=(0,0,0)

pygame.display.init()

screenWidth = 400
screenHeight = 400
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Hangman')

hangmanRect= Rect(screenWidth/2-75,10,150,150)
running = True
playing = True
clock=pygame.time.Clock()

letterList=['']
guessList={}
wordList={}

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 14)
font2 = pygame.font.Font('freesansbold.ttf', 20)
font3 = pygame.font.Font('freesansbold.ttf', 11)
startText=font3.render('Enter the word you want the challenger to guess. Then press enter.',True,black,None)
startText2=font3.render('Type "random" for a random word',True,black,None)
startWord=font.render(word,True,black,None)
winText=font2.render('Yay! You Win! Press Any Key To Exit', True, black, None)
loseText=font2.render('You Lost! Press Any Key To Exit', True, black, None)
livesText=font.render(f'{lives}',True,black,None)
formatLetters=''
guessText = font.render(f'{formatLetters}', True, black, None)
guessWord=''
wordText=font.render(f'{guessWord}', True, black, None)
alreadyText=font.render('Letter Already Guessed', True, black, None)
alreadyGuessed=False
instructionText=font.render('Press a key to guess the letter',True,black,None)
wordText=font.render('The word was: '+word,True,black,None)
changeList=True
start=True

inputLetter=''
addLetter = False
reduceLife = False
youWin = False
youLose = False

def render():
    global formatLetters, addLetter, guessWord, winText, running

    screen.fill(white)
    if len(letterList)>0:
        formatLetters=''
        for i in letterList:
            formatLetters = formatLetters + i + ' '

    guessWord=''
    for key,letters in guessList.items():
        guessWord=guessWord+' '+letters
    if start == True:
        screen.blit(startText,(int(screenWidth/2-startText.get_width()/2),int(screenHeight/2-startText.get_height()/2)))
        screen.blit(startText2,(int(screenWidth/2-startText2.get_width()/2),int(screenHeight/2+(startText.get_height()/2))))
        startWord=font.render(word,True,black,None)
        screen.blit(startWord,(int(screenWidth/2-startWord.get_width()/2),int(screenHeight*7/12)))
    if youWin == True:
        screen.blit(winText,(int(screenWidth/2-winText.get_width()/2),int(screenHeight/2-winText.get_height()/2)))
        running = False
    if youLose == True:
        wordText=font.render('The word was: '+word,True,black,None)
        screen.blit(wordText,(int(screenWidth/2-wordText.get_width()/2),int(screenHeight*3/4-wordText.get_height()/4)))
        screen.blit(loseText,(int(screenWidth/2-loseText.get_width()/2),int(screenHeight/2-loseText.get_height()/2)))
        running=False
    
    letterText=font.render(f'{guessWord}', True, black, None)
    guessText = font.render(f'{formatLetters}', True, black, None)

    if youWin==False and youLose == False:
        if alreadyGuessed==True:
            screen.blit(alreadyText,(int(screenWidth/2-alreadyText.get_width()/2),int(screenHeight*3/4-alreadyText.get_height()/4)))
        elif start==False:
            livesText=font.render(f'Lives: {lives}',True,black,None)
            screen.blit(livesText,(int(screenWidth*3/4),livesText.get_height()))
            screen.blit(instructionText,(int(screenWidth/2-instructionText.get_width()/2),int(screenHeight*3/4-instructionText.get_height()/4)))
        screen.blit(letterText,(int(screenWidth/2-letterText.get_width()/2),int(screenHeight*1/2)))
        screen.blit(guessText,(int(screenWidth/3),int(screenHeight*7/12)))
    if lives > 0:
        screen.blit(hangmanList[lives-1],hangmanRect.toPygame())

    pygame.display.update()

while running:
    render()

    event = pygame.event.wait()
    if event.type == pygame.KEYDOWN:
        if event.unicode.isalpha()==True and event.unicode.islower()==True and start == False:
            inputLetter=event.unicode
        if start==True and event.key != pygame.K_BACKSPACE and event.unicode.islower():
            word=word+event.unicode
        if event.key == pygame.K_BACKSPACE and len(word)>0:
            word=word[::-1]
            word=word.replace(word[0],'',1)
            word=word[::-1]
        if (event.key==pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and start == True:
            if word=='random':
                fileName = 'hangmanWords.txt'
                randomList=[]
                with open(fileName,'r')  as file:
                    for line in file:
                        randomList.append(line)
                word=random.choice(randomList)
                wordLetterList=[]
                for i in word:
                    wordLetterList.append(i)
                wordLetterList.pop(-1)
                word=''
                for i in wordLetterList:
                    word=word+i
                #remove last char. of word here
            start=False
            counter=0
            for i in word:
                wordList[counter]=i
                guessList[counter]='_'
                counter+=1
    if len(inputLetter)> 0 and start==False:
        alreadyGuessed=False
        reduceLife=True
        addList=True

        for key, letter in wordList.items():
            if inputLetter == letter:
                reduceLife=False
                guessList[key]=inputLetter
                addList=False

        for letter in letterList:
            if letter == inputLetter:
                alreadyGuessed=True
                reduceLife=False
                addList=False

        if reduceLife==True:
            lives-=1
        if addList == True:
            letterList.append(inputLetter)

        counter=0
        for letter in letterList:
            counter+=1
            if letter == inputLetter and counter != len(letterList):
                changeList = False

        if changeList == False and len(letterList)>0:
            alreadyGuessed=True
            changeList =True

        guessWord=''
        for key,letters in guessList.items():
            guessWord=guessWord+letters

        if guessWord==word:
            youWin=True

        if lives == 0:
            youLose = True
            
        inputLetter=''

        clock.tick(60)
while playing:
    event = pygame.event.wait()
    if event.type == pygame.KEYDOWN:
        sys.exit()
        pygame.quit()