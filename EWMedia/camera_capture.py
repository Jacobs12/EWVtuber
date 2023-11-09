"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
import io
import os
import sys
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2

try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
except:
    print('')

import cv2
import pygame.camera
import pygame.image
import threading
import os
# import imageio.v2 as imageio
from PIL import Image
from decimal import *
import numpy as np
from PyQt5.QtCore import Qt


def get_camera() -> list:
    pygame.camera.init()
    camera_id_list = pygame.camera.list_cameras()
    print(camera_id_list)
    return camera_id_list


class CameraCapture(object):
    label: QLabel = None
    cap: cv2.VideoCapture = None
    CAM_NUM: int = 0
    timer: QTimer = None

    def __init__(self, video_label: QLabel,channel:int):
        self.label = video_label
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = channel

    # 播放视频画面
    # def init_timer(self):
    # if self.timer is None:
    #     self.timer = QTimer(self)
    #     self.timer.timeout.connect(self.show_pic)

    def open_camera(self):
        # self.init_timer()
        # 获取选择的设备名称
        # index = self.comboBox.currentIndex()
        # print(index)
        # self.CAM_NUM = 3
        # 检测该设备是否能打开
        flag = self.cap.open(self.CAM_NUM)
        print(flag)
        if flag is False:
            # QMessageBox.information(self, "警告", "该设备未正常连接", QMessageBox.Ok)
            print('该设备未连接')
        else:
            # 幕布可以播放
            # self.label.setEnabled(True)
            # # 打开摄像头按钮不能点击
            # self.pushButton.setEnabled(False)
            # # 关闭摄像头按钮可以点击
            # self.pushButton_2.setEnabled(True)
            # self.timer.start()
            # print("beginning！")
            # self.show_pic()
            timer = threading.Timer(float(Decimal(1.0) / Decimal(30.0)), self.show_pic)
            timer.start()

    def show_pic(self):
        ret, img = self.cap.read()
        if ret:
            cur_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # 视频流的长和宽
            height, width = cur_frame.shape[:2]
            pixmap = QImage(cur_frame, width, height, QImage.Format_RGB888)
            # pixmap = QPixmap.fromImage(pixmap)
            pixmap = QPixmap.fromImage(pixmap).scaled(380, 210)
            # 获取是视频流和label窗口的长宽比值的最大值，适应label窗口播放，不然显示不全
            # ratio = max(width / self.label.width(), height / self.label.height())
            # pixmap.setDevicePixelRatio(ratio)
            # # 视频流置于label中间部分播放
            # self.label.setAlignment(Qt.AlignCenter)
            self.label.setPixmap(pixmap)
            timer = threading.Timer(float(Decimal(1.0) / Decimal(30.0)), self.show_pic)
            timer.start()

    # timer: threading.Timer = None
    # camera: pygame.camera.Camera = None
    # video_count: int = 0
    # img_lst = []
    # max = 20
    # # fps = Decimal(1.0)/Decimal(30.0)
    # fps = Decimal(1.0) / Decimal(max)
    # count: int = 0

    # def refresh(self):
    #     if self.camera is None:
    #         cameraname = get_camera()[0]
    #         self.camera = pygame.camera.Camera(cameraname)
    #         self.camera.start()
    #     img = self.camera.get_image()
    #     img = pygame.transform.scale(img, (512, 360))
    #
    # # img_bytes = pygame.image.tostring(img, "RGB", False)
    # # img_image = Image.frombytes("RGB", (1024, 768), img_bytes)
    # # Image.frombytes()
    # # img_image = np.asarray(bytearray(img_bytes), dtype="uint8")
    # pygame.image.save(img, f'Tmp/camera/img/{self.count}.jpg')
    # # self.img_lst.append(img_image)
    # self.count += 1
    # if self.count >= self.max:
    #     self.gen_videonew()
    #
    # # print('refresh')
    # timer = threading.Timer(self.fps, self.refresh)
    # timer.start()

    # def capture(self):
    #     timer = threading.Timer(self.fps, self.refresh)
    #     timer.start()

    # def gen_videonew(self):
    #     # 图片转视频代码
    #     import cv2
    #     import os
    #     # 图片文件夹路径
    #     image_folder = r'Tmp/camera/img/'
    #
    #     # 视频输出路径及文件名
    #     video_name = f'Tmp/camera/video/{self.video_count}.mp4'
    #     self.video_count += 1
    #     self.count = 0
    #
    #     # 获取所有图片文件名并排序
    #     images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    #     images.sort()
    #
    #     frame = cv2.imread(os.path.join(image_folder, images[0]))
    #     height, width, layers = frame.shape
    #
    #     # 使用cv2.VideoWriter()创建视频编写器VideoWriter_fourcc
    #     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或者使用其他视频编解码器例如'XVID'
    #     video = cv2.VideoWriter(video_name, fourcc, self.max, (width, height))
    #
    #     # 循环读取图片并写入视频
    #     for image in images:
    #         video.write(cv2.imread(os.path.join(image_folder, image)))
    #
    #     # 释放资源
    #     cv2.destroyAllWindows()
    #     video.release()

    # def gen_video(self):
    #     print('视频')
    #     img_dir = 'Tmp/camera/img/'
    #     video_dir = 'Tmp/camera/'
    #     filename = 'output.mp4'
    #     # filepath = os.path.join(os.getcwd(), filename)
    #     # 读取所有 PNG 图片
    #     filepath = f'{video_dir}{filename}'
    #     images = []
    #     for file_name in sorted(os.listdir(img_dir)):
    #         if file_name.endswith('.png'):
    #             print(file_name)
    #             path = f'{img_dir}{file_name}'
    #             images.append(Image.open(path))
    #     # 将图片转换为视频
    #     fps = 30  # 每秒钟30帧
    #     with imageio.get_writer(filepath, fps=fps) as video:
    #         for image in images:
    #             frame = image.convert('RGB')
    #             video.append_data(frame)
