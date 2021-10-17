#!/usr/bin/python
import pygame
import sys
import threading
import time

#changes name of terminal window
sys.stdout.write("\x1b]2;Chess\x07")

screenWidth=800
screenHeight=800
pygame.display.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Chess')
chessBoard=pygame.image.load('chessBoard.png')

running = True
clock = pygame.time.Clock()

class Piece:
    def __init__(self, x: int, y: int, color: int,Type: int):
        self.__x = x
        self.__y = y
        self.__color=color
        self.__Type = Type

    def __str__(self):
        return 'x: {} y: {} color: {} Type: {}'.format(
            self.__x, self.__y, self.__color,self.__Type)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = float(x)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = float(y)

    @property
    def Type(self):
        return self.__Type
    @property
    def color(self):
        return self.__color
    

#type: pawn=0,k=1,q=2,k=3,r=4,b=5
pieces=[]
for i in range(0,8):
    #white pawns
    pieces.append(Piece(i,6,0,0))
    #black pawns
    pieces.append(Piece(i,1,1,0))
#wKing
pieces.append(Piece(4,7,0,1))
#bKing
pieces.append(Piece(4,0,1,1))
#wQueen
pieces.append(Piece(3,7,0,2))
#bQueen
pieces.append(Piece(3,0,1,2))
#wKnights
pieces.append(Piece(1,7,0,3))
pieces.append(Piece(6,7,0,3))
#bKnights
pieces.append(Piece(1,0,1,3))
pieces.append(Piece(6,0,1,3))
#wRooks
pieces.append((Piece(0,7,0,4)))
pieces.append((Piece(7,7,0,4)))
#bRooks
pieces.append((Piece(0,0,1,4)))
pieces.append((Piece(7,0,1,4)))
#wBishops
pieces.append((Piece(2,7,0,5)))
pieces.append((Piece(5,7,0,5)))
#bBishops
pieces.append((Piece(2,0,1,5)))
pieces.append((Piece(5,0,1,5)))

turn=0

wPawn=pygame.image.load("wPawn.png")
bPawn=pygame.image.load("bPawn.png")
wKing=pygame.image.load("wKing.png")
bKing=pygame.image.load("bKing.png")
wQueen=pygame.image.load("wQueen.png")
bQueen=pygame.image.load("bQueen.png")
wKnight=pygame.image.load("wKnight.png")
bKnight=pygame.image.load("bKnight.png")
wRook=pygame.image.load("wRook.png")
bRook=pygame.image.load("bRook.png")
wBishop=pygame.image.load("wBishop.png")
bBishop=pygame.image.load("bBishop.png")

Pieces={0:{},1:{},2:{},3:{},4:{},5:{},6:{},7:{}}
for piece in pieces:
    Pieces[piece.y][piece.x]=piece
print(Pieces)
images={0:[wPawn,bPawn],1:[wKing,bKing],2:[wQueen,bQueen],3:[wKnight,bKnight],4:[wRook,bRook],5:[wBishop,bBishop]}
movePiece=False
PiecesLock=threading.Lock()
#placeholder piece
pieceSelected=0
def event():
    global Pieces, movePiece,running,pieceSelected
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running=False
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                #FINDING SELECTED PIECE
                if len(str(pygame.mouse.get_pos()[1]))>=3:
                    pieceY=int(str(pygame.mouse.get_pos()[1])[0])
                else:
                    pieceY=0

                if len(str(pygame.mouse.get_pos()[0]))>=3:
                    pieceX=int(str(pygame.mouse.get_pos()[0])[0])
                else:
                    pieceX=0
                if pieceX in Pieces[pieceY].keys():
                    pieceSelected = Pieces[pieceY][pieceX]
                    pieceSelected.x=(pygame.mouse.get_pos()[0]-50)/100
                    pieceSelected.y=(pygame.mouse.get_pos()[1]-50)/100
                    print(pieceSelected,"coords:",pieceX,pieceY)
                    movePiece=True
                else:
                    print("no piece selected")
            if event.type==pygame.MOUSEMOTION and movePiece==True:
                pieceSelected.x=(pygame.mouse.get_pos()[0]-50)/100
                pieceSelected.y=(pygame.mouse.get_pos()[1]-50)/100

            if event.type==pygame.MOUSEBUTTONUP and event.button==1 and movePiece==True:
                movePiece=False
                print(Pieces[pieceY][pieceX])
                PiecesLock.acquire()
                Pieces[pieceY].pop(pieceX)
                if len(str(pygame.mouse.get_pos()[0]))>=3:
                    pieceSelected.x=int(str(pygame.mouse.get_pos()[0])[0])
                else:
                    pieceSelected.x=0
                if len(str(pygame.mouse.get_pos()[1]))>=3:
                    pieceSelected.y=int(str(pygame.mouse.get_pos()[1])[0])
                else:
                    pieceSelected.y=0
                Pieces[pieceSelected.y][pieceSelected.x]=pieceSelected
                pieceSelected=0
                PiecesLock.release()
            time.sleep(0.01)

event_thread = threading.Thread(target=event)
event_thread.start()
#After moving and capturing pieces, have board flip depending on turn, chess clock

def render():
    screen.blit(chessBoard,(0,0))
    PiecesLock.acquire()
    for column,pieces in Pieces.items():
        for row,piece in pieces.items():
            screen.blit(images[piece.Type][piece.color],(piece.x*100,piece.y*100))
    if pieceSelected!=0:
        print(pieceSelected)
        screen.blit(images[pieceSelected.Type][pieceSelected.color],(pieceSelected.x*100,pieceSelected.y*100))
    PiecesLock.release()
    pygame.display.flip()

while running:
    render()
    clock.tick(60)
pygame.quit()
sys.exit()