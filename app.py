"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""

from vtuber import Vtuber

if __name__ == '__main__':
    app = Vtuber()
    app.start_command_line()
    # select = str(input('请输入界面模式：\n  1.命令行模式\n  2.可视化界面\n>> '))
    # if select == '1':
    #     app.start_command_line()
    # elif select == '2':
    #     print('可视化界面正在开发中')
    # else:
    #     print('无效的参数')
