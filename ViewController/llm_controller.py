"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
from ViewController.ewbase_controller import BaseController
from Session.langchain_session import LangchainSession


class LLMController(BaseController):
    def setup_ui(self):
        super().setup_ui()
        self.window.llm_sender_button.clicked.connect(self.llm_send_click)

    history: list = None

    # LLM聊天模式回复label
    def llm_send_click(self):
        question = self.window.llm_input_field.toPlainText()
        if question == '' or question is None:
            self.window.llm_response_field.setText('您没有输入任何内容')
        session = LangchainSession()
        self.window.llm_input_field.setText('')
        response, history = session.chat_normal(question=question, history=self.history)
        self.history.extend(history)
        print(question)
        value = f'>> 用户：{question}\nAI：{response}\n\n{self.window.llm_response_field.toPlainText()}'
        self.window.llm_response_field.setText(value)
