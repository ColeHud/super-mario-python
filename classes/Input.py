import pygame
from pygame.locals import *
import sys


class Input:
    def __init__(self, entity):
        self.mouseX = 0
        self.mouseY = 0
        self.entity = entity

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

        if len(current_touches) == 1:
            if current_touches[0][0] < 500: #move left
                direction = -1
            elif current_touches[0][0] > 800: #move right
                direction = 1
            else: #don't move
                direction = 0

                if len(previous_touches) == 1:
                    if current_touches[0][1] - previous_touches[0][1] > 50:
                        jump = True
                    if previous_touches[0][1] - current_touches[0][1] > 50:
                        special = True
        elif len(current_touches) == 3:
            menu = True
        elif len(current_touches) == 4:
            select = True

        #should we boost?
        if len(current_touches) == 2:
            shift = True

        self.entity.traits["goTrait"].direction = direction
        self.entity.traits['goTrait'].boost = shift

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
        #self.entity.traits['jumpTrait'].jump(isJumping)


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
