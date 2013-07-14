#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
test_date
~~~~~~~~~~~

Unit tests for date manipulation functions
"""
import unittest, suds

from datetime import datetime

from date import split_periods, month_range, check_dates_are_valid


class DateManipulationTestCase(unittest.TestCase):
  def setUp(self):
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

if __name__ == '__main__':
  unittest.main()
