import pygame
from pygame.locals import *
import sys


class Input:
    def __init__(self, entity):
        self.mouseX = 0
        self.mouseY = 0
        self.entity = entity
        self.previous_touches = [[0,0]]

    def checkForInput(self, current_touches):
        events = pygame.event.get()
        self.checkForKeyboardInput(current_touches)
        self.checkForMouseInput(events)
        self.checkForQuitAndRestartInputEvents(events)

    def checkForKeyboardInput(self, current_touches):
        #parse the touches
        direction = 0
        shift = False
        menu = False
        select = False
        jump = False
        special = False

        #should we boost?
        if len(current_touches) == 2:
            shift = True

        if len(current_touches) <= 2:
            for touch in current_touches:
                x = touch[0]
                y = touch[1]
                if(y < 500):
                    if x < 300: #move left
                        direction = -1
                    elif x >= 800: #move right
                        direction = 1
    
                #elif(y >= 500):
                #    jump = True
                
                 
                if len(self.previous_touches) == 1 and len(current_touches) == 1:
                    if current_touches[0][1] - self.previous_touches[0][1] > 50:
                        jump = True
                    if self.previous_touches[0][1] - current_touches[0][1] > 50:
                        jump = True

                self.previous_touches = current_touches
                
        elif len(current_touches) == 3:
            menu = True
        elif len(current_touches) == 4:
            select = True
            self.entity.pause = True
            self.entity.pauseObj.createBackgroundBlur()


        self.entity.traits["goTrait"].direction = direction
        self.entity.traits['goTrait'].boost = shift
        self.entity.traits['jumpTrait'].jump(jump)
        print(jump)

        #print("Dir " + str(direction))
        # pressedKeys = pygame.key.get_pressed()

        """
        if pressedKeys[K_LEFT] or pressedKeys[K_h] and not pressedKeys[K_RIGHT]:
            self.entity.traits["goTrait"].direction = -1
        elif pressedKeys[K_RIGHT] or pressedKeys[K_l] and not pressedKeys[K_LEFT]:
            self.entity.traits["goTrait"].direction = 1
        else:
            self.entity.traits['goTrait'].direction = 0
        """
        #isJumping = pressedKeys[K_SPACE] or pressedKeys[K_UP] or pressedKeys[K_k]
        


    def checkForMouseInput(self, events):
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.isRightMouseButtonPressed(events):
            self.entity.levelObj.addKoopa(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
            self.entity.levelObj.addGoomba(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
            self.entity.levelObj.addRedMushroom(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
        if self.isLeftMouseButtonPressed(events):
            self.entity.levelObj.addCoin(
                mouseX / 32 - self.entity.camera.pos.x, mouseY / 32
            )

    def checkForQuitAndRestartInputEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and \
                (event.key == pygame.K_ESCAPE or event.key == pygame.K_F5):
                self.entity.pause = True
                self.entity.pauseObj.createBackgroundBlur()

    def isLeftMouseButtonPressed(self, events):
        return self.checkMouse(events, 1)

    def isRightMouseButtonPressed(self, events):
        return self.checkMouse(events, 3)

    def checkMouse(self, events, button):
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP and e.button == button:
                return True
        return False
