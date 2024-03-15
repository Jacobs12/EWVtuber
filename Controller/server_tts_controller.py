"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
import Utils.config
from Controller.server_base_controller import *
from Tools.player import AudioPlayer
import Utils.config as config
from Utils.thread import EWThread as Thread
import Tools.speech as speech
import os

class ServerTTSController(BaseController):
    audio_player: AudioPlayer = None
    folder = 'Buffer/Audio/'
    audio_id:int = 0;
    def setup_ui(self):
        self.setup_button()
        self.setup_default()

    speaker_array: [] = []

    def setup_default(self):
        if os.path.exists(self.folder) is False:
            os.mkdir(self.folder)
        def process(input_value):
            speaker_array = Utils.config.get_speaker_array()
            self.speaker_array = speaker_array

        def finished():
            speaker_array = []
            for item in self.speaker_array:
                name = item['name']
                gender = item['gender']
                obj = f'{name} ({gender})'
                speaker_array.append(obj)
            self.window.tts_speaker_box.clear()
            self.window.tts_speaker_box.addItems(speaker_array)

        thread = Thread()
        thread.start(value_input='', process_handler=process, completion_handler=finished)

    def setup_button(self):
        self.window.tts_start_button.clicked.connect(self.start_button_click)
        self.window.tts_folder_button.clicked.connect(self.folder_button_click)

    def folder_button_click(self):
        os.system(f'open {self.folder}')

    def start_button_click(self):
        if self.audio_player is None:
            self.audio_player = AudioPlayer()
        text = self.window.tts_text_view.toPlainText()
        if len(text) <= 0:
            return
        index = self.window.tts_speaker_box.currentIndex()
        # print(index)
        obj: {} = self.speaker_array[index]
        speaker = obj['name']
        speed = self.window.tts_speed_box.value()
        name = text
        if len(name)>15:
            name = text[0:15:1]
        output = f'{self.folder}{name}_{self.audio_id}.mp3'
        self.audio_id += 1
        speech.text_to_speech(text=text, speaker=speaker,speed=speed,output=output)

        def completion():
            print('')

        self.audio_player.play_completion_handler(output, completion=completion)
        print(text)

