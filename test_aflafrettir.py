#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
test_aflafrettir
~~~~~~~~~~~

Unit tests for Aflafrettir
"""

import unittest

from utils.date import split_periods, month_range

class AflafrettirTestCase(unittest.TestCase):
  def setUp(self):
    pass
  
  def tearDown(self):
    pass

  def test_month_diff(self):
    from datetime import datetime

    d1 = datetime(2012, 01, 01)
    d2 = datetime(2012, 05, 05)
    d3 = datetime(2013, 02, 02)

    assert month_range(d1, d2) == (1,5)
    assert month_range(d2, d1) == (1,5)
    assert month_range(d1, d3) == (1, 14)
    assert month_range(d3, d1) == (1, 14)
    assert month_range(d2, d3) == (5, 14)
    assert month_range(d3, d2) == (5, 14)

  def test_period_split(self):
    date1 = '2012-01-15'
    date2 = '2014-03-05'
    p = split_periods(date1, date2)

    assert p['date_from'].pop(0) == '2012-01-15'
    assert p['date_to'].pop(0) == '2012-01-31'
    assert p['date_from'].pop(0) == '2012-02-01'
    assert p['date_to'].pop(0) == '2012-02-29'
    assert p['date_from'].pop() == '2014-03-01'
    assert p['date_to'].pop() == '2014-03-05'

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
