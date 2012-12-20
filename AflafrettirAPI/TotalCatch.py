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

    id_list[0]['harbour'] = self.get_unique_values(id_list, 'harbour')
    id_list[0]['Gear'] = self.get_unique_values(id_list, 'Gear')
    id_list[0]['Catch'] =  sum(i['Catch'] for i in id_list)
    id_list[0]['Number'] = len(id_list)

    return id_list[0]
  
  def get_unique_values(self, id_list, key):
    unique = {i[key]:i[key] for i in id_list}.values()
    return ', '.join(unique)


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
