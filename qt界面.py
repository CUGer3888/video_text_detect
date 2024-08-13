# 制作一个qt界面，获取用户想要处理的文件地址，将获得的地址传递给一个值
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
import cv2
import numpy as np
import ffmpeg
from paddleocr import PaddleOCR
ocr = PaddleOCR(lang='ch')
import time
import csv
class VideoProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 添加处理文件保存地址选项
        self.setWindowTitle('视频处理')
        self.setGeometry(100, 100, 500, 400)

        self.label = QLabel('请选择要处理的视频文件:', self)
        self.label.move(20, 20)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 50)
        self.textbox.resize(260, 30)

        self.button = QPushButton('选择文件', self)
        self.button.move(20, 90)
        self.button.clicked.connect(self.selectFile)

        self.label_1 = QLabel('请选择要保存的视频文件地址(全英文路径):', self)
        self.label_1.move(20, 130)

        self.textbox_1 = QLineEdit(self)
        self.textbox_1.move(20, 150)
        self.textbox_1.resize(260, 30)

        self.label_2 = QLabel('请输入处理开始时间:', self)
        self.label_2.move(300, 20)
        self.textbox_3 = QLineEdit(self)
        self.textbox_3.move(300, 30)

        self.label_3 = QLabel('请输入处理结束时间:', self)
        self.label_3.move(300, 60)
        self.textbox_4 = QLineEdit(self)
        self.textbox_4.move(300, 80)

        self.label_4 = QLabel('请输入处理帧率:', self)
        self.label_4.move(300, 100)

        self.textbox_2 = QLineEdit(self)
        self.textbox_2.move(300, 120)

        # 添加保存地址选项，选文件夹而不是具体得到文件
        self.button_1 = QPushButton('选择保存地址', self)
        self.button_1.move(20, 190)
        self.button_1.clicked.connect(self.selectFile_1)

        self.processButton = QPushButton('开始处理', self)
        self.processButton.move(20, 240)
        self.processButton.clicked.connect(self.processVideo)

        self.showPutton = QPushButton('显示视频信息', self)
        self.showPutton.move(50, 280)
        self.showPutton.clicked.connect(self.showVideoInfo)

        self.totel_button = QPushButton('文字识别', self)
        self.totel_button.move(50, 310)
        self.totel_button.clicked.connect(self.text_detect)


        self.exitButton = QPushButton('退出', self)
        self.exitButton.move(50, 350)
        self.exitButton.clicked.connect(self.close)
        # self.processButton.setEnabled(False)
        # self.processButton.setEnabled(False)禁用按钮
        # self.processButton.setEnabled(True)启用按钮
        # self.processButton.clicked.connect(self.processVideo)点击按钮时执行processVideo函数

    # 开始使用
    def selectFile_1(self):
        # 创建一个QFileDialog.Options对象
        options = QFileDialog.Options()
        # 设置只读选项
        options |= QFileDialog.ReadOnly
        # 弹出选择保存地址的对话框，并将返回的路径赋值给save_path变量
        save_path = QFileDialog.getExistingDirectory(self, "选择保存地址", "", options=options)
        if save_path:
            self.textbox_1.setText(save_path)
            print(save_path)
    def close(self):
        sys.exit()

    def selectFile(self):  # 选择文件
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文件", "",
                                                  "All Files (*);;MP4 Files (*.mp4);;AVI Files (*.avi)",
                                                  options=options)
        if fileName:
            self.textbox.setText(fileName)
            self.processButton.setEnabled(True)  # 选择文件后启用按钮

    def text_detect(self):
        video_path = self.textbox.text()
        save_path = self.textbox_1.text()
        cap = cv2.VideoCapture(video_path)

        # 获取视频总帧数和FPS
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # 设置帧率，开始时间和结束时间
        frameRate = int(self.textbox_2.text()) if self.textbox_2.text() else 30
        start_time = int(self.textbox_3.text()) if self.textbox_3.text() else 0
        end_time = int(self.textbox_4.text()) if self.textbox_4.text() else int(total_frames / fps)

        # 创建csv文件
        nowtime = time.time()
        csv_file_path = os.path.join(save_path, f'{nowtime}.csv')


        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 检查当前帧是否在指定的时间范围内
            if start_time * fps <= frame_idx < end_time * fps and frame_idx % frameRate == 0:
                result = ocr.ocr(frame)
                dic = {}
                for i in range(20):
                    try:
                        x = result[0][i][1][0]
                        dic[i+frame_idx*20] = x
                    except:
                        pass

            frame_idx += 1
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for item in dic:
                writer.writerow([item, dic[item]])
        print("文本检测和保存完成")
        cap.release()


    def showVideoInfo(self):
        # 弹窗显示视频信息
        # 显示总时间
        video_path_1 = self.textbox.text()
        cap = cv2.VideoCapture(video_path_1)
        time = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        # print(fps, width, height, total_frames)
        QMessageBox.information(self, "视频信息",
                                f"视频帧率：{fps}\n视频宽度：{width}\n视频高度：{height}\n视频总帧数：{total_frames} \n 视频总时间{time}秒")
        cap.release()

    def processVideo(self):
        video_path = self.textbox.text()
        save_path = self.textbox_1.text()
        cap = cv2.VideoCapture(video_path)
        frameRate_str = self.textbox_2.text()
        start_time_str = self.textbox_3.text()
        end_time_str = self.textbox_4.text()

        # 获取视频总帧数和FPS
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # 设置帧率，开始时间和结束时间
        frameRate = int(frameRate_str) if frameRate_str else 30
        start_time = int(start_time_str) if start_time_str else 0
        end_time = int(end_time_str) if end_time_str else int(total_frames / fps)

        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 检查当前帧是否在指定的时间范围内
            if start_time * fps <= frame_idx < end_time * fps and frame_idx % frameRate == 0:
                frame_num = int(frame_idx / fps) + 1
                print(f"开始截取视频第：{frame_num} 帧")
                frame_save_path = os.path.join(save_path, f'{str(frame_num)}.jpg')
                cv2.imwrite(frame_save_path, frame)

            frame_idx += 1

        print("处理结束")
        cap.release()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoProcessor()
    window.show()
    sys.exit(app.exec_())
