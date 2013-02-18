#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

class DOFWebScraper(object):
  """ :class DOFWebScraper: an object which scrapes data from a HTML site being
  fed to it.
  """
  
  def __init__(self, html, name, harbour=True):
    """ Initializes the :class: 'DOFWebScraper' object

    :param self:    instance attribute of :class: 'DOFWebScraper' object
    :param html:    A HTML website
    :param name:    The name of the harbour or species being processed on the HTML
                    page
    :param harbour: A boolean, which decides whether a harbour or species is
                    being processed
    """
    self.html = html
    self.harbour = harbour
    self.name = name

    self.table = self.get_table()
    
    if self.harbour:
      self.set_harbour()
    elif not self.harbour:
      self.set_species()

  def get_table(self):
    """ Returns a HTML table that contains the data that is looked for, if found

    :param self: instance attribute of :class: 'DOFWebScraper' object
    """
    tables = BeautifulSoup(self.html).find_all('table')

    for t in tables:
      if 'cellspacing' in t.attrs and 'cellpadding' in t.attrs:
        return t

    return None

  def get_data(self, table):
    """ Returns a list of tuples that contain the data necessary. The data it
    contains, depends whether the data is for species or harbours.
    Harbour:
      date:     The date of the landing
      ID:       The ID of the ship that landed
      Name:     Name of the ship
      Gear:     The gear for this fishing trip
      Species:  The species caught
      Catch:    How much was caught in kg.
      Harbour:  The harbour in which was landed
    Species: 
      ID:       The ID of the ship that landed
      Name:     Name of the ship
      Category: The category this ship belongs to
      Catch:    How much was caught in kg.
      Species:  The species which was caught

    :param self: instance attribute of :class: 'DOFWebScraper' object
    :param table: A HTML table with the data
    """
    rows = ()
    data = []

    for row in table.find_all('tr')[self.init_row:]:
      for index, column in enumerate(row.find_all('td')):
        if index == 0:
          if column.string is not None:
            first = column.string.strip()
          rows = rows + ({self.fields[index]:first},)
        elif index == len(self.fields)-1:
          column.string = column.string.replace('.', '')
          rows = rows + ({self.fields[index]:column.string.strip()},)
        else:
          rows = rows + ({self.fields[index]:column.string.strip()},)

      rows = rows + (self.name,)
      data.append(rows)
      rows = ()

    return data

  def set_harbour(self):
    """ Sets the instance variables of :class: 'DOFWebScraper' object, for
    harbours
    
    :param self: instance attribute of :class: 'DOFWebScraper' object
    """
    self.init_row = 1
    self.fields = ['Date', 'ID', 'Name', 'Gear', 'Species', 'Catch by harbour']
    self.index = range(0,6)
    

  def set_species(self):
    """ Sets the instance variables of :class: 'DOFWebScraper' object, for
    species
    
    :param self: instance attribute of :class: 'DOFWebScraper' object
    """
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
