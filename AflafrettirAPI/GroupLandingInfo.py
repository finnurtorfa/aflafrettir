#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# File: GroupLandingInfo.py
# Author: Finnur Smári Torfason
# Date: 15.12.2012
# About:
#   Class for gathering landing information from the web page of the Directorate
#   of Fisheries in Iceland.
#   The GroupLandingInfo class takes as a parameter a list of dictionaries containing
#   the info for the landings. Then it group the list into gears.

from QueryURL import QueryURL
from ParseHTML import ParseHTML
from TotalCatch import TotalCatch

class GroupLandingInfo(object):

  def __init__(self, landings):
    self.landings = landings
    self.gears = [u'LODN', u'SILD', u'FLOT', u'LOFL', u'SIFL', u'NET', u'SNET',
        u'GRSL', u'HUMA', u'LINA', u'RAEK', 'BOTN', 'DRAG', u'HAND', 'YMIS',
        u'\xdeGIL', u'KRAB', u'HORP', u'SJOS']
    self.lists = {'Uppsjávarskip':[u'LODN', u'SILD', u'FLOT', u'LOFL', u'SIFL'],
        'Net':[u'NET', u'SNET', u'GRSL', ], 'Humar':[u'HUMA'], 'Lína':[u'LINA'],
        'Rækja':[u'RAEK'], 'Botnvörpungar':[u'BOTN'], 'Dragnót':[u'DRAG'],
        'Handfæri':[u'HAND'], 'Ýmislegt':[u'YMIS', u'\xdeGIL', u'KRAB', u'HORP',
          u'SJOS']}
    self.sorting = {} 
    for l in self.lists: self.sorting[l] = []

  def get_lists(self):
    for g in self.gears:
      gear_dict = {g:[dictio for dictio in self.landings if dictio['Gear'] in g]}
      for l in self.lists:
        if any([(v in self.lists[l] and gear_dict[g]) for v in gear_dict.keys()]):
          self.sorting[l].extend(gear_dict[g])

  def __iter__(self):
    self.get_lists()
    for s in self.sorting:
      yield {s:self.sorting[s]}
      

###################################################
# Main body
###################################################
if __name__ == '__main__': # If run on it's own
  url = {
      'url2':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2011&hofn=149&dagurTil=11.12.2012&magn=Samantekt',
      'url3':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2011&hofn=1&dagurTil=11.12.2012&magn=Samantekt',
      }
  landingList = []
  html = QueryURL(url)

  for i in html:
    table = ParseHTML(i)
    for j in table:
      landingList.append(j)

  groups = GroupLandingInfo(landingList)
  groupList = {}
  for g in groups:
    groupList.update(g)
   
  for g in groupList:
    lists = TotalCatch(groupList[g])
    landingList = []
    for l in lists:
      landingList.append(l)
    groupList[g] = landingList

  print groupList

