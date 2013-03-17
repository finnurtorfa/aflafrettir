#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
GUI
"""

import sys, Queue

from PySide.QtGui import (QApplication, QMainWindow, QWidget, QAction,
                          QTextEdit, QVBoxLayout, QHBoxLayout, QCalendarWidget,
                          QPushButton, QProgressBar)

from crawlermanager.manager import WebCrawler

class AflafrettirGUI(QMainWindow):
  def __init__(self):
    super(AflafrettirGUI, self).__init__()

    base_url = 'http://www.fiskistofa.is/veidar/aflaupplysingar/'
    self.h_url = base_url + 'landanir-eftir-hofnum/landanir.jsp'
    self.s_url = base_url + 'afliallartegundir/aflastodulisti_okvb.jsp'

    self.cnt = 0

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

    self.pbar = QProgressBar(self)

    exit_action = QAction('Exit', self)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Exit Application')
    exit_action.triggered.connect(self.exit)

    menubar = self.menuBar()
    filemenu = menubar.addMenu('&File')
    filemenu.addAction(exit_action)
    
    self.statusbar = self.statusBar()

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
    (date1, date2) = self.get_dates()
    self.statusbar.addWidget(self.pbar)
    
    if date1 and date2:
      self.h_thread.set_params({'dagurFra':date1, 'dagurTil':date2, 'magn':'Sundurlidun'})
      self.s_thread.set_params({'p_fra':date1, 'p_til':date2})

      self.pbar.setMaximum(len(self.h_thread.new_params) + len(self.s_thread.new_params))

      self.h_thread.fetchReady.connect(self.get_fetch)
      self.s_thread.fetchReady.connect(self.get_fetch)

      self.h_thread.start()
      self.s_thread.start()
    else:
      self.info.append(u'Villa!Eru dagsetningarnar þær sömu?')

  def get_fetch(self, data):
    self.info.append(u'Sæki gögn vegna ' + data)
    self.cnt += 1
    self.pbar.setValue(self.cnt)

  def get_dates(self):
    fmt = 'dd.MM.yyyy'
    date1 = self.cal1.selectedDate().toString(fmt)
    date2 = self.cal2.selectedDate().toString(fmt)

    if date1 > date2:
      (date1, date2) = (date2, date1)
    elif date1 == date2:
      return (None, None)

    return (date1, date2)

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
