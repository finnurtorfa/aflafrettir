#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Class: ParseHTML.py
---------

*  The ParseHTML class is used by the Aflafrettir API, a web scraping API. The
API is used to gather information on landings from the website of Directorate
of Fisheries in Iceland.

*  The ParseHTML class is initialized with a html_dict, tbl_row_no,
fields, field_range, as described by
the __init__ docstring. It returns a dictionary with all the values of the html
page that was given as a input.

*  Example use of the class:
        
        # Initialization parameters
        url = {'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?p_fteg=Ýsa+2&p_fra=01.12.2012&p_til=22.12.2012'}
          
          html = QueryURL(url)
          for h in html:
            info = ParseHTML(h, [1, 2], ['ShipID', 'Name', 'Gear', 'Catch'], range(0,4))
            for i in info:
              print i
"""

import logging
from BeautifulSoup import BeautifulSoup
from QueryURL import QueryURL

class ParseHTML(object):

  def __init__(self, html_dict, tbl_row_no, fields, field_range):
    """
    Args:
      self:         The instance attributes of the ParseHTML object
      html_dict:    A Dictionary containing the html code and other necessary info
      tbl_row_no:   A list with the table number and row number where the data is
                  contained.
      fields:       Name of the fields of interest
      field_range:  Range over which the fields of interest are located.
    Returns:
      None
    """
    self.name = html_dict['name']
    self.html = html_dict['content']
    self.tbl_row_no = tbl_row_no
    self.fields = fields 
    self.field_range = field_range
    
  def _get_landing_info(self):
    """
    Args:
      self:   The instance attributes of the ParseHTML object
    Returns:
      result: A dictionary with the fields of interest as keys, and the
               corresponding value
    """
    result = []
    row = {}
    html = BeautifulSoup(self.html)
    
    try:
      table = html.findAll('table')[self.tbl_row_no[0]]
    except(IndexError):
      logging.exception('There appears to be no info of interest on this page, continue')
      return {'error':1}

    for tr in table.findAll('tr')[self.tbl_row_no[1]:]:
      for index, i in enumerate(self.field_range):
        #print index, i
        td = tr.findAll('td')[i].string
#        if val is None:
#          print "Hello None"
#        for td in tr.findAll('td')[i]:
          #print index, td
        if index == 0:
          if td is not None:
            first = td
          row.update({self.fields[index]:first.strip()})
        elif index == len(self.fields)-1:
          td = td.replace('.', '')
          row.update({self.fields[index]:int(td)})
        else:
          row.update({self.fields[index]:td.strip()})
      #Wrow.update({':first})
      row['name-key'] = self.name
      result.append(row)
      row = {}
    
    return result

  def get_list(self, species=False):
    """
    Args:
      self:    The instance attributes of the ParseHTML object
      species: A boolean expression that determines wether the returned object
               should be harbours or species.
    Returns:
      result:  A dictionary of harbours or species and their accompanying values
    """
    result = {}
    html = BeautifulSoup(self.html)
    if species:
      select = html.findAll('select')[0]
    else:
      select = html.findAll('select')[1]
    for o in select.findAll('option'):
      result.update({o.string.encode('utf-8'):o.get('value').encode('utf-8')})
    if not species:
      result.update({'Færeyjar':'167'})
      result.update({'Noregur':'163'})

    return result

  def __iter__(self):
    """
    Args:
      self: The instance attributes of the ParseHTML object
    Yields:
      info: A dictionary with the fields of interest as keys, and the
            corresponding value
    """
    for info in self._get_landing_info():
      if 'error' not in info:
        yield info

if __name__ == '__main__': # If run on it's own
  
  url = {'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=1&dagurTil=11.12.2012&magn=Samantekt'}
  url2 = {'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?p_fteg=Ýsa+2&p_fra=20.12.2012&p_til=25.12.2012'}

  html = QueryURL(url)
  html2 = QueryURL(url2)
  for i in html:
    info = ParseHTML(i, [2, 1], ['Date', 'ShipID', 'Name', 'Gear', 'Catch'], range(0,5))
    for j in info:
      print j

  for i in html2:
    info = ParseHTML(i, [1, 2], ['ShipID', 'Name', 'Category', 'Catch'], range(0,4))
    for j in info:
      print j

#Authorship information
__author__ = 'Finnur Smári Torfason'
__copyright__ = 'Copyright 2012, www.aflafrettir.com'
__credits__ = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Finnur Smári Torfason'
__email__ = 'finnurtorfa@gmail.com'
__status__ = 'Development'
