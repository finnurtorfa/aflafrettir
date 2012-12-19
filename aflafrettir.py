#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# File: aflafrettir.py
# Author: Finnur Smári Torfason
# Date: 19/12/2012  
# Abouth:
#   Main program for the aflafrettir program
#
import logging
import gui.gui as gui

def logging_info():
  fn = 'log/aflafrettir.log'
  f = '[%(levelname)s: %(asctime)s] \t%(message)s'
  date = '%d-%m-%Y %H:%M:%S'
  logging.basicConfig(filename=fn, format=f, datefmt=date, level = logging.DEBUG)
  logging.info('Started running %s', __file__)

if __name__ == '__main__':
  logging_info()
  gui.main()
