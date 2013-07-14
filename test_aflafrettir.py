#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
test_aflafrettir
~~~~~~~~~~~

Unit tests for Aflafrettir
"""

import unittest, suds

from datetime import datetime
from suds.sax.date import Date

from utils.date import split_periods, month_range, check_dates_are_valid
from datamanager.manager import SoapManager

class AflafrettirTestCase(unittest.TestCase):
  def setUp(self):
    self.manager = SoapManager()
    pass
  
  def tearDown(self):
    pass

  def test_month_diff(self):

    d1 = datetime(2012, 01, 01)
    d2 = datetime(2012, 05, 05)
    d3 = datetime(2013, 02, 02)

    assert month_range(d1, d2) == (1,5)
    assert month_range(d2, d1) == (1,5)
    assert month_range(d1, d3) == (1, 14)
    assert month_range(d3, d1) == (1, 14)
    assert month_range(d2, d3) == (5, 14)
    assert month_range(d3, d2) == (5, 14)

  def test_check_date_is_valid(self):

    try:
      check_dates_are_valid()
    except ValueError:
      pass

    assert (False, 0) == check_dates_are_valid('2012')
    assert (False, 0) == check_dates_are_valid('2012-09')
    assert (True, 0)  == check_dates_are_valid('2012-09-15')
    assert (False, 0) == check_dates_are_valid('2012-15-09')
    assert (False, 1) == check_dates_are_valid('2012-09-15', '2012-15-09')

  def test_period_split(self):
    date1 = '2012-09-15'
    date2 = '2016-03-05'
    p = split_periods(date1, date2)
    assert p['date_from'].pop(0) == '2012-09-15'
    assert p['date_to'].pop(0) == '2012-09-30'
    assert p['date_from'].pop(0) == '2012-10-01'
    assert p['date_to'].pop(0) == '2012-10-31'
    assert p['date_from'].pop() == '2016-03-01'
    assert p['date_to'].pop() == '2016-03-05'

  def test_SoapManager(self):
    try:
      self.manager.get_client()
    except ValueError:
      pass
    else:
        self.fail('No ValueError')

    try:
      self.manager.set_credentials('aflafrettir', 'ananrer8')
      #self.manager.set_credentials('ship', 'test')
      self.manager.get_client()
    except ValueError:
      if self.manager.headers:
        pass
      else:
        self.fail('Headers not set')

    d1 = '2012-01-01'
    d2 = '2012-01-02'

    args = (d1, d2)

    a = self.manager.call_method('getLandings', *args)

    assert isinstance(a, list)
    
    b = self.manager.get_landings('2013-01-01', '2013-01-2')

    assert isinstance(b, list)
    
    try:
      c = self.manager.call_method('getLanding', *args)
    except suds.MethodNotFound:
      pass

if __name__ == '__main__':
  unittest.main()

__author__      = 'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.1'
__maintainer__  = 'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
