"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject


class MyThread(QThread):
    func = None
    signal = None

    def __init__(self):
        super().__init__()

    def run(self):
        if self.func is not None:
            self.func()

    def get_mainloop(self, message: str):
        print(message)
        if self.signal is not None:
            self.signal.emit(message)


class Thread(QObject):
    thread: MyThread = None
    tag: int = 0

    def __init__(self):
        # """
        #     t = None
        #
        #     def testt(self):
        #         t = Thread()
        #         self.t = t
        #         self.t.start(func=self.run)
        #
        #     # 子线程运行的内容
        #     async def run(self):
        #         print('子线程开始')
        #         time.sleep(5)
        #         print('子线程回调')
        #         # 返回主线程
        #         self.t.get_mainloop(message='接收到子线程的消息了',func=self.callback)
        #
        #     # 主线程运行的内容
        #     def callback(self,message):
        #         print('主')
        #         print(message)
        #         self.window.cartoon_queue1_browser.setText(message)
        # """
        super().__init__()

    noti: str = None
    func = None
    recive_event_signal: pyqtSignal = pyqtSignal(str)

    def start(self, func):
        print('11111111111')
        self.recive_event_signal.connect(self.did_recieve_signal)
        t = MyThread()
        self.thread = t
        t.signal = self.recive_event_signal
        t.func = func
        t.target = self
        t.start()

    def get_mainloop(self, message: str, func):
        self.func = func
        self.thread.get_mainloop(message=message)

    def did_recieve_signal(self, noti: str):
        print('接收到消息')
        self.func(noti)

    def destroy(self):
        self.thread.exit()
