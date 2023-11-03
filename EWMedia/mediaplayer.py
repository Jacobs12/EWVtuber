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


#     self.player = EWMediaPlayer(widget=self.window.video_widget)
#     self.player.load_content_filepath('Tmp/1.mp4')
#     self.player.play()
class EWMediaPlayer(object):
    # VLC
    instance: vlc = None
    # 播放器实例
    player = None
    # 播放器widget
    widget = None

    def __init__(self, widget):
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.player = self.instance.media_player_new()
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

    # 加载视频流
    def load_stream(self, stream: str = None):
        if str is None:
            return
        # Put the media in the media player
        media = self.instance.media_new(stream)
        self.player.set_media(media)
        # Parse the metadata of the file
        media.parse()

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
