#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# File: ParseHTML.py
# Author: Finnur Smári Torfason
# Date: 11.12.2012
# About:
#   Class for gathering landing information from the web page of the Directorate
#   of Fisheries in Iceland.
#   The ParseHTML class takes in a HTML content of the website and pulls the
#   necessary data to form a list

import logging
from BeautifulSoup import BeautifulSoup
from QueryURL import QueryURL

###################################################
# Class: ParseHTML
###################################################
class ParseHTML(object):

  def __init__(self, html_dict, key):
    self.harbour = html_dict[key]
    self.html = html_dict['content']
    self.fieldType = ['ShipID', 'Name', 'Gear', 'Catch']
    self.row = dict()
    
  def _get_landing_info(self):
    result = []
    landingHTML = BeautifulSoup(self.html)
    try:
      landingTable = landingHTML.findAll('table')[2]
    except(IndexError):
      logging.exception('There appears to be no landing information on this page, continue')
      return {'error':1}

    for tr in landingTable.findAll('tr')[1:]:
      for i in range(1,5):
        for td in tr.findAll('td')[i]:
          if i is 1:
            self.row.update({self.fieldType[i-1]:int(td)})
          elif i is 4:
            td = td.replace('.','')
            self.row.update({self.fieldType[i-1]:int(td)})
          else:
            self.row.update({self.fieldType[i-1]:td})
      self.row['Harbour'] = self.harbour
      result.append(self.row)
      self.row = dict()
    
    return result

  def get_list(self, species=False):
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
    for info in self._get_landing_info():
      if 'error' not in info:
        yield info

if __name__ == '__main__': # If run on it's own
  
#      'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=1&dagurTil=11.12.2012&magn=Samantekt',
#      }
#  landingList = []
#  html = QueryLandingURL(url)
#
#  for i in html:
#    #print i
#    table = ParseHTML(i)
#    for j in table:
#      landingList.append(j)
#
#  print landingList

  url = {'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp'}
  url2 = {'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp'}

  html = QueryLandingURL(url)
  html2 = QueryLandingURL(url2)
  for i in html:
    ParseHTML(i).get_fish_list()
  for i in html2:
    ParseHTML(i).get_fish_list(True)
