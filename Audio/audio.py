import pygame
import sounddevice as sd

class audioManager(object):
    def __init__(self) -> None:
        # VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)
        # pygame.mixer.init(devicename='VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)')
        pygame.mixer.init()
        self.mixer = pygame.mixer
        self.player = self.mixer.music

    def play(self,filename:str = ''):
        print('play')
        devs = sd.query_devices()
        print('声卡')
        for dev in devs:
            # print(dev['name'])
            device = dev['name']
            if 'Voice' in device:
                print(device)

        # VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)
        # pygame.mixer.init(devicename='VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)')
        self.player.load(filename=filename)
        self.player.set_volume(0.5)
        self.player.play(1)

    def pause(self):
        self.player.pause()
    
    def unpause(self):
        self.player.unpause()