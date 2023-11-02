"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""

from command import CommandManager
from Audio.player import AudioPlayer
from EWSpeech.speech import Speaker
import MainWindow


class Vtuber(object):
    window: MainWindow = None
    cmd_manager: CommandManager = None  # 命令行控制器
    audio_player: AudioPlayer = None  # 音频播放器
    speaker: Speaker = None

    # 单例模式
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Vtuber, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.cmd_manager = CommandManager()
        self.audio_player = AudioPlayer()
        self.cmd_manager.audio_manager = self.audio_player

    # 启动命令行界面模式
    def start_command_line(self):
        while True:
            cmd = input('>> ')
            is_break = self.cmd_manager.check_cmd(cmd=str(cmd))
            if cmd == '--aaa':
                self.audio_player.test()
            if is_break:
                break

    def setup_ui(self):
        self.window.pushButton.clicked.connect(self.click)
     #
     # def click(self):
     #    print('哈哈哈哈哈哈哈哈')

    def play_test(self):
        self.audio_player.test()

    def click(self):
        print('哈哈哈哈哈哈哈')


def audio_player() -> AudioPlayer:
    player = Vtuber().audio_player
    return player

# default_vtuber = Vtuber()
# cmd_manager = default_vtuber.cmd_manager
# audio_player = default_vtuber.audio_player
# speaker = default_vtuber.speaker
