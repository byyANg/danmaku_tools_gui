import subprocess
import sys

import danmaku_tools.danmaku_energy_map
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QVBoxLayout, \
    QHBoxLayout


class CommandExecutionThread(QThread):
    finished = Signal()

    def __init__(self, command):
        super().__init__()
        self.command = command
        print(f"cmd: {command}")

    def run(self):
        try:
            subprocess.run(self.command, check=True, shell=True, text=True)
        except Exception as e:
            print(f"命令执行失败: {e}")
        finally:
            self.finished.emit()


class FileSelectorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.label_instruction = QLabel("选择xml文件", self)
        self.lineEdit_path = QLineEdit(self)
        self.button_browse = QPushButton("选择文件", self)
        self.button_browse.clicked.connect(self.browse_file)
        self.button_confirm = QPushButton("确认", self)
        self.button_confirm.clicked.connect(self.show_result)
        self.result_msg = QLabel("", self)

        layout = QVBoxLayout()
        layout.addWidget(self.label_instruction)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.lineEdit_path)
        h_layout.addWidget(self.button_browse)
        layout.addLayout(h_layout)
        layout.addWidget(self.result_msg)
        # 创建水平布局来专门放置按钮，使其能够居中
        # button_layout = QHBoxLayout()
        # button_layout.setAlignment(Qt.AlignHCenter)  # 设置水平居中对齐
        # button_layout.addWidget(self.button_confirm)  # 将按钮添加到布局中
        # 调整按钮宽度和居中
        # self.button_confirm.setStyleSheet("QPushButton {"
        #                                   "width: 80px;"  # 按钮宽度设置为80像素，您可以按需调整
        #                                   "text-align: center;"  # 文本居中
        #                                   "}")

        # 替换原有的按钮直接添加到主布局，改为添加这个居中的按钮布局
        # layout.addLayout(button_layout)  # 使用button_layout替换原来的layout.addWidget(self.button_confirm)
        layout.addWidget(self.button_confirm)
        self.setLayout(layout)

        self.setWindowTitle('弹幕高能片段')
        self.setGeometry(200, 200, 300, 120)
        self.show()

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if file_path:
            self.lineEdit_path.setText(file_path)

    def show_result(self):
        # print(f"filepath:{self.lineEdit_path.text()}")
        # cmd_thread = CommandExecutionThread(
        #     f"python -m danmaku_tools.danmaku_energy_map " + self.lineEdit_path.text() + \
        #     f" --he_map ./output/he_list.txt " +
        #     f" --sc_list ./output/sc_list.txt "
        # )
        self.handle_process_started()
        params = danmaku_tools.danmaku_energy_map.init_params(self.lineEdit_path.text(), None, "./output/he_list.txt", "./output/sc_list.txt", None, None, None)
        danmaku_tools.danmaku_energy_map.energy_map_params(params)
        self.handle_process_finished()
        # cmd_thread.finished.connect(self.handle_process_finished)
        # cmd_thread.start()

    def handle_process_started(self):
        self.result_msg.setText("生成中...")

    def handle_process_finished(self):
        self.result_msg.setText("生成结束")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSelectorGUI()
    sys.exit(app.exec())
