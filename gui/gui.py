#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
GUI
"""

import sys, Queue

from PySide.QtGui import (QApplication, QMainWindow, QWidget, QAction,
                          QTextEdit, QVBoxLayout, QHBoxLayout, QCalendarWidget,
                          QPushButton)

from crawlermanager.manager import WebCrawler

class AflafrettirGUI(QMainWindow):
  def __init__(self):
    super(AflafrettirGUI, self).__init__()

    base_url = 'http://www.fiskistofa.is/veidar/aflaupplysingar/'
    self.h_url = base_url + 'landanir-eftir-hofnum/landanir.jsp'
    self.s_url = base_url + 'afliallartegundir/aflastodulisti_okvb.jsp'

    self.h_queue_in = Queue.Queue()
    self.h_queue_out = Queue.Queue()
    
    self.s_queue_in = Queue.Queue()
    self.s_queue_out = Queue.Queue()

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
    (date1, date2) = self.get_dates()

    h_params = (
        self.h_url, 
        self.h_queue_in,
        self.h_queue_out,
        'hofn',
        {'dagurFra':date1, 'dagurTil':date2, 'magn':'Sundurlidun'},)
    s_params = (
        self.s_url, 
        self.s_queue_in,
        self.s_queue_out,
        'p_fteg',
        {'p_fra':date1, 'p_til':date2},
        False,)

    h_thread = WebCrawler(*h_params)
    s_thread = WebCrawler(*s_params)
    h_thread.start()
    s_thread.start()

  def get_dates(self):
    fmt = 'dd.MM.yyyy'
    date1 = self.cal1.selectedDate().toString(fmt)
    date2 = self.cal2.selectedDate().toString(fmt)

    if date1 > date2:
      (date1, date2) = (date2, date1)

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
