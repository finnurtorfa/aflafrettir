#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, time

from PySide.QtGui import (QMainWindow, QApplication, QWidget, QTextEdit,
                          QVBoxLayout, QHBoxLayout, QLabel, QDateTimeEdit,
                          QPushButton, QProgressBar, QAction, QFileDialog,
                          QDialog, QLineEdit)
from PySide.QtCore import (QObject, QDate, Signal, Qt, QTimer)

from threading import Thread
from Queue import Queue
#from multiprocessing import Process, Queue

from landings.manager import LandingsManager
from landings.landings import Landings, sort_landings
from landings.excel import save_excel

from utils.date import split_periods, month_range, check_dates

date_fmt = 'yyyy-MM-dd'

class AflafrettirSignal(QObject):
  """ :class AflafrettirSignal: is a custom signalling class
  """
  work_done = Signal(bool)

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

    self.queue = Queue()
    self.cred = CredentialsDialog(self)
    
    self.working = False
    self.dates = {'date_from': None, 'date_to':None}
    self.username = ''
    self.password = ''
    self.fname = ''

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
    self.button.clicked.connect(self.set_landing_info)

    self.pbar = QProgressBar(self)

    exit_action = QAction('Exit', self)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Exit Application')
    exit_action.triggered.connect(self.close)

    credential_action = QAction(u'Notenda upplýsingar', self)
    credential_action.setStatusTip(u'Slá inn notendanafn og lykilorð')
    credential_action.triggered.connect(self.enter_credentials)

    self.timer = QTimer(self)
    self.timer.timeout.connect(self.act)
    self.timer.start(1000)

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

  def act(self):
    """ Called when a :class QTimer: times out. This function checks if a
    previous thread has finished fetching data, and if there are other threads
    left to start. If not it will calculate the landing lists and write the on
    an excel format.

    :param self: An instance attribute of the :class AflafrettirGUI:
    """
    if not self.working and self.dates['date_from']:
      #time.sleep(2)
      self.start_thread()
      
    if (not self.working and self.dates['date_from'] != None and 
        not self.dates['date_from']):
      self.dates = {'date_from':None, 'date_to':None}
      landing_list = list()
    
      self.info.append(u'Búið að sækja allar upplýsingar. Reikna út lista')
      
      while not self.queue.empty():
        landing_list.append(self.queue.get())
  
      landing_dict = sort_landings(landing_list)
      save_excel(self.fname, landing_dict)

      self.info.append(u'Hef lokið útreikningum. Listinn er vistaður í: ' +
          unicode(self.fname))

 
  def enter_credentials(self):
    """ Starts the Credentials Dialog
    
    :param self: An instance attribute of the :class AflafrettirGUI:
    """
    self.cred.show()

  def start_thread(self):
    """ Set's the manager, and starts a thread to fetch data from the SOAP
    service of the Icelandic Directorate of Fisheries.
    
    :param self: An instance attribute of the :class AflafrettirGUI:
    """
    manager = LandingsManager()
    manager.set_credentials(self.username, self.password)
    manager.get_client()
    
    date_from = self.dates['date_from'].pop()
    date_to = self.dates['date_to'].pop()
    
    self.info.append(u'Sæki upplýsingar fyrir tímabilið: ' +
                     str(date_from) + u' - ' + str(date_to))
    
    worker = Worker(self.queue, manager, date_from, date_to)
    worker.signal.work_done.connect(self.worker_done)
    worker.start()
    
    self.working = True

  def set_landing_info(self):
    """ Once the button is started, this function is called to set up some lists
    and variables to be able to calculate the landing lists.

    :param self: An instance attribute of the :class AflafrettirGUI:
    """
    if self.password and self.username:
      self.info.clear()
      self.fname, _ = QFileDialog.getSaveFileName(self, 'Vista skrá', '~/')
      date_from = self.cal1.date().toString(date_fmt)
      date_to = self.cal2.date().toString(date_fmt)

      if check_dates(date_from, date_to):
        self.dates = split_periods(date_from, date_to)


  def worker_done(self):
    """ Called when a :class Worker: is done fetching data.
    
    :param self: An instance attribute of the :class AflafrettirGUI:
    """
    self.working = False

class CredentialsDialog(QDialog):
  """ A dialog for entering username and password.
  """
  def __init__(self, parent):
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

  def keyPressEvent(self, event):
    """ Overloads the keyPressEvent, calling push_ok() when enter was pressed

    :param self:  An instance attribute of the :class CredentialsDialog:
    :param event: A key press event
    """
    if event.key() == Qt.Key_Return:
      self.push_ok()

  def push_ok(self):
    """ Gets the text that are written in the 2 :class QLineEdit: objects and if
    there is any, it passes the username and password up to the parent of :class
    CredentialsDialog: and finally closes the dialog.
    
    :param self:  An instance attribute of the :class CredentialsDialog:
   """
    user = self.username.text()
    passw = self.password.text()

    if user and passw:
      self.parent.password = passw
      self.parent.username = user

    self.close()

class Worker(Thread):
  """ :class Worker: inherits from the :class Thread:. It handles interaction
  with the SOAP service of the Icelandic Directorate of Fisheries.
  """
  signal = AflafrettirSignal()
  
  def __init__(self, queue, manager, date_from, date_to):
    """ Initializes the :class Worker: which inherits from :class Process:

    :param self:      An instance attribute of the :class Worker:
    :param queue:     A :class Queue: to put results into.
    :param manager:   A :class LandingManager: that fetches the landings
    :param date_from: A date which forms the date range to fetch data from the
                      SOAP service of the Icelandic Directorate of Fisheries.
    :param date_to:   The other date to form the date range to call the SOAP
                      service provided by the Icelandic Directorate of Fisheries.
    """
    super(Worker, self).__init__()
    self.queue = queue
    self.manager = manager
    self.date_from = date_from
    self.date_to = date_to
    self.daemon = True

  def run(self):
    """ Here is the work of the :class Worker: is performed. Started by calling
    Thread.start() method.
    """
    landings = self.manager.get_landings(self.date_from, self.date_to)

    for l in landings:
      tmp = Landings()
      tmp.set_variable(l)
      tmp.calc_total_catch()
      self.queue.put(tmp)
    
    self.signal.work_done.emit(True)

def main():
  app = QApplication(sys.argv)
  gui = AflafrettirGUI()
  sys.exit(app.exec_())
