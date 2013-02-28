#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
GUI
"""

import sys

from PySide.QtGui import (QApplication, QMainWindow, QWidget, QAction,
                          QTextEdit, QVBoxLayout, QHBoxLayout, QCalendarWidget,
                          QPushButton)

from crawlermanager.manager import WebCrawler

class AflafrettirGUI(QMainWindow):
  def __init__(self):
    super(AflafrettirGUI, self).__init__()

    self.initUI()

  def initUI(self):
    self.setMaximumWidth(750)
    window = QWidget()

    self.info = QTextEdit()
    self.info.setReadOnly(True)

    self.cal1 = QCalendarWidget(self)
    self.cal1.setMaximumSize(370, 200)

    self.cal2 = QCalendarWidget(self)
    self.cal2.setMaximumSize(370, 200)

    self.button = QPushButton('Reikna afla', self)
    self.button.clicked.connect(self.calc_catch)

    exit_action = QAction('Exit', self)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Exit Application')
    exit_action.triggered.connect(self.exit)

    menubar = self.menuBar()
    filemenu = menubar.addMenu('&File')
    filemenu.addAction(exit_action)
    
    self.statusBar()

    calendar_layout = QHBoxLayout()
    calendar_layout.addWidget(self.cal1)
    calendar_layout.addWidget(self.cal2)
    calendar_layout.addStretch(1)

    button_layout = QHBoxLayout()
    button_layout.addWidget(self.button)
    button_layout.addStretch(1)

    main_layout = QVBoxLayout()
    main_layout.addLayout(calendar_layout)
    main_layout.addLayout(button_layout)
    main_layout.addWidget(self.info)
    
    window.setLayout(main_layout)
    self.setCentralWidget(window)

    self.setGeometry(300, 300, 350, 500)
    self.setWindowTitle(u'Aflafréttir')
    self.show()
    window.show()

  def calc_catch(self):
    print "Clicked"

  def closeEvent(self, e):
    self.exit()

  def exit(self):
    self.close()
    

def main():
  app = QApplication(sys.argv)
  gui = AflafrettirGUI()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
