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
      print queue.get()

  def calc_species(self, queue):
    while not queue.empty():
      print queue.get()
