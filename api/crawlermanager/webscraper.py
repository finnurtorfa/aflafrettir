#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

class DOFWebScraper(object):
  
  def __init__(self, html, name, harbour=True):
    self.html = html
    self.harbour = harbour
    self.name = name

    self.table = self.get_table()

    if self.table is None:
      print "None", self.name
    else:
      print "Not NONE", self.name

    #self.unique = {i['ShipID']:i['ShipID'] for i in self.harbour_list}.values()
    self.ratio= {u'Þorskur':0.84,u'Ýsa':0.84, u'Ufsi':0.8399, u'Blálanga':0.799,
        u'Steinbítur':0.9, u'Hlýri':0.899, u'Grálúða':0.921, u'Skötuselur':0.833,
        u'Langa': 0.797, u'Þykkvalúra':0.921, u'Sólkoli':0.921, u'Sandkoli':0.919,
        u'Lýsa':0.795, u'Tindaskata':0.895, u'Skarkoli':0.919, u'Humar':0.307,
        u'Skata':0.888, u'Stinglax':0.799, u'Keila':0.909, u'Langlúra':0.915,
        u'Hámeri':0.791, u'Lúða':0.923, u'Skrápflúra':0.916,
        u'Sandhverfa':0.875, u'Slétthali':0.875, u'Hvítaskata':0.897,
        u'Hvítskata':0.897, u'Stóra':0.9, u'Tindabikkja':0.875, u'Grásleppa':0}

  def get_table(self):
    """ Grabs needed data from html
    """
    tables = BeautifulSoup(self.html).find_all('table')

    for t in tables:
      if 'cellspacing' in t.attrs and 'cellpadding' in t.attrs:
        if self.harbour:
          self.set_harbour()
        elif not self.harbour:
          self.set_species()
        return t

    return None

  def set_harbour(self):
    self.init_row = 1
    self.fields = ['Date', 'ID', 'Name', 'Gear', 'Species', 'Catch by harbour']
    self.index = range(0,6)
    

  def set_species(self):
    self.init_row = 2
    self.fields = ['ID', 'Name', 'Category', 'Catch by species']
    self.index = range(0,4)

#Authorship information
__author__      = 'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__     = 'GPL'
__version__     = '0.1'
__maintainer__  = 'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
