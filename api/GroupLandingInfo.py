#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# File: GroupLandingInfo.py
# Author: Finnur Smári Torfason
# Date: 11.12.2012
# About:
#   Class for gathering landing information from the web page of the Directorate
#   of Fisheries in Iceland.
#   The SortLandingInfo class takes as a parameter a list of dictionaries containing
#   the info for the landings. Then it group the list into gear and adds the
#   catch up by ShipID's so that all is left a single entry for each ShipID,
#   containing the total catch for that Ship.

from QueryLandingURL import QueryLandingURL
from ParseHTML import ParseHTML

class GroupLandingInfo(object):
  
  def __init__(self, info):
    self.info = info
    self.gears = [u'HUMA', u'LODN', u'YMIS', u'BOTN', u'NET', u'\xdeGIL',
        u'KRAB', u'HAND', u'SNET', u'HORP', u'DRAG', u'SILD', u'SJOS', u'RAEK',
        u'GRSL', u'FLOT', u'LOFL', u'LINA', u'SIFL']

  def _sort_by_gear(self, gears):
    gear_dict = {}
    for g in gears:
      gear_dict.update({g:self.add_catch(
        [dictio for dictio in self.info if dictio['Gear'] in [g]])})

    return gear_dict

  def add_catch(self, gear_list):
    unique_ID = {v['ShipID']:v['ShipID'] for v in gear_list}.values()
    tmp_list = []
    for i in unique_ID:
      tmp_list.append(self.add_catch_by_id(
          [dictio for dictio in gear_list if dictio['ShipID'] in [i]]))
    
    return tmp_list

  def add_catch_by_id(self, id_list):
    totalCatch = 0
    for i in id_list:
      totalCatch = totalCatch + i['Catch']
      tmp_dict = {'Gear':i['Gear'], 'ShipID':i['ShipID'], 'Name':i['Name'], 'Catch':totalCatch}

    return tmp_dict
    
  def __iter__(self):
      result = self._sort_by_gear(self.gears)
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

  lists = GroupLandingInfo(landingList)
  for i in lists:
    print i
