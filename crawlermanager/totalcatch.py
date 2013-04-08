#!/usr/bin/python
# -*- coding: utf-8 -*-

class TotalCatch(object):
  def __init__(self):
    self.ratio= {u'Þorskur':0.84,u'Ýsa':0.84, u'Ufsi':0.8399, u'Blálanga':0.799,
        u'Steinbítur':0.9, u'Hlýri':0.899, u'Grálúða':0.921, u'Skötuselur':0.833,
        u'Langa': 0.797, u'Þykkvalúra':0.921, u'Sólkoli':0.921, u'Sandkoli':0.919,
        u'Lýsa':0.795, u'Tindaskata':0.895, u'Skarkoli':0.919, u'Humar':0.307,
        u'Skata':0.888, u'Stinglax':0.799, u'Keila':0.909, u'Langlúra':0.915,
        u'Hámeri':0.791, u'Lúða':0.923, u'Skrápflúra':0.916,
        u'Sandhverfa':0.875, u'Slétthali':0.875, u'Hvítaskata':0.897,
        u'Hvítskata':0.897, u'Stóra':0.9, u'Tindabikkja':0.875, u'Grásleppa':0}
    self.pelagic = ['Gulldepla / Norræna Gulld 130', 'Kolmunni 34', 'Loðna 31',
        'Makríll 36', 'Síld 30']

  def calc_harbour(self, queue):
    while not queue.empty():
      queue.get()

  def calc_species(self, queue):
    data = list()
    while not queue.empty():
      data.extend(queue.get())

    data = self._split_by_unique_values('Name', data)

  def _split_by_unique_values(self, key, data):
    from operator import itemgetter
    from itertools import groupby
    output = ()
    for i, g in groupby(sorted(data, key=itemgetter(key)), 
        key = itemgetter(key)):
      output = output + (list(g), )

    return output

__author__      = 'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__     = 'GPL'
__version__     = '0.1'
__maintainer__  = 'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
