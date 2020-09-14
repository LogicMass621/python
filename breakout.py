#!/usr/bin/python3
import pygame
import math
import sys


class Rect:

    def __init__(self, x: float, y: float, width: int, height: int):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__pyg_rect = pygame.Rect(
            self.__x, self.__y, self.__width, self.__height)

    def __str__(self):
        return 'x: {} y: {} width: {} height: {}'.format(self.__x, self.__y,
                                                         self.__width, self.__height)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = float(x)
        self.__pyg_rect.x = self.__x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = float(y)
        self.__pyg_rect.y = self.__y

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def colliderect(self, other):
        if self.x+self.width >= other.x and \
                other.x+other.width >= self.x and \
                self.y+self.height >= other.y and \
                other.y+other.height >= self.y:
            return True

    def rectintersection(self, other):
        x5 = max(self.x, other.x)
        x6 = min(self.x+self.width, other.x+other.width)
        y5 = max(self.y, other.y)
        y6 = min(self.y+self.height, other.y+other.height)
        if x5 >= x6 or y5 >= y6:
            return Rect(0, 0, 0, 0)
        return Rect(x5, y5, x6-x5, y6-y5)

    def toPygame(self):
        return self.__pyg_rect


pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.init()
pygame.font.init()

print('PyGame Version', pygame.version.ver)
print('SDL Version', pygame.get_sdl_version())

screenWidth = 800
screenHeight = 800

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 7, 58)
green = (50, 255, 50)
teal = (0, 255, 255)

pygame.display.set_caption('Breakout!')

surface = pygame.display.set_mode((screenWidth, screenHeight))

screens = []
pygame.mouse.set_visible(False)
blockHit = pygame.mixer.Sound('beep-02.wav')
paddleHit = pygame.mixer.Sound('beep-02.wav')


def stop_sounds():
    blockHit.stop()
    paddleHit.stop()


def block_hit():
    stop_sounds()
    blockHit.play()


def play_hit_sound():
    stop_sounds()
    paddleHit.play()


class Screen:
    def render(self):
        return

    def handleEvent(self, event):
        return


class StartScreen(Screen):
    largeFont = pygame.font.Font('freesansbold.ttf', 80)
    font = pygame.font.Font('freesansbold.ttf', 20)

    textBreakout = largeFont.render('BREAKOUT', True, teal, black)
    textBreakoutX = screenWidth/2-textBreakout.get_width()/2
    textBreakoutY = screenHeight/3

    textStart = font.render('Press SPACE to start', True, teal, black)
    textStartX = screenWidth/2-textStart.get_width()/2
    textStartY = screenHeight/2-textStart.get_height()/2

    def render(self):
        surface.fill(black)

        surface.blit(self.textBreakout,
                     (self.textBreakoutX, self.textBreakoutY))
        surface.blit(self.textStart, (self.textStartX, self.textStartY))

        pygame.display.update()
        return True

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screens.append(GameScreen())
        return True


class EndScreen(Screen):

    font = pygame.font.Font('freesansbold.ttf', 60)

    def render(self):
        surface.fill(black)
        textGameover = self.font.render('YOU WIN!', True, teal, black)
        textGameoverX = screenWidth/2-textGameover.get_width()/2
        textGameoverY = screenHeight/2-textGameover.get_height()/2
        surface.blit(textGameover, (textGameoverX, textGameoverY))
        pygame.display.update()

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screens.pop()
        return True


class GameScreen(Screen):

    font = pygame.font.Font('freesansbold.ttf', 20)
    largeFont = pygame.font.Font('freesansbold.ttf', 60)

    paddleRectWidth = screenWidth/10
    paddleRect = Rect(screenWidth*0.5-paddleRectWidth*0.5,
                      screenHeight*0.9, paddleRectWidth, screenHeight/75)
    paddleMoveSpeed = paddleRectWidth/4

    ballSize = 20

    stepStrength = 20.0

    def __init__(self):
        self.ball_rect = Rect((screenWidth-self.ballSize)/2,
                              screenHeight/2, self.ballSize, self.ballSize)
        self.points = 0
        self.speed = 6
        self.min_speed = 6
        self.max_speed = 12
        self.y_step = self.speed
        self.x_step = 0

        self.blocks = []
        i = 30
        while i < screenWidth-30:
            self.blocks.append(Rect(i, 80, 20, 20))
            i += 50

    def render(self):

        surface.fill(black)

        i = len(self.blocks)-1
        if i == -1:
            screens.pop()
            screens.append(EndScreen())
            return True

        self.ball_rect.y += self.y_step
        self.ball_rect.x += self.x_step
        while i >= 0:
            rect = self.ball_rect.rectintersection(self.blocks[i])

            if rect.width > 0 or rect.height > 0:

                self.blocks.pop(i)
                self.points += 10
                block_hit()

                if rect.width > rect.height:
                    self.y_step = -self.y_step
                else:
                    self.x_step = -self.x_step
            else:
                pygame.draw.rect(surface, red, self.blocks[i].toPygame())
            i -= 1

        textScore = self.font.render(
            'Score: '+str(self.points)+' ', True, black, white)
        textScoreX = screenWidth-textScore.get_width()
        textScoreY = textScore.get_height()/3
        surface.blit(textScore, (textScoreX, textScoreY))

        if self.paddleRect.colliderect(self.ball_rect):
            play_hit_sound()
            ballMidPoint = self.ball_rect.x+self.ballSize/2
            paddleMidPoint = self.paddleRect.x+self.paddleRectWidth/2
            
            midPtDelta = (ballMidPoint - paddleMidPoint)/self.stepStrength

            self.speed += midPtDelta
            self.speed = max(self.min_speed,min(self.speed,self.max_speed))
            
            self.x_step += midPtDelta
            self.x_step = min(self.max_speed,max(self.x_step,-self.max_speed))
            
            self.y_step = - \
                math.sqrt(abs(self.speed*self.speed - self.x_step*self.x_step))

            print('hit','speed',self.speed,'xstep',self.x_step,'ystep',self.y_step)

        if self.ball_rect.y + self.ballSize > screenHeight:
            screens.pop()
            return False

        if self.ball_rect.y < 0:
            self.ball_rect.y = 0
            self.y_step = -self.y_step
            play_hit_sound()

        if self.ball_rect.x < 0:
            self.ball_rect.x = 0
            self.x_step = -self.x_step
            play_hit_sound()

        if self.ball_rect.x + self.ballSize > screenWidth:
            self.ball_rect.x = screenWidth-self.ball_rect.width
            self.x_step = -self.x_step
            play_hit_sound()

        pygame.draw.rect(surface, teal, self.paddleRect.toPygame())
        pygame.draw.rect(surface, green, self.ball_rect.toPygame())

        pygame.display.update()
        return True

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.paddleRect.x = min(
                    self.paddleRect.x + self.paddleMoveSpeed, screenWidth - self.paddleRectWidth)
            if event.key == pygame.K_LEFT:
                self.paddleRect.x = max(
                    self.paddleRect.x - self.paddleMoveSpeed, 0)
            if event.key == pygame.K_DELETE:
                self.blocks.pop()
        elif event.type == pygame.MOUSEMOTION:
            self.paddleRect.x = min(max(pygame.mouse.get_pos()[0] - self.paddleRectWidth*0.5, 0),
                                    screenWidth-self.paddleRectWidth)
        return True


pygame.key.set_repeat(50, 0)
screens.append(StartScreen())

clock = pygame.time.Clock()

while True:
    if not screens:
        break
    screen = screens[-1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        screen.handleEvent(event)

    screen.render()
    clock.tick(60)
