#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
aflafrettir
~~~~~~~~~~~

This module starts the GUI for the Aflafréttir GUI and sets the logging level

"""

import logging, gui.gui

def init_logging(**kwargs):
  """ Initializes the :class: 'logging'. 

  :param filename:  name of the file to log to
  :param formate:   Change the output formate
  :param datefmt:   Change the date format
  :param level:     The logging level
  """
  logging.basicConfig(**kwargs)
  logging.info('Started running %s', __file__)

if __name__ == '__main__':
  log_args = {'filename':'log/aflafrettir.log', 
            'format': '[%(levelname)s: %(asctime)s] \t %(message)s', 
            'datefmt':'%d-%m-%Y %H:%M:%S',
            'level': 'DEBUG'}
  #init_logging(**log_args)
  gui.gui.main()

__author__      = 'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.1'
__maintainer__  = 'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
