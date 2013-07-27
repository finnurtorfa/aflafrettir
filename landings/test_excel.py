#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
test_aflafrettir
~~~~~~~~~~~

Unit tests for Aflafrettir
"""

import unittest

class ExcelTestCase(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

  def test_save_excel(self):
    landing_list = list()
    landings = dict()

    for i in range(0,10):
      l = Landings()
      l.totalCatch = 100+i
      l.landingCatch = {'Þorskur': 1234, 'Ýsa': 4321}
      l.landingDate = i
      l.landingHarbour = ['Höfn', 'Höfn', 'Eyjar']
      l.shipGrossTonnage = i
      l.shipName = 'Skinney'
      l.shipNumber = 1234
      l.equipment = ['Net', 'Net', 'Net']
      l.group = 'Net'
      l.count = i+1
      landing_list.append(l)

    landings['Name'] =  landing_list
    landing_list = []
    
    for i in range(0,10):
      l = Landings()
      l.totalCatch = 100+i+10+i
      l.landingCatch = {'Þorskur': 1234, 'Ýsa': 4321}
      l.landingDate = i
      l.landingHarbour = ['Höfn', 'Höfn', 'Eyjar']
      l.shipGrossTonnage = i
      l.shipName = 'Skinney'
      l.shipNumber = 1234
      l.equipment = ['Net', 'Net', 'Net']
      l.group = 'Net'
      l.count = i+1
      landing_list.append(l)

    landings['Name2'] =  landing_list

    save_excel('Name_of_excel_file', landings)

    try:
      with open('Name_of_excel_file'): pass
    except IOError:
      pass

 
if __name__ == '__main__':
  import sys
  sys.path.insert(0,'.')
  
  from landings.landings import Landings
  from landings.excel import save_excel

  unittest.main()
