from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QApplication, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread
import sys
import praw
import config
import time


class PostingThread(QThread):
    def __init__(self, mainwindow, parant=None):
        super().__init__()
        self.mainwindow = mainwindow

    def run(self):
        self.subbred = self.mainwindow.subreddit_text.toPlainText()
        reddit = praw.Reddit(client_id=config.client_id,
                             client_secret=config.client_secret,
                             user_agent=config.user_agent,
                             username=config.username,
                             password=config.password)
        self.subreddit = reddit.subreddit(self.subbred)
        nomber_phohto = 0
        while True:
            kolichestvo = self.mainwindow.kol_vo.toPlainText()
            son_v_sec = self.mainwindow.sec_meg_post.toPlainText()
            son_v_porc = self.mainwindow.sec_meg_porc.toPlainText()
            title = self.mainwindow.title.toPlainText()
            self_text = self.mainwindow.body_post.toPlainText()
            spis = self.mainwindow.photos
            if self.mainwindow.runed:
                for i in range(int(kolichestvo)):
                    if nomber_phohto == 4:
                        nomber_phohto = 0
                    self.subreddit.submit_image(title, image_path=spis[nomber_phohto], nsfw=True)
                    time.sleep(int(son_v_sec))
                    self.mainwindow.otpravl += 1
                    nomber_phohto += 1
                    self.mainwindow.otprav.setText(str(self.mainwindow.otpravl))
            time.sleep(int(son_v_porc))


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        loadUi('ui.ui', self)
        self.photo1.clicked.connect(self.load_photo1)
        self.photo2.clicked.connect(self.load_photo2)
        self.photo3.clicked.connect(self.load_photo3)
        self.photo4.clicked.connect(self.load_photo4)
        self.start.clicked.connect(self.started)
        self.stop.clicked.connect(self.stoped)
        self.traed = PostingThread(mainwindow=self)
        self.otprav.setText('0')
        self.status.setText('Не работает')
        self.otpravl = 0
        self.photos = []
        self.runed = False

    def started(self):
        self.status.setText('Работает')
        self.runed = True
        self.traed.start()

    def stoped(self):
        self.status.setText('Не работает')
        self.runed = False
        self.traed.start()

    def load_photo1(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:')
        self.name_photo1.setText(fname[0])
        self.photos.append(self.name_photo1.text())

    def load_photo2(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:')
        self.name_photo2.setText(fname[0])
        self.photos.append(self.name_photo2.text())

    def load_photo3(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:')
        self.name_photo3.setText(fname[0])
        self.photos.append(self.name_photo3.text())

    def load_photo4(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:')
        self.name_photo4.setText(fname[0])
        self.photos.append(self.name_photo4.text())


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

