"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
import os

try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
except IndexError:
    pass
import sys

import pygame
import sounddevice as sd
import os
import Utils.utils
import threading


class AudioPlayer(object):

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

    def play(self, filename: str = ''):
        if os.path.exists(filename) is False or os.path.isfile(filename) is False:
            print('当前播放的文件路径有误')
            return
        try:
            self.player.unload()
        except:
            print('')
        # VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)
        # pygame.mixer.init(devicename='VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)')
        self.player.load(filename=filename)
        self.player.set_volume(1.0)
        self.player.play(1)

    process_handler = None
    completion_handler = None

    def play_completion_handler(self, filename: str, process_handler=None, completion=None):
        self.completion_handler = completion
        self.process_handler = process_handler
        self.play(filename=filename)
        self.start_timer()

    def start_timer(self):
        timer = threading.Timer(0.5, self.refresh)
        timer.start()

    def refresh(self):
        current_postion = self.player.get_pos()
        if current_postion < 0:
            if self.completion_handler is not None:
                self.completion_handler()
            return
        # print(int(current_postion/1000))
        t = int(current_postion / 1000)
        minute = int(t / 60)
        sec = int(t % 60)
        if self.process_handler is not None:
            self.process_handler(current_postion)
        print(f'当前播放进度：{"%02d" % minute}:{"%02d" % sec}')
        timer = threading.Timer(1.0, self.refresh)
        timer.start()

    # 暂停播放音频
    def pause(self):
        self.player.pause()

    def is_pause(self):
        is_pause = False
        if self.player.get_busy() is True:
            return is_pause
        current_postion = self.player.get_pos()
        if current_postion < 0:
            return is_pause
        else:
            is_pause = True
            return is_pause

    # 恢复音频播放
    def resume(self):
        self.player.unpause()

    def stop(self):
        self.player.stop()

    def test_completion_handler(self, completion_handler=None):
        def completion():
            print('audio completion')
            if completion_handler is not None:
                completion_handler()

        platform = Utils.utils.get_system_platform()
        if platform == 'win':
            self.play_completion_handler(filename='TTmp\\1.mp3', completion=completion)
        else:
            self.play_completion_handler(filename='Tmp/1.mp3', completion=completion)


player: AudioPlayer = AudioPlayer()


def default_player():
    global player
    if player is None:
        player = AudioPlayer()
    return player


def reset_player():
    global player
    if player is not None:
        audio_player: AudioPlayer = player
        audio_player.stop()
        player = None
