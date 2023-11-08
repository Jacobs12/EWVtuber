"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
import vlc
import platform
from PyQt5 import QtWidgets, QtGui, QtCore
import threading
from decimal import Decimal

#     self.player = EWMediaPlayer(widget=self.window.video_widget)
#     self.player.load_content_filepath('Tmp/1.mp4')
#     self.player.play()
class EWMediaPlayer(object):
    # VLC
    instance: vlc = None
    # 播放器实例
    player:vlc.MediaPlayer = None
    # 播放器widget
    widget = None

    def __init__(self, widget):
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        # self.player = self.instance.media_player_new()
        self.player = vlc.MediaPlayer()
        self.set_widget(widget=widget)

    # 设置播放器widget
    def set_widget(self, widget):
        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this
        if widget is not None:
            if platform.system() == "Linux":  # for Linux using the X Server
                self.player.set_xwindow(int(widget.winId()))
            elif platform.system() == "Windows":  # for Windows
                self.player.set_hwnd(int(widget.winId()))
            elif platform.system() == "Darwin":  # for MacOS
                self.player.set_nsobject(int(widget.winId()))

    # 加载本地视频
    def load_content_filepath(self, filepath: str = None):
        if str is None:
            return
        # Put the media in the media player
        media = self.instance.media_new(filepath)
        self.player.set_media(media)

        # Parse the metadata of the file
        media.parse()
        self.player.set_mrl()

    count = 0
    timer:threading.Timer = None
    def update_events(self):
        if self.player.is_playing() == 0 and self.player.get_time() > 0.5:
            self.video_finished()
            return 
        self.timer = threading.Timer(0.001, self.update_events)
        self.timer.start()
    def load_camera(self):
        self.load_content_filepath(f'Tmp/camera/video/{self.count}.mp4')
        print(f'Tmp/camera/video/{self.count}.mp4')
        self.timer = threading.Timer(0.001, self.update_events)
        self.timer.start()
        # event = self.player.event_manager()
        # vlc.EventType.MediaPlayerEndReached
        # event.event_attach(vlc.EventType.MediaPlayerEndReached, self.video_finished(), 1)


    def video_finished(self):
        print('播放结束')
        self.count += 1
        self.load_camera()
        self.play()

    # 加载视频流
    def load_stream(self, stream: str = None):
        if str is None:
            return
        # Put the media in the media player
        media = self.instance.media_new(stream)
        self.player.set_media(media)
        # Parse the metadata of the file
        media.parse()

    # def load_cammera(self):
    #     self.instance = vlc.Instance("--no-xlib")
    #     instance = self.instance
    #     player = instance.media_player_new()
    #     player.set_mrl('v4l2:///dev/FaceTime HD Camera')
    #     player.video_set_format("RV24", 640, 480, 0)
    #     player.set_hwnd(0)
    #     player.play()
    #     self.player = player

    # 播放
    def play(self):
        self.player.play()

    # 暂停
    def pause(self):
        self.player.pause()

    # 停止
    def stop(self):
        self.player.stop()

    def create_ui(self):
        if platform.system() == "Darwin":  # for MacOS
            videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            videoframe = QtWidgets.QFrame()
        palette = videoframe.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        videoframe.setPalette(palette)
        videoframe.setAutoFillBackground(True)
