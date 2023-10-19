'''
Author: wolffy
Date: 2023-10-11 17:00:16
LastEditors: fengtao92 1440913385@qq.com
LastEditTime: 2023-10-17 18:37:03
FilePath: /EWVtuber/Audio/audio.py
Description: 项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Copyright (c) 2023 by 北京光线传媒股份有限公司, All Rights Reserved. 
'''
import pygame
import sounddevice as sd
import os

class audioManager(object):
    def __init__(self) -> None:
        # VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)
        # pygame.mixer.init(devicename='VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)')
        devs = sd.query_devices()
        devicename = ''
        for dev in devs:
            device = dev['name']
            if 'VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)' in device:
                devicename = device
        if devicename != '':
            print(f'在设备{devicename}上播放\n')
            pygame.mixer.init(devicename=devicename)
        else:
            pygame.mixer.init()

        self.mixer = pygame.mixer
        self.player = self.mixer.music

    def play(self,filename:str = ''):
        if os.path.exists(filename)==False or os.path.isfile(filename)==False:
            print('当前播放的文件路径有误')
            return
        # VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)
        # pygame.mixer.init(devicename='VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)')
        self.player.load(filename=filename)
        self.player.set_volume(1.0)
        self.player.play(1)

    # 暂停播放音频
    def pause(self):
        self.player.pause()
    
    # 恢复音频播放
    def unpause(self):
        self.player.unpause()

    def test(self):
        self.play(filename='Tmp\\1.mp3')