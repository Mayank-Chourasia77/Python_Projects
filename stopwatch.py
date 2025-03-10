import sys
from cProfile import label

from PyQt5.QtWidgets import QApplication ,QLabel, QWidget , QVBoxLayout , QHBoxLayout , QPushButton
from PyQt5.QtCore import QTimer , QTime , Qt

class stopWatch(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.time = QTime(0,0,0,0)
        self.label = QLabel("00:00:00.0",self)
        self.start = QPushButton("start",self)
        self.reset = QPushButton("reset", self)
        self.end = QPushButton("end", self)
        self.initUI()

    def initUI(self):
        self.label.setGeometry(300,150,300,10)
        self.setWindowTitle("Stop watch")
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.start)
        vbox.addWidget(self.reset)
        vbox.addWidget(self.end)
        self.setLayout(vbox)

        self.label.setAlignment(Qt.AlignCenter)
        hbox = QHBoxLayout()
        hbox.addWidget(self.start)
        hbox.addWidget(self.reset)
        hbox.addWidget(self.end)
        vbox.addLayout(hbox)

        self.setStyleSheet(""" 
            QPushButton{
             font-size:20px;
             }
             QLabel{
             font-size:30px;
             background-color:#bbd3fa;
             }
        """)

        self.start.clicked.connect(self.start_)
        self.end.clicked.connect(self.stop_)
        self.reset.clicked.connect(self.reset_)
        self.timer.timeout.connect(self.update_timer)


    def start_(self):
        self.timer.start(10)
    def stop_(self):
        self.timer.stop()
    def reset_(self):
        self.timer.stop()
        self.time = QTime(0,0,0,0)
        self.label.setText(self.format_time(self.time))

    def format_time(self,time):
        hour = time.hour()
        min = time.minute()
        sec = time.second()
        mili = time.msec() //10
        return f"{hour:02}:{min:02}:{sec:02}.{mili:02}"
    def update_timer(self):
        self.time = self.time.addMSecs(10)
        self.label.setText(self.format_time(self.time))




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = stopWatch()
    window.show()
    sys.exit(app.exec_())
