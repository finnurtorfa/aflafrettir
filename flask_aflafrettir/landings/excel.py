#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
excel.py
~~~~~~~~~~~

Contains functions for sorting and writing information contained in :class
Landings: to an excel file.
"""

import xlwt

style0 = xlwt.easyxf('font: name Arial, color-index black',
    num_format_str='#,##0')
style1 = xlwt.easyxf('font: name Arial, color-index black, bold on',
    num_format_str='#,##0')
item = [u'Skipaskrárnúmer', u'Nafn', u'Fjöldi', u'Heildarafli', u'Mesti afli',
    u'Höfn', u'Veiðarfæri', u'Tegundir', u'Afli e. tegundum']
keys = [u'shipNumber', u'shipName', u'count', u'totalCatch', u'maxCatch',
    u'landingHarbour', u'equipment', u'landingCatch']

def save_excel(name, landing_dict):
  """ Sets up a :class xlwt.Workbook: and saves data in an excel file.

  :param name:          A string representing the name of the excel file.
  :param landing_dict:  A dictionary of landings to be written to excel file.
  """
  wbk = xlwt.Workbook('utf-8')

  for k,v in landing_dict.iteritems():
    v.sort(reverse=True)
    write_data(wbk, k, v)
    
  wbk.save(name)

def write_data(wbk, sheet_name, data_sorted):
  """ Writes data to a :class xlwt.Workbook: object.

  :param wbk:         A :class xlwt.Workbook: that will receive data
  :param sheet_name:  Name of the sheet to be added to the workbook. The sheet
                      name represents the group of landings in data_sorted.
  :param data_sorted: A list of :class Landings: sorted in reverse order by
                      totalCatch
  """
  sheet = wbk.add_sheet(sheet_name)

  for i, v in enumerate(item):
    sheet.write(0, i, v, style1)

  for i, v in enumerate(data_sorted):
    for j, k in enumerate(keys):
      tmp = getattr(v, k)

      if k == 'landingHarbour' or k == 'equipment':
        if type(tmp) is list:
          tmp = ', '.join([unicode(x) for x in tmp])
      
      if k == 'landingCatch':
        tmp_k = ', '.join([unicode(f) for f in tmp.keys()])
        tmp_v = ', '.join([str(v) for v in tmp.values()])
        sheet.write(i+1, j, tmp_k)
        sheet.write(i+1, j+1, tmp_v)
      else:
        sheet.write(i+1, j, tmp)

__author__      = u'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = [u'Finnur Smári Torfason', u'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.1'
__maintainer__  = u'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
