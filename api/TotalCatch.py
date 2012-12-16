#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# File: GroupLandingInfo.py
# Author: Finnur Smári Torfason
# Date: 11.12.2012
# About:
#   Class for gathering landing information from the web page of the Directorate
#   of Fisheries in Iceland.
#   The TotalCatch class takes as a parameter a list of dictionaries containing
#   the info for the landings. Then it calculates the total catch for all the
#   unique ShipID's in the list. 

from QueryLandingURL import QueryLandingURL
from ParseHTML import ParseHTML


###################################################
# class: TotalCatch
###################################################
class TotalCatch(object):
  
  def __init__(self, landingList):
    self.landingList = landingList
    self.unique = {i['ShipID']:i['ShipID'] for i in self.landingList}.values()

  def _calc_total_catch(self, id_list):
    totalCatch = 0
    for i in id_list:
      totalCatch = totalCatch + i['Catch']

    tmp_dict = {'Gear':i['Gear'], 'ShipID':i['ShipID'], 'Name':i['Name'], 'Catch':totalCatch}
    return tmp_dict
    
  def __iter__(self):
    result = []
    for uid in self.unique:
      result = self._calc_total_catch(
          [dictio for dictio in self.landingList if dictio['ShipID'] in [uid]])
      yield result
        
      
###################################################
# Main body
###################################################
if __name__ == '__main__': # If run on it's own
  url = {
      'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=1&dagurTil=11.12.2012&magn=Samantekt',
      'url1':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=149&dagurTil=11.12.2012&magn=Samantekt',
      }
  landingList = []
  html = QueryLandingURL(url)

  for i in html:
    table = ParseHTML(i)
    for j in table:
      landingList.append(j)
      #print j

  lists = TotalCatch(landingList)
  for i in lists:
    print i
