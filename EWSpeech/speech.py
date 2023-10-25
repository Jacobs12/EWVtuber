"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""

import pyttsx3
import io
import sys
import os
from Audio.audio import AudioManager


class Speaker(object):
    audio_manager: AudioManager = None
    output_path = 'Buffer\\Audio\\speech.wav'

    def __init__(self) -> None:
        self.text = ''

    def speak(self, text: str):
        print(sys.platform)
        try:
            self.audio_manager.player.unload()
            os.remove(self.output_path)
        except:
            pass
        engine = pyttsx3.init()

        # 获取语音包
        voices = engine.getProperty('voices')
        for voice in voices:
            print('id = {}\tname = {} \n'.format(voice.id, voice.name))
        # 设置使用的语音包
        engine.setProperty('voice', 'zh')  # 开启支持中文
        # engine.setProperty('voice', voices[0].id)

        # 改变语速  范围为0-200   默认值为200
        rate = engine.getProperty('rate')  # 获取当前语速
        engine.setProperty('rate', rate - 40)

        # 设置音量  范围为0.0-1.0  默认值为1.0
        engine.setProperty('volume', 0.7)

        # 预设要朗读的文本数据
        line = text  # 要播报的内容
        self.text = text
        # engine.say(line)

        engine.save_to_file(line, self.output_path)

        # 朗读
        engine.runAndWait()
