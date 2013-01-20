#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
GUI
"""

import sys

from PySide.QtGui import (QApplication, QMainWindow, QWidget, QAction)

class AflafrettirGUI(QMainWindow):
  def __init__(self):
    super(AflafrettirGUI, self).__init__()

    self.initUI()

  def initUI(self):
    window = QWidget()

    exit_action = QAction('Exit', self)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Exit Application')
    exit_action.triggered.connect(self.exit)

    menubar = self.menuBar()
    filemenu = menubar.addMenu('&File')
    filemenu.addAction(exit_action)
    
    self.statusBar()

    self.setGeometry(300, 300, 350, 250)
    self.setWindowTitle(u'Aflafréttir')
    self.show()
    window.show()

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
