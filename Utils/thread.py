"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
from PySide6.QtCore import Qt, QThread, Signal, QObject

# 强引用对象，防止内存被提前释放
thread_queue: [] = []


class EWThreadObject(QThread):
    process_handler = None
    completion_handler = None
    value_input = None
    signal = None

    def __init__(self):
        super().__init__()

    def run(self):
        if self.process_handler is not None:
            if self.value_input is not None:
                self.process_handler(self.value_input)
            else:
                self.process_handler()
        self.get_mainloop(self.value_input)

    def get_mainloop(self, message):
        print(message)
        value_output = tuple()
        if message is not None:
            value_output = tuple(message)
        if self.signal is not None:
            self.signal.emit(value_output)


class EWThread(QObject):
    thread: EWThreadObject = None
    tag: int = 0

    def __init__(self):
        # """
        # from Utils.threading import EWThread
        #
        # def process_handler(value_input = None):
        #     print(value)
        #     time.sleep(5)
        #     print('process_handler')
        #
        # def completion_handler(value_input = None):
        #     print('completion_handler')
        #
        # thread = EWThread()
        # thread.start(process_handler=process_handler, completion_handler=completion_handler)
        # """
        super().__init__()

    completion_handler = None
    recive_event_signal: Signal = Signal(tuple)

    def start(self, value_input=None, process_handler=None, completion_handler=None):
        self.recive_event_signal.connect(self.did_recieve_signal)
        t = EWThreadObject()
        self.thread = t
        t.signal = self.recive_event_signal
        t.process_handler = process_handler
        t.completion_handler = completion_handler
        t.value_input = value_input
        self.completion_handler = completion_handler
        t.target = self
        t.start()
        add_thread_queue(self)

    def did_recieve_signal(self, value):
        # print(f'接收到消息{value}')
        if self.completion_handler is not None:
            if value is not None and len(value) != 0:
                self.completion_handler(value)
            else:
                self.completion_handler()
        remove_thread_queue(self)


thread_tag: int = 0


# 强引用对象，防止内存被提前释放
def add_thread_queue(thread: EWThread):
    global thread_tag
    tag = thread_tag
    thread_tag += 1
    thread.tag = tag
    print(tag)
    thread_queue.append(thread)


# 子进程已完成，移出引用序列，释放对象内存
def remove_thread_queue(thread: EWThread):
    result = None
    # print(f'移除前{thread_queue}')
    for obj in thread_queue:
        if obj.tag == thread.tag:
            result = obj
            break
    thread_queue.remove(result)
    # print(f'移除后{thread_queue}')
