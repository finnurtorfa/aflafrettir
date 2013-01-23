#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Class: TotalCatch.py
---------

*  The TotalCatch class is used by the Aflafrettir API, a web scraping API. The
API is used to gather information on landings from the website of Directorate
of Fisheries in Iceland.

*  The TotalCatch class is initialized with a harbour_list, species_list,
h_keys, and s_keys as described by the __init__ docstring. It returns a
dictionary with all the valuable information the two lists contain. It also
calculates the total catch of each unique ShipID in the harbour_list list.

*  Example use of the class, given a harbour_list and a species_list:
        
        # Initialization parameters
        h_keys = ['Name', 'Gear', 'Catch S', 'Harbour']
        s_keys = ['Name', 'Category', 'Catch US', 'Species']
        
        lists = TotalCatch(harbour_list, species_list, h_keys, s_keys)
        for i in lists:
          print i
"""

class TotalCatch(object):
  
  def __init__(self, harbour_list, species_list, h_keys, s_keys):
    self.harbour_list = harbour_list
    """
    Args:
      self:         The instance attributes of the TotalCatch object
      harbour_list: A list of landings, by harbours
      species_list: A list of catch, by species
      h_keys:       Keys that will be joined together from the harbour_list
      s_keys:       Keys that will be joined together from the species_list
    Returns:
      None
    """
    self.species_list = species_list
    self.h_keys = h_keys
    self.s_keys = s_keys
    self.unique = {i['ShipID']:i['ShipID'] for i in self.harbour_list}.values()
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

  def _calc_total_catch(self, h_list, s_list, h_keys, s_keys):
    """
    Args:
      self:   The instance attributes of the TotalCatch object
      h_list: A list of landings by harbour, by ShipID
      s_list: A list of catch by species, by ShipID
      h_keys: Keys that will be joined together from the harbour_list
      s_keys: Keys that will be joined together from the species_list
    Returns:
      result: A dictionary containing all valuable information from the
              harbour_list and species_list.
    """
    result = {}
    h_list = self.calc_slaughtered(h_list)
    s_list = self.calc_pelagic(s_list)

    if not h_list:
      return None

    for k in h_keys:
      result[k] = self.cat_unique_values(h_list, k)

    for k in s_keys:
      result[k] = self.cat_unique_values(s_list, k)

    total_us = [i['Catch US'] for i in s_list]
    total_s = [i['Catch S'] for i in h_list]

    result['Total US'] =  round(float(sum(total_us)), 3)
    result['Total S'] =  round(float(sum(total_s)), 3)
    result['Most S'] =  round(float(max(total_s)), 3)
    result['Number'] = len({i['Date']:i['Date'] for i in h_list}.values())
    
    return result

  def calc_slaughtered(self, h_list):
    """
    Args:
      self:   The instance attributes of the TotalCatch object
      h_list: A list of landings in harbours itemized by species
    Returns:
      h_list: The same list, except if the item is spawn of liver, it is left
              out. If the item was slaughtered, the catch was updated by
              multiplying it with the appropriate ratio in self.ratio
    """
    import re
    
    for index, landing in reversed(list(enumerate(h_list))):
      if u'ósl' in landing['Stuff'].lower():
        continue
      elif u'lifur' in landing['Stuff'].lower() or  u'hrogn' in landing['Stuff'].lower():
        del h_list[index]
      elif u'slæ' in landing['Stuff'].lower() or u'sl.' in landing['Stuff'].lower():
        tmp = re.split('\\/|\\-|\\ ', landing['Stuff'].title())
        if tmp[0] in self.ratio:
          h_list[index]['Catch S'] = round(landing['Catch S']/self.ratio[tmp[0]], 3)

    return h_list
   
  def calc_pelagic(self, s_list):
    """
    Args:
      self:   The instance attributes of the TotalCatch object
      s_list: A list of catch by species. 
    Returns:
      s_list: If the species is a pelagic species, then the catch is multiplied
              by 1000 to represent it in tonnes.
    """
    for index, species in enumerate(s_list):
      if species['Species'] in self.pelagic:
        s_list[index]['Catch US'] *= 1000

    return s_list

  def cat_unique_values(self, dict_list, key):
    """
    Args:
      self:      The instance attributes of the TotalCatch object
      dict_list: A list of dictionaries
      key:       A key from the dictionary
    Returns:
      A concatenated string of each unique key:value pair of the dict_list
    """
    unique = {i[key]:i[key] for i in dict_list}.values()
    return ', '.join(['%s' % u for u in unique])


  def __iter__(self):
    """
    Args:
      self:   The instance attributes of the TotalCatch object
    Yields:
      result: A dictionary of information available from harbour_list and
              species_list.
    """
    result = {}
    for uid in self.unique:
      result = self._calc_total_catch(
          [dictio for dictio in self.harbour_list if dictio['ShipID'] in [uid]],
          [dictio for dictio in self.species_list if dictio['ShipID'] in [uid]],
          self.h_keys,
          self.s_keys)
      if result is not None:
        yield result
      
if __name__ == '__main__': # If run on it's own
  from QueryURL import QueryURL
  from ParseHTML import ParseHTML
  
  url = {
      'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=1&dagurTil=11.12.2012&magn=Sundurlidun',
      'url1':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=149&dagurTil=11.12.2012&magn=Sundurlidun',
      }
      
  url2 = {
      u'Síld 30':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?p_fteg=Þorskur+1&p_fra=01.12.2012&p_til=11.12.2012',
      u'Loðna 31':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?p_fteg=Ufsi+3&p_fra=01.12.2012&p_til=11.12.2012'
      }

  harbour_list = []
  species_list = []
  html = QueryURL(url)
  html2 = QueryURL(url2)
  h_keys = ['Date', 'Name', 'Gear', 'Catch S', 'Harbour']
  s_keys = ['Name', 'Category', 'Catch US', 'Species']

  for i in html:
    table = ParseHTML(i, [2, 1], ['Date', 'ShipID', 'Name', 'Gear', 'Stuff', 'Catch S'],
        range(0,6), 'Harbour')
    for j in table:
      harbour_list.append(j)
      #print j
  
  for i in html2:
    table = ParseHTML(i, [1, 2], ['ShipID', 'Name', 'Category', 'Catch US'],
        range(0,4), 'Species')
    for j in table:
      species_list.append(j)
  
  lists = TotalCatch(harbour_list, species_list, h_keys, s_keys)
  for i in lists:
    print i

#Authorship information
__author__ = 'Finnur Smári Torfason'
__copyright__ = 'Copyright 2012, www.aflafrettir.com'
__credits__ = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Finnur Smári Torfason'
__email__ = 'finnurtorfa@gmail.com'
__status__ = 'Development'
