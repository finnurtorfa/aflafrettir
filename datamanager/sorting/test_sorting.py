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
    pass
  def tearDown(self):
    pass

  def test_Landings(self):
    test = Landings()
    
    self.manager = SoapManager()
    self.manager.set_credentials('aflafrettir', 'ananrer8')
    self.manager.get_client()

    data = self.manager.get_landings('2013-02-01', '2013-02-02')
    
    assert test.totalCatch == None
    assert test.landingCatch == None
    assert test.landingDate == None
    assert test.landingHarbour == None
    assert test.shipGrossTonnage == None
    assert test.shipName == None
    assert test.shipNumber == None
    assert test.equipment == None
    assert test.group == None
    
    test.set_variable(data.pop())
    
    assert test.totalCatch == None
    assert test.landingCatch != None
    assert test.landingDate != None
    assert test.landingHarbour != None
    assert test.shipGrossTonnage != None
    assert test.shipName != None
    assert test.shipNumber != None
    assert test.equipment == None 
    assert test.group == None 

    test.calc_total_catch()

    assert test.totalCatch != None
    assert test.equipment != None
    assert test.group != None

if __name__ == '__main__':
  import sys
  sys.path.insert(0,'.')
  
  from datamanager.soap.manager import SoapManager
  from manager import Landings

  unittest.main()
