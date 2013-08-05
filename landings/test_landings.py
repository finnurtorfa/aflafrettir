#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
test_aflafrettir
~~~~~~~~~~~

Unit tests for Aflafrettir
"""

import unittest, suds

class LandingsTestCase(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

  def test_Landings(self):
    test = Landings()
    test_list = []
    
    usern = raw_input('Enter username: ')
    passw = raw_input('Enter password: ')

    self.manager = LandingsManager()
    self.manager.set_credentials(usern, passw)
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
    assert test.count == 1
    
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
    assert test.count == 1

    test.calc_total_catch()

    assert test.totalCatch != None
    assert test.equipment != None
    assert test.group != None

    test_list.append(test)

    for landing in data:
      test = Landings()
      test.set_variable(landing)
      test.calc_total_catch()
      test_list.append(test)

    result = sort_landings(test_list)
    assert type(result) == type(dict())

    a = result['Handfæri'][0]
    b = result['Handfæri'][1]
    
    with self.assertRaises(ValueError):
      a+b

if __name__ == '__main__':
  import sys
  sys.path.insert(0,'.')
  
  from landings.manager import LandingsManager
  from landings.landings import Landings, sort_landings

  unittest.main()
