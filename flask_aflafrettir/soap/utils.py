"""
  flask.aflafrettir.soap.utils
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  Add some utilities for helping the SOAP manager.
"""

import logging

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

fmt = '%Y-%m-%d'

def check_dates(*args):
  """ Returns the first occurrence of an invalid date from a list of input
  dates and True if all dates are valid

  :param *args: list of 0 or more dates
  """
  if not args:
    raise ValueError('At least 1 date is needed')

  for (i, date) in enumerate(args):
    try:
      d = datetime.strptime(date, fmt)
    except ValueError:
      return False, i

  return True, 0

def split_periods(date_from, date_to):
  """ Returns a :dict: object with lists of dates to and from, representing the
  input period from month to month.

  :param date_from: Starting date of the input period
  :param date_to:   End date of the input period
  """
  p = {'date_from': [], 'date_to': []}

  logging.info('Date from: %s', date_from)
  logging.info('Date to: %s', date_to)
  
  if type(date_from) is not datetime:
    logging.info('Change date_from string to a datetime object')
    date_from = datetime.strptime(date_from, '%Y-%m-%d')

  if type(date_to) is not datetime:
    logging.info('Change date_to string to a datetime object')
    date_to = datetime.strptime(date_to, '%Y-%m-%d')

  start_month, end_month = month_range(date_from, date_to)
  new_year = 0

  if date_from.year == date_to.year and date_from.month == date_to.month:
    p['date_from'].append(date_from.strftime(fmt))
    p['date_to'].append(date_to.strftime(fmt))
    return p

  for m in range(start_month, end_month+1):
    if (m+new_year)%13 == 0: # End of year condition
      date_from += relativedelta(year=date_from.year+1, day=1, month=1)
      p['date_from'].append(date_from.strftime(fmt))
      date_from += relativedelta(day=31)
      p['date_to'].append(date_from.strftime(fmt))
      new_year += 1
    elif m == start_month: # start condition
      p['date_from'].append(date_from.strftime(fmt))
      date_from += relativedelta(day=31)
      p['date_to'].append(date_from.strftime(fmt))
    elif m == end_month: # End condition
      date_from += relativedelta(day=1, month=(m+new_year)%13)
      p['date_from'].append(date_from.strftime(fmt))
      p['date_to'].append(date_to.strftime(fmt))
    else:
      date_from += relativedelta(day=1, month=(m+new_year)%13)
      p['date_from'].append(date_from.strftime(fmt))
      date_from += relativedelta(day=31)
      p['date_to'].append(date_from.strftime(fmt))

  return p


def month_range(d1, d2):
  """ Returns the starting month, and end month of the dates given. The end
  month is calculated as
    (Difference in years)*12 + end_month - starting_month

  :param d1: The first date
  :param d2: The second date
  """
  if d1 > d2:
    (d1, d2) = (d2, d1)

  diff = (d2.year - d1.year)*12 + d2.month - d1.month

  return d1.month, d1.month + diff

__author__      = u'Finnur Smári Torfason'
__copyright__   = 'Copyright 2015, www.aflafrettir.com'
__credits__     = [u'Finnur Smári Torfason', u'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.2'
__maintainer__  = u'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
