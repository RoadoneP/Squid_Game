#-*-coding:utf-8-*-
import sys
import os

import cv2
import numpy as np
import jetson.inference
import jetson.utils
import serial
import time
import threading
import random
import pygame.mixer


# from playsound import playsound
# import keyboard


# 영희의 상태
robot_status = 'blind' # (blind, speaking, looking)
# 플레이어의 상태
player_status ='alive' # (alive, dead)
MOVE_THRESHOLD = 2000
cx = 0
cy = 0
flag = True
P1 = 320
P2 = 240
ALPHA = 25
BETA = 20
pygame.mixer.init()
MP3_1 = pygame.mixer.Sound('./sound/squid_game_1.mp3')
MP3_2 = pygame.mixer.Sound('./sound/squid_game_2.mp3')
MP3_3 = pygame.mixer.Sound('./sound/squid_game_3.mp3')
MP3_4 = pygame.mixer.Sound('./sound/squid_game_4.mp3')
MP3_5 = pygame.mixer.Sound('./sound/squid_game_5.mp3')
MP3_6 = pygame.mixer.Sound('./sound/squid_game_6.mp3')
MP3 = [MP3_1,MP3_2,MP3_3,MP3_4,MP3_5,MP3_6]

# 아두이노(영희) 메시지
def send_Younghee(status):
    younghee.write(status.encode())
    time.sleep(0.2)
    msg = younghee.readline().decode('ascii')
    return msg

def start_blind():
    global robot_status
    robot_status = 'blind'
    msg = send_Younghee(robot_status)
    time.sleep(0.2)
    if msg == 'ok':
        #print("blind end")
        start_speaking()

# 스피커 작동 명령
def start_speaking():
    global robot_status
    robot_status = 'speaking'
    rand_sound = random.randint(0, 5)
    # sound_path = "./sound/squid_game_" + str(rand_sound) + ".mp3" 
    MP3[rand_sound].play()
    time.sleep(round(MP3[rand_sound].get_length(),1)-1.3)
    #playsound(sound_path)
    start_looking()


# 영희 모터 회전 및 감지시작
def start_looking():
    msg = send_Younghee('looking')
    global robot_status
    robot_status = 'looking'
    time.sleep(0.2)
    # 아두이노의 응답 & player가 살아있는 경우  
        
        

if __name__ == "__main__":
    younghee = serial.Serial('/dev/ttyACM1', 9600)
    younghee.timeout = 1

    start_blind()

    # Webcam()
    
    
    