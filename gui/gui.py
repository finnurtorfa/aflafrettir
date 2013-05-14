#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, Queue

from PySide.QtGui import (QApplication, QMainWindow, QWidget, QAction,
                          QTextEdit, QVBoxLayout, QHBoxLayout, QDateTimeEdit,
                          QPushButton, QProgressBar, QLabel)
from PySide.QtCore import (QDate)

from crawlermanager.totalcatch import TotalCatch
from crawlermanager.manager import WebCrawler

class AflafrettirGUI(QMainWindow):
  """:class AflafrettirGUI: object which inherits from :class: 'QMainWindow'
  object from PySide and defines the GUI application and how it's properties.
  """
  
  def __init__(self):
    """ Initializes the :class: 'AflafrettirGUI' object.

    :param self: instance attribute of :class: 'AflafrettirGUI' object
    """
    super(AflafrettirGUI, self).__init__()

    base_url = 'http://www.fiskistofa.is/veidar/aflaupplysingar/'
    self.h_url = base_url + 'landanir-eftir-hofnum/landanir.jsp'
    self.s_url = base_url + 'afliallartegundir/aflastodulisti_okvb.jsp'

    self.cnt = 0
    self.sort_cnt = 0

    self.h_queue_in = Queue.Queue()
    self.h_queue_out = Queue.Queue()
    
    self.s_queue_in = Queue.Queue()
    self.s_queue_out = Queue.Queue()
    h_params = (
        self.h_url, 
        self.h_queue_in,
        self.h_queue_out,
        'hofn',)
    s_params = (
        self.s_url, 
        self.s_queue_in,
        self.s_queue_out,
        'p_fteg',
        None,
        False,)

    self.h_thread = WebCrawler(*h_params)
    self.s_thread = WebCrawler(*s_params)
    
    self.h_thread.fetchReady.connect(self.get_fetch)
    self.s_thread.fetchReady.connect(self.get_fetch)
    self.h_thread.fetchDone.connect(self.calc_catch)
    self.s_thread.fetchDone.connect(self.calc_catch)

    self.catch = TotalCatch()
 
    self.initUI()

  def initUI(self):
    """ GUI specific initialization of the :class: 'AflafrettirGUI' object.

    :param self: instance attribute of :class: 'AflafrettirGUI' object
    """
    self.setMaximumWidth(750)
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
    """ Sets the dates in :class: 'WebCrawler' object and starts two threads
    which gather data from the website fo Directorate of Fisheries in Iceland.

    :param self: instance attribute of :class: 'AflafrettirGUI' object
    """
    self.info.clear()
    try:
      (date1, date2) = self.get_dates()

      self.statusbar.addWidget(self.pbar)
      self.pbar.show()
      self.pbar.setMaximum(len(self.h_thread.new_params) + len(self.s_thread.new_params))
      
      self.h_thread.set_params({'dagurFra':date1, 'dagurTil':date2, 'magn':'Sundurlidun'})
      self.s_thread.set_params({'p_fra':date1, 'p_til':date2})

      self.h_thread.start()
      self.s_thread.start()
    except ValueError as e:
      self.info.append(unicode(e))

  def calc_catch(self, done):
    """ Called when a 'WebCrawler' thread has emptied it's queue. Runs the
    sorting algorithm when both of the threads have emptied their queues.

    :param self: Instance attribute of the :class: 'AflafrettirGUI' object
    :param done: A boolean expression stating whether a thread has emptied it's
                 queue
    """
    if done:
      self.sort_cnt += 1

    if self.sort_cnt >= 2:
      self.catch.calc_harbour(self.h_queue_out)
      self.catch.calc_species(self.s_queue_out)
      self.statusbar.removeWidget(self.pbar)
      self.cnt = 0
      self.sort_cnt = 0


  def get_fetch(self, data):
    """ Called when :class: 'WebCrawler' object pops an object from it's input
    queue. 

    :param self: Instance attribute of the :class: 'AflafrettirGUI' object
    :param data: String containing the name of the harbour/species the :class:
                 'WebCrawler' object is fetching data about
    """
    self.info.append(u'Sæki gögn vegna ' + data)
    self.cnt += 1
    self.pbar.setValue(self.cnt)

  def get_dates(self):
    """ Returns the dates selected in :class: 'QDateTimeEdit' objects. It
    returns the dates in ascending order. If the dates are
    equal it raises a ValueError
    
    :param self: Instance attribute of the :class: 'AflafrettirGUI' object
    """
    fmt = 'dd.MM.yyyy'
    date1 = self.cal1.date().toString(fmt)
    date2 = self.cal2.date().toString(fmt)

    if date1 > date2:
      (date1, date2) = (date2, date1)
    elif date1 == date2:
      raise ValueError(u'Sömu Dagsetningar')

    return (date1, date2)

  def closeEvent(self, e):
    """ Closes the application
    
    :param self: Instance attribute of the :class: 'AflafrettirGUI' object
    :param e: A :class: 'QCloseEvent' object.
    """
    e.accept()

def main():
  app = QApplication(sys.argv)
  gui = AflafrettirGUI()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
