#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PySide.QtGui import (QMainWindow, QApplication, QWidget, QTextEdit,
                          QVBoxLayout, QHBoxLayout, QLabel, QDateTimeEdit,
                          QPushButton, QProgressBar, QAction, QFileDialog,
                          QDialog, QLineEdit)
from PySide.QtCore import (QDate)

from multiprocessing import Process, Event, Queue

from landings.manager import LandingsManager
from landings.landings import Landings

from utils.date import split_periods, month_range, check_dates

date_fmt = 'yyyy-MM-dd'

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
    self.cal1.setCalendarPopup(True)
    self.cal1.setDisplayFormat('dd.MM.yyyy')
    
    self.cal2 = QDateTimeEdit(QDate.currentDate())
    self.cal2.setCalendarPopup(True)
    self.cal2.setDisplayFormat('dd.MM.yyyy')

    self.button = QPushButton('Reikna afla', self)
    self.button.clicked.connect(self.fetch_data)

    self.pbar = QProgressBar(self)

    exit_action = QAction('Exit', self)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Exit Application')
    exit_action.triggered.connect(self.close)

    credential_action = QAction(u'Notenda upplýsingar', self)
    credential_action.setStatusTip(u'Slá inn notendanafn og lykilorð')
    credential_action.triggered.connect(self.enter_credentials)

    menubar = self.menuBar()
    filemenu = menubar.addMenu('&File')
    filemenu.addAction(credential_action)
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
    
    self.enter_credentials()

  def enter_credentials(self):
    cred = CredentialsDialog(self)
    cred.show()

  def fetch_data(self):
    """ R
    """

    if self.password and self.username:
      print self.username, self.password

    date_from = self.cal1.date().toString(date_fmt)
    date_to = self.cal2.date().toString(date_fmt)

    if check_dates(date_from, date_to):
      dates = split_periods(date_from, date_to)


    fname, _ = QFileDialog.getSaveFileName(self, 'Vista skrá', '~/')

class CredentialsDialog(QDialog):
  """ A dialog for entering username and password.
  """
  def __init__(self, parent=None):
    """ A initialization function for :class CredentialsDialog:
    
    :param self:    An instance attribute of the :class CredentialsDialog:
    :param parent:  A parent to the :class CredentialsDialog:
    """
    super(CredentialsDialog, self).__init__(parent)

    self.parent = parent
  
    username_label = QLabel(u'Notendanafn:', self)
    password_label = QLabel(u'Lykilorð:', self)
  
    self.username = QLineEdit(self)
    self.password = QLineEdit(self)
    self.password.setEchoMode(QLineEdit.Password)
  
    self.ok_button = QPushButton(u'OK')
    self.cancel_button = QPushButton(u'Cancel')
  
    self.ok_button.clicked.connect(self.push_ok)
    self.cancel_button.clicked.connect(self.close)
  
    user_layout = QHBoxLayout()
    user_layout.addWidget(username_label)
    user_layout.addStretch(1)
    user_layout.addWidget(self.username)
  
    pass_layout = QHBoxLayout()
    pass_layout.addWidget(password_label)
    pass_layout.addStretch(1)
    pass_layout.addWidget(self.password)
  
    button_layout = QHBoxLayout()
    button_layout.addStretch(1)
    button_layout.addWidget(self.cancel_button)
    button_layout.addWidget(self.ok_button)
  
    main_layout = QVBoxLayout()
    main_layout.addLayout(user_layout)
    main_layout.addLayout(pass_layout)
    main_layout.addLayout(button_layout)

    self.setLayout(main_layout)
  
    self.setWindowTitle(u'Sláðu in notendanafn of lykilorð')

  def push_ok(self):
    """ Gets the text that are written in the 2 :class QLineEdit: objects and if
    there is any, it passes the username and password up to the parent of :class
    CredentialsDialog: and finally closes the dialog.
   """
    user = self.username.text()
    passw = self.password.text()

    if user and passw:
      self.parent.username = user
      self.parent.password = passw

    self.close()


def main():
  app = QApplication(sys.argv)
  gui = AflafrettirGUI()
  sys.exit(app.exec_())
