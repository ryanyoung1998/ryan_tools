# 导入所需要的模块
import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import openai

# 创建一个QWidget
class ChatWindow(QWidget):
    # 初始化
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatGPT (free edition)")
        self.setGeometry(300, 300, 500, 500)
        self.initUI()
 
    # 创建UI
    def initUI(self):
        # 创建一个QTextEdit，用于显示聊天记录
        self.chatTextEdit = QTextEdit(self)
        self.chatTextEdit.setReadOnly(True)
        self.chatTextEdit.setGeometry(10, 10, 480, 350)
        self.chatTextEdit.setStyleSheet("""
            QTextEdit {
                padding: 5px;
                margin: 0px;
                background-color: #f2f2f2;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            QTextEdit:hover {
                background-color: #fff;
                border: 1px solid #aaa;
            }
        """)
 
        # 创建一个QLineEdit，用于输入聊天信息
        self.inputLineEdit = QLineEdit(self)
        self.inputLineEdit.setPlaceholderText('请输入您的问题')
        self.inputLineEdit.setGeometry(10, 370, 480, 30)
        self.inputLineEdit.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                margin: 0px;
                background-color: #ffffff;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            QLineEdit:focus{
                border: 1px solid #aaa;
            }
            QLineEdit!:focus{
                border: 1px solid #ccc;
            }
        """)

 
        # 创建一个发送按钮
        self.sendBtn = QPushButton(self)
        self.sendBtn.setText("发送")
        self.sendBtn.setGeometry(400, 410, 80, 30)
        self.sendBtn.setStyleSheet("""
            QPushButton {
                padding: 5px;
                margin: 0px;
                background-color: #f2f2f2;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            QPushButton:hover {
                background-color: #fff;
                border: 1px solid #aaa;
            }
        """)

        self.enterShortcut = QShortcut(QKeySequence("Enter"), self)
        self.enterShortcut.activated.connect(self.sendMsg)
        
        # 绑定发送按钮的点击事件
        self.sendBtn.clicked.connect(self.sendMsg)

    # 发送消息
    def sendMsg(self):
        # 获取输入框中的内容
        msg = self.inputLineEdit.text()
        if msg != '':
            # 将内容添加到文本框中
            self.chatTextEdit.append('\n我：' + msg)
            # 清空输入框
            self.inputLineEdit.clear()

            # 调用OpanAI
            openai.api_key = "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"
            model_engine = "text-davinci-003"
            # 限制1024字节   512汉字
            prompt = msg
            res = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            # 将内容添加到文本框中
            msg = res.choices[0].text
            self.chatTextEdit.append('\nChatGPT：' + msg)
        else:
            self.chatTextEdit.append('\nChatGPT：输入框不能为空哦~' )

 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatWindow = ChatWindow()
    chatWindow.show()
    sys.exit(app.exec())