#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
test_aflafrettir
~~~~~~~~~~~

Unit tests for Aflafrettir
"""

import unittest, suds

from manager import LandingsManager


class LandingsManagerTestCase(unittest.TestCase):
  def setUp(self):
    self.manager = LandingsManager()
  
  def tearDown(self):
    pass

  def test_LandingsManager(self):
    try:
      self.manager.get_client()
    except ValueError:
      pass
    else:
        self.fail('No ValueError')

    try:
      user = raw_input("Enter username: ")
      passw = raw_input("Enter password: ")
      self.manager.set_credentials(user, passw)
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
