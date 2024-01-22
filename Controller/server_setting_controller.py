"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
import Utils.config
from Controller.server_base_controller import BaseController
from PySide6.QtWidgets import QFileDialog
import Utils.config as config
from Utils.thread import EWThread as Thread

class SettingController(BaseController):
    def setup_ui(self):
        self.setup_button()
        self.setup_default()

    speaker_array:[] = []

    def setup_default(self):
        project_directory = Utils.config.get_project_directory()
        if project_directory != '':
            self.window.setting_projectfolder_label.setText(project_directory)

        def process(input_value):
            speaker_array = Utils.config.get_speaker_array()
            self.speaker_array = speaker_array

        def finished():
            speaker_array = []
            for item in self.speaker_array:
                name = item['name']
                gender = item['gender']
                if 'zh-' not in name:
                    continue
                obj = f'{name} ({gender})'
                speaker_array.append(obj)
            self.window.setting_speaker_combo.clear()
            self.window.setting_speaker_combo.addItems(speaker_array)
        thread = Thread()
        thread.start(value_input='',process_handler=process,completion_handler=finished)

    def setup_button(self):
        self.window.setting_projectfolder_button.clicked.connect(self.select_project_click)


    def select_project_click(self):
        project_directory = Utils.config.get_project_directory()
        target = QFileDialog.getExistingDirectory(dir=project_directory)
        if target is None or target == '':
            return
        config.set_project_directory(target)
        project_directory = Utils.config.get_project_directory()
        self.window.setting_projectfolder_label.setText(project_directory)

