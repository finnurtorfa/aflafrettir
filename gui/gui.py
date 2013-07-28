#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PySide.QtGui import (QMainWindow, QApplication, QWidget, QTextEdit,
                          QVBoxLayout, QHBoxLayout, QLabel, QDateTimeEdit,
                          QPushButton, QProgressBar, QAction, QFileDialog, )
from PySide.QtCore import (QDate)

class AflafrettirGUI(QMainWindow):
  """ :class AflafrettirGUI: a PySide GUI :class:. This GUI handles interaction
  with a SOAP service provided by the Icelandic Directorate of Fisheries, and
  outputs the data on an Excel format.
  """

  def __init__(self):
    """ Initialization function of the :class AflafrettirGUI:

    :param self: An instance attribute of the :class AflafrettirGUI:
    """
    super(AflafrettirGUI, self).__init__()

    self.initUI()

  def initUI(self):
    """ GUI specific initialization for the :class AflafrettirGUI:

    :param self: An instance attribute of the :class AflafrettirGUI:
    """
    window = QWidget()

    self.info = QTextEdit()
    self.info.setReadOnly(True)

    cal_text1 = QLabel('Dagsetning 1:', self)
    cal_text2 = QLabel('Dagsetning 2:', self)

    self.cal1 = QDateTimeEdit(QDate.currentDate())
    self.cal1.setDisplayFormat('dd.MM.yyyy')
    self.cal2 = QDateTimeEdit(QDate.currentDate())
    self.cal2.setDisplayFormat('dd.MM.yyyy')

    self.button = QPushButton('Reikna afla', self)
    self.button.clicked.connect(self.fetch_data)

    self.pbar = QProgressBar(self)

    exit_action = QAction('Exit', self)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Exit Application')
    exit_action.triggered.connect(self.close)

    menubar = self.menuBar()
    filemenu = menubar.addMenu('&File')
    filemenu.addAction(exit_action)

    self.statusbar = self.statusBar()

    date_layout1 = QHBoxLayout()
    date_layout1.addWidget(cal_text1)
    date_layout1.addWidget(self.cal1)

    date_layout2 = QHBoxLayout()
    date_layout2.addWidget(cal_text2)
    date_layout2.addWidget(self.cal2)

    calendar_layout = QVBoxLayout()
    calendar_layout.addLayout(date_layout1)
    calendar_layout.addLayout(date_layout2)

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

  def fetch_data(self):
    fname, _ = QFileDialog.getSaveFileName(self, 'Vista skrá', '~/')

    print fname

def main():
  app = QApplication(sys.argv)
  gui = AflafrettirGUI()
  sys.exit(app.exec_())
