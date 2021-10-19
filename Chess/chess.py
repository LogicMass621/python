#!/usr/bin/python
import pygame
import sys
import threading
import time
import math

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

Check = False
class Piece:
    def __init__(self, x: int, y: int, color: int):
        self.__x = x
        self.__y = y
        self.__color=color

    def __str__(self):
        return 'x: {} y: {} color: {} Type: {}'.format(
            self.__x, self.__y, self.__color,self.getType())

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
    def color(self):
        return self.__color
    def selectPiece():
        #FINDING SELECTED PIECE
        global Pieces, movePiece, pieceSelected, pieceX,pieceY, PiecesLock
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
            print(Pieces[pieceY])
            PiecesLock.acquire()
            Pieces[pieceY].pop(pieceX)
            PiecesLock.release()
            pieceSelected.x=(pygame.mouse.get_pos()[0]-50)/100
            pieceSelected.y=(pygame.mouse.get_pos()[1]-50)/100
            print(pieceSelected,"coords:",pieceX,pieceY)
            movePiece=True
        else:
            print("no piece selected")
    def grabPiece():
        global pieceSelected
        pieceSelected.x=(pygame.mouse.get_pos()[0]-50)/100
        pieceSelected.y=(pygame.mouse.get_pos()[1]-50)/100
    def placePiece():
        global pieceSelected, movePiece, Pieces, PiecesLock
        movePiece=False
        #finding target square
        if len(str(pygame.mouse.get_pos()[0]))>=3:
            targetX=int(str(pygame.mouse.get_pos()[0])[0])
        else:
            targetX=0
        if len(str(pygame.mouse.get_pos()[1]))>=3:
            targetY=int(str(pygame.mouse.get_pos()[1])[0])
        else:
            targetY=0
        PiecesLock.acquire()
        #check to see if legal move
        if pieceSelected.checkMove(targetX,targetY,pieceX,pieceY):
            if targetX in Pieces[targetY].keys(): #check to see if capture
                if Pieces[targetY][targetX].color==pieceSelected.color:
                    print("same")
                    pieceSelected.x=pieceX
                    pieceSelected.y=pieceY
                    Pieces[pieceY][pieceX]=pieceSelected
                else:
                    print("else")
                    Pieces[targetY].pop(targetX)
                    Pieces[targetY][targetX]=pieceSelected
                    pieceSelected.x=targetX
                    pieceSelected.y=targetY
            else: #no piece on new square
                Pieces[targetY][targetX]=pieceSelected
                pieceSelected.x=targetX
                pieceSelected.y=targetY
        else: #not legal move
            pieceSelected.x=pieceX
            pieceSelected.y=pieceY
            Pieces[pieceY][pieceX]=pieceSelected
        pieceSelected=0
        PiecesLock.release()

class Rook(Piece):
    def __init__(self,x: int, y: int, color: int):
        super().__init__(x, y, color)
        self.__Type=4
    def getType(self):
        return 4
    def checkMove(self,targetX,targetY,pieceX,pieceY):
        piecesList=[]
        if targetY==pieceY:
            if targetX>pieceX:
                for xCoords in Pieces[targetY]:
                    if xCoords>pieceX and xCoords<targetX:
                        return False
            if pieceX>targetX:
                for xCoords in Pieces[targetY]:
                    if xCoords<pieceX and xCoords>targetX:
                        return False
        elif targetX==pieceX:
            for column,row in Pieces.items():
                print(Pieces)
                for pieceXCoord,piece in Pieces[column].items():
                    if pieceXCoord==targetX and pieceXCoord==pieceX:
                        piecesList.append(piece.y)
            print(piecesList,pieceY,targetY)
            if targetY>pieceY:
                for pieceYCoord in piecesList:
                    print(pieceYCoord,pieceY,targetY)
                    if pieceYCoord>pieceY and pieceYCoord<targetY:
                        return False
                        print("no")
            if targetY<pieceY:
                for pieceYCoord in piecesList:
                    if pieceYCoord<pieceY and pieceYCoord>targetY:
                        return False
                        print("no2")
        if targetY!=pieceY and targetX!=pieceX:
            return False
        return True
class Bishop(Piece):
    def __init__(self,x: int, y: int, color: int):
        super().__init__(x, y, color)
    def getType(self):
        return 5
    def checkMove(self, targetX,targetY,pieceX,pieceY):
        direction={1:-1,2:-1,3:-1,4:-1}
        step=1
        if abs(targetX-pieceX)==abs(targetY-pieceY):
            while step<9:
                if pieceY+step*-1 in Pieces.keys():
                    if pieceX+step*-1 in Pieces[pieceY+step*-1].keys() and direction[1]==-1:
                        if Pieces[pieceY+step*-1][pieceX+step*-1].color!=pieceSelected.color:
                            direction[1]=step+1
                        else:
                            direction[1]=step                             
                        print('yeah1')
                if pieceY+step*1 in Pieces.keys():
                    if pieceX+step*1 in Pieces[pieceY+step*1].keys() and direction[2]==-1:
                        if Pieces[pieceY+step*1][pieceX+step*1].color!=pieceSelected.color:
                            direction[2]=step+1
                        else:
                            direction[2]=step                            
                        print('yeah2')
                if pieceY+step*1 in Pieces.keys():
                    if pieceX+step*-1 in Pieces[pieceY+step*1].keys() and direction[3]==-1:
                        if Pieces[pieceY+step*1][pieceX+step*-1].color!=pieceSelected.color:
                            direction[3]=step+1
                        else:
                            direction[3]=step                           
                        print('yeah3')
                if pieceY+step*-1 in Pieces.keys():
                    if pieceX+step*1 in Pieces[pieceY+step*-1].keys() and direction[4]==-1:
                        if Pieces[pieceY+step*-1][pieceX+step*1].color!=pieceSelected.color:
                            direction[4]=step+1
                        else:
                            direction[4]=step                            
                        print('yeah4')

                step+=1
            print(targetX,pieceX,pieceY,targetY,direction)
            print(targetX-pieceX,targetX-pieceX,abs(targetX-pieceX),direction[1])
            if targetX-pieceX < 0 and targetY-pieceY < 0 and (abs(targetX-pieceX)<direction[1] or direction[1]==-1):
                print('yeah1')
                return True
            if targetX-pieceX>0 and targetY-pieceY < 0 and (abs(targetX-pieceX)<direction[4] or direction[4]==-1):
                print('yeah4')
                return True
            if targetX-pieceX>0 and targetY-pieceY > 0 and (abs(targetX-pieceX)<direction[2] or direction[2]==-1):
                print('yeah2')
                return True
            if targetX-pieceX<0 and targetY-pieceY > 0 and (abs(targetX-pieceX)<direction[3] or direction[3]==-1):
                print('yeah3')
                return True
        else:
            return False
            i

        
class Pawn(Piece):
    def __init__(self,x: int, y: int, color: int):
        super().__init__(x, y, color)
    def getType(self):
        return 0
    def checkMove(self, targetX,targetY,pieceX,pieceY):
        print(targetX,targetY,pieceX,pieceY)
        if (self.color==0 and pieceY==6 and targetY==4) or (self.color==1 and pieceY==1 and targetY==3):
            return True
        if (self.color==0 and pieceY-1==targetY and targetX==pieceX) or (self.color==1 and pieceY+1==targetY and targetX==pieceX):
            block=False
            for xCoord,piece in Pieces[targetY].items():
                if xCoord==targetX:
                    block = True
                    print("block")
            if block == False:
                print("no block")
                return True
        if (self.color == 0 and pieceY-1==targetY and (targetX==pieceX-1 or targetX==pieceX+1)) or (self.color == 1 and pieceY+1==targetY and (targetX==pieceX-1 or targetX==pieceX+1)):
            for xCoord,piece in Pieces[targetY].items():
                if xCoord==targetX:
                    return True
        return False

class Knight(Piece):
    def __init__(self,x: int, y: int, color: int):
        super().__init__(x, y, color)
    def getType(self):
        return 3
    def checkMove(self,targetX,targetY,pieceX,pieceY):
        print(abs(targetX-pieceX),abs(targetY-pieceY))
        if (abs(targetX-pieceX)==2 and abs(targetY-pieceY)==1) or (abs(targetX-pieceX)==1 and abs(targetY-pieceY)==2):
            return True
        return False

class King(Piece):
    def __init__(self,x: int, y: int, color: int):
        super().__init__(x, y, color)
    def getType(self):
        return 1
    def checkMove(self,targetX,targetY,pieceX,pieceY):
        #Check but haven't fully implemented
        for column, row in Pieces.items():
            for xCoords,piece in Pieces[column].items():
                if piece.color != self.color and piece.checkMove(targetX,targetY,piece.x,piece.y):
                    Check = True
                    print(Check)
                    return False
        if abs(targetX-pieceX)<2 and abs(targetY-pieceY)<2 and abs(targetY-pieceY)+ abs(targetX-pieceX)<3:
            return True
        return False
class Queen(Piece):
    def __init__(self,x: int, y: int, color: int):
        super().__init__(x, y, color)
    def getType(self):
        return 2
    def checkMove(self,targetX,targetY,pieceX,pieceY):
        print(targetX,targetY,pieceX,pieceY)
        rook=Rook(pieceX,pieceY,4)
        bishop=Bishop(pieceX,pieceY,5)
        if rook.checkMove(targetX,targetY,pieceX,pieceY) or bishop.checkMove(targetX,targetY,pieceX,pieceY):
            return True

#type: pawn=0,k=1,q=2,k=3,r=4,b=5
pieces=[]
for i in range(0,8):
    #white pawns
    pieces.append(Pawn(i,6,0))
    #black pawns
    pieces.append(Pawn(i,1,1))
#wKing
pieces.append(King(4,7,0))
#bKing
pieces.append(King(4,0,1))
#wQueen
pieces.append(Queen(3,7,0))
#bQueen
pieces.append(Queen(3,0,1))
#wKnights
pieces.append(Knight(1,7,0))
pieces.append(Knight(6,7,0))
#bKnights
pieces.append(Knight(1,0,1))
pieces.append(Knight(6,0,1))
#wRooks
pieces.append((Rook(0,7,0)))
pieces.append((Rook(7,7,0)))
#bRooks
pieces.append((Rook(0,0,1)))
pieces.append((Rook(7,0,1)))
#wBishops
pieces.append((Bishop(2,7,0)))
pieces.append((Bishop(5,7,0)))
#bBishops
pieces.append((Bishop(2,0,1)))
pieces.append((Bishop(5,0,1)))

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
                Piece.selectPiece()
            if event.type==pygame.MOUSEMOTION and movePiece==True:
                Piece.grabPiece()
            if event.type==pygame.MOUSEBUTTONUP and event.button==1 and movePiece==True:
                Piece.placePiece()
            time.sleep(0.01)

event_thread = threading.Thread(target=event)
event_thread.start()
#After moving and capturing pieces, have board flip depending on turn, chess clock

def render():
    screen.blit(chessBoard,(0,0))
    PiecesLock.acquire()
    for column,pieces in Pieces.items():
        for row,piece in pieces.items():
            screen.blit(images[piece.getType()][piece.color],(piece.x*100,piece.y*100))
    if pieceSelected!=0:
        print(pieceSelected)
        screen.blit(images[pieceSelected.getType()][pieceSelected.color],(pieceSelected.x*100,pieceSelected.y*100))
    PiecesLock.release()
    pygame.display.flip()

while running:
    render()
    clock.tick(60)
pygame.quit()
sys.exit()