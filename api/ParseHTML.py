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

from BeautifulSoup import BeautifulSoup
from QueryLandingURL import QueryLandingURL

###################################################
# Class: ParseHTML
# About: ParseHTML takes in a html_code and fetches
#        the relevent landing information from it
###################################################
class ParseHTML(object):

  def __init__(self, html_dict):
    self.html = html_dict['content']
    self.fieldType = ['ShipID', 'Name', 'Gear', 'Catch']
    self.row = dict()
    
  def _get_landing_info(self):
    result = []
    landingHTML = BeautifulSoup(self.html)
    landingTable = landingHTML.findAll('table')[2]
    for tr in landingTable.findAll('tr')[1:]:
      for i in range(1,5):
        for td in tr.findAll('td')[i]:
          self.row.update({self.fieldType[i-1]:td})
      result.append(self.row)
      self.row = dict()

    return result

  def __iter__(self):
    for info in self._get_landing_info():
      yield info

if __name__ == '__main__': # If run on it's own
  
  url = {
      'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=1&dagurTil=11.12.2012&magn=Samantekt',
      }
  landingList = []
  html = QueryLandingURL(url)

  for i in html:
    #print i
    table = ParseHTML(i)
    for j in table:
      landingList.append(j)

  print landingList
