#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
manager
~~~~~~~~~~~
"""

from suds.client import Client
from suds.sax.date import Date

class Landings(object):
  """ :class Landings: contains info about landings such as catch, total catch,
  shipID, name etc.
  """

  def __init__(self):
    """ Initializes the :class Landings:
    """
    self.shipId       = None
    self.name         = None
    self.ship_size    = None
    self.catch        = None
    self.harbour      = None
    self.total_catch  = None
    self.gear         = None
    self.group        = None
    self.date         = None

    #for key,val in kwargs.iteritems():
    #  if key in 
    #  setattr(self, key, val)

class SortingManager(object):
  """ :class SortingManager: contains functions to sort data regarding landings
  from the Icelandic Directorate of Fisheries.
  """
  def __init__(self):
    pass

  def group_by_gears(self, data):
    return False

if __name__ == '__main__':
  manager = SoapManager()

__author__      = 'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.1'
__maintainer__  = 'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
