"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
from MainWindow import Ui_MainWindow as UIWindow


class BaseController(object):
    window: UIWindow = None

    def __init__(self, window: UIWindow):
        super().__init__()
        self.window = window
        self.init()
        self.setup_ui()

    def setup_ui(self):
        pass

    def init(self):
        pass
