#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
manager
~~~~~~~~~~~
"""

import xlwt

style0 = xlwt.easyxf('font: name Arial, color-index black',
    num_format_str='#,##0')
style1 = xlwt.easyxf('font: name Arial, color-index black, bold on',
    num_format_str='#,##0')
item = ['Skipaskrárnúmer', 'Nafn', 'Fjöldi', 'Heildarafli', 'Mesti afli',
    'Höfn', 'Veiðarfæri', 'Tegundir', 'Afli e. tegundum']
keys = ['shipNumber', 'shipName', 'count', 'totalCatch', 'maxCatch',
    'landingHarbour', 'equipment', 'landingCatch']

def save_excel(name, landing_dict):
  wbk = xlwt.Workbook('utf-8')

  for k,v in landing_dict.iteritems():
    v.sort(reverse=True)
    write_data(wbk, k, v)
    
  wbk.save(name)

def write_data(wbk, sheet_name, data_sorted):
  sheet = wbk.add_sheet(sheet_name)

  for i, v in enumerate(item):
    sheet.write(0, i, v, style1)

  for i, v in enumerate(data_sorted):
    for j, k in enumerate(keys):
      tmp = getattr(v, k)

      if k == 'landingHarbour' or k == 'equipment':
        tmp = ', '.join(list(set([str(x) for x in tmp])))
      
      if k == 'landingCatch':
        tmp_k = ', '.join([str(f) for f in tmp.keys()])
        tmp_v = ', '.join([str(v) for v in tmp.values()])
        sheet.write(i+1, j, tmp_k)
        sheet.write(i+1, j+1, tmp_v)
      else:
        sheet.write(i+1, j, tmp)

__author__      = 'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.1'
__maintainer__  = 'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
