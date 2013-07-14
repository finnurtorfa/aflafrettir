#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
test_aflafrettir
~~~~~~~~~~~

Unit tests for Aflafrettir
"""

import unittest, suds

class SortingManagerTestCase(unittest.TestCase):
  def setUp(self):
    self.manager = SoapManager()
    self.manager.set_credentials('aflafrettir', 'ananrer8')
    #self.manager.get_client()
    #self.data = self.manager.get_landings('2013-01-01', '2013-01-2')

  def tearDown(self):
    pass

  def test_Landings(self):
    test = Landings()

    assert test.shipId == None
    assert test.name == None
    assert test.ship_size == None
    assert test.catch == None
    assert test.harbour == None
    assert test.total_catch == None
    assert test.gear == None
    assert test.group == None
    assert test.date == None

if __name__ == '__main__':
  import sys
  sys.path.insert(0,'.')
  
  from datamanager.soap.manager import SoapManager
  from manager import Landings

  unittest.main()
