"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
import sys
import os

try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
except:
    print('')

import pygame.camera


def get_system_platform():
    platform = sys.platform
    if 'win32' in platform:
        return 'win'
    else:
        return 'linux'


def get_camera_mrl() -> list:
    print()
    pygame.camera.init()
    camera_id_list = pygame.camera.list_cameras()
    print(camera_id_list)
    return camera_id_list





