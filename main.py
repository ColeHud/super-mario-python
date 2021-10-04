import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario
import cv2
import math

camera_port = 1
camera = cv2.VideoCapture(camera_port)

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 64
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

low_ellipse_area_name = 'Low Area'
high_ellipse_area_name = 'High Area'
max_ellipse_area = 40000
low_ellipse_area = 10000
high_ellipse_area = max_ellipse_area


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)

def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)

def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)

def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)

def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)

def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)

def on_low_ellipse_area_thresh_trackbar(val):
    global low_ellipse_area
    global high_ellipse_area
    low_ellipse_area = min(val, high_ellipse_area - 1)
    cv2.setTrackbarPos(low_ellipse_area_name, window_detection_name, low_ellipse_area)

def on_high_ellipse_area_thresh_trackbar(val):
    global low_ellipse_area
    global high_ellipse_area
    high_ellipse_area = max(val, low_ellipse_area + 1)
    cv2.setTrackbarPos(high_ellipse_area_name, window_detection_name, high_ellipse_area)

previous_touches = []
current_touches = []
direction = 0
shift = False
menu = False
select = False
jump = False
special = False
def touchscreen():
    #Read image from camera
    _, frame = camera.read()

    if frame is None:
        print("No frame")
        cv2.destroyAllWindows()
        return []
    
    current_touches = []
    #Convert image to HSV
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Threshold HSV version of image
    frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

    #Show HSV threshold image
    cv2.imshow(window_detection_name, frame_threshold)

    #Find contours in image
    contours, _ = cv2.findContours(frame_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #Create ellipse for each valid contour on original image
#Create ellipse for each valid contour on original image
    for cnt in contours:
        if(len(cnt) >= 5):
            ((centx,centy), (width,height), angle) = cv2.fitEllipse(cnt)
            if((not math.isnan(centx)) and (not math.isnan(centy))
            and (not math.isnan(width)) and (not math.isnan(height))
                and (not math.isnan(angle))):

                #Compute Area of ellipse
                area = math.pi * width * height
                ratio = width / height

                #Plot ellipse and center point of ellipse if fingerprint sized ellipse
                if(area >= low_ellipse_area and area <= high_ellipse_area and ratio < 1.0 and ratio > 0.3):
                    centx = int(centx)
                    centy = int(centy)
                    cv2.ellipse(frame, (centx,centy), (int(width/2),int(height/2)), angle, 0, 360, (0,0,255), 1)

                    current_touches.append([centx, centy])

                    text = "x:" + str(centx) + " y:" + str(centy)
                    cv2.putText(frame, text, (centx - int(width), centy + int(height/2)),
                    cv2.FONT_ITALIC, 0.5, (255,255,255), 1, cv2.LINE_AA)

    #Show contours on original image
    cv2.imshow('Contours', frame)

    return current_touches



windowSize = 640, 480


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = None#Sound()
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound)

    cv2.destroyAllWindows()

    cv2.namedWindow(window_detection_name)

    #Create sliders for HSV thresholding
    cv2.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
    cv2.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
    cv2.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
    cv2.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
    cv2.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
    cv2.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)

    #Create sliders for ellipse thresholding
    cv2.createTrackbar(low_ellipse_area_name, window_detection_name , low_ellipse_area, max_ellipse_area, on_low_ellipse_area_thresh_trackbar)
    cv2.createTrackbar(high_ellipse_area_name, window_detection_name , high_ellipse_area, max_ellipse_area, on_high_ellipse_area_thresh_trackbar)

    while not menu.start:
        menu.update()

    mario = Mario(0, 0, level, screen, dashboard, sound)
    clock = pygame.time.Clock()
    
    while not mario.restart:
        touches = touchscreen()
        # print("Len Touches "+ str(len(touches)))

        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        if mario.pause:
            mario.pauseObj.update()
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update(touches)
        pygame.display.update()
        clock.tick(max_frame_rate)
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
