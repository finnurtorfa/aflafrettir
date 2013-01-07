#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Class: GroupLandingInfo
---------

*  The GroupLandingInfo class is used by the Aflafrettir API, a web scraping API. The
API is used to gather information on landings from the website of Directorate
of Fisheries in Iceland.

*  The GroupLandingInfo class is initialized with a landing_list as described by the
the __init__ docstring. It returns a dictionary of groups of landings. If a ship
appears in two or more lists, all of it's landings are placed in a common
landing list for further processing later on.

*  Example use of the class, given a list of landings from the GroupLandingInfo class:
        
        groups = GroupLandingInfo(landingList)
        groupList = {}
        for g in groups:
          groupList.update(g)
"""

from itertools import groupby
from operator import itemgetter

class GroupLandingInfo(object):

  def __init__(self, landing_list):
    """
    Args:
      self:         The instance attributes of the GroupLandingInfo object
      landing_list: A list of dictionaries containing the info on landings
    Return:
      None
   """
    self.landing_list = landing_list
    self.gears = [u'LODN', u'SILD', u'FLOT', u'LOFL', u'SIFL', u'NET', u'SNET',
        u'GRSL', u'HUMA', u'LINA', u'RAEK', 'BOTN', 'DRAG', u'HAND', 'YMIS',
        u'\xdeGIL', u'KRAB', u'HORP', u'SJOS', u'IGPL', u'RMNT', u'KRAL']
    self.groups = {'Uppsjávarskip':[u'LODN', u'SILD', u'FLOT', u'LOFL', u'SIFL'],
        'Net':[u'NET', u'SNET', u'GRSL', ], 'Humar':[u'HUMA'], 'Lína':[u'LINA'],
        'Rækja':[u'RAEK'], 'Botnvörpungar':[u'BOTN'], 'Dragnót':[u'DRAG'],
        'Handfæri':[u'HAND'], 'Ýmislegt':[u'YMIS', u'\xdeGIL', u'KRAB', u'HORP',
          u'SJOS', u'IGPL', u'RMNT', u'KRAL']}
    self.common_id = []
    self.common_landings = []
    self.group_landings = {} 

  def get_groups(self):
    """
    Args:
      self: The instance attributes of the GroupLandingInfo object
    Return:
      None
    """
    self.group_landings = self.group_by_gear(self.gears, self.landing_list, self.groups)
    self.common_id = self.get_unique_id_by_group(self.groups, self.group_landings)
    self.common_landings, self.group_landings = self.get_common_landings(self.group_landings, self.common_id)
    self.group_landings['Common'] = self.common_landings

  def group_by_gear(self, gears, landing_list, groups):
    """
    Args:
      self:           The instance attributes of the GroupLandingInfo object
      gears:          A list of gears available
      landing_list:   A list of dictionaries containing the info on landings
      groups:         The list of gears grouped together
    Return:
      group_landings: The landing_list object split into groups.
    """
    group_landings = {}
    for g in groups: group_landings[g] = []

    list_sorted = sorted(landing_list, key=lambda d:(d['Gear'], d['ShipID']))

    for gear, landing in groupby(list_sorted, key=itemgetter('Gear')):
      for l in landing:
        for g in groups:
          if gear in groups[g]:
            l['Group'] = g
            group_landings[g].append(l)
       
    return group_landings
  
  def get_unique_id_by_group(self, groups, group_landings):
    """
    Args: 
      self:           The instance attributes of the GroupLandingInfo object
      groups:         The list of gears grouped together
      group_landings: The landing_list object split into groups.
    Return:
      common_id:      A list of id's that appear in more than one group of
                      landings
    """
    common_id = []
    unique_id = {}
    for g in groups: unique_id[g] = []

    for g in group_landings:
      unique_id[g].extend(
          {i['ShipID']:i['ShipID'] for i in group_landings[g]}.values())

    for u_idx, u in enumerate(unique_id):
      for uu_idx, uu in enumerate(unique_id):
        if uu_idx > u_idx:
          for uid in unique_id[u]:
            if uid in unique_id[uu]:
              common_id.append(uid)

    return common_id

  def get_common_landings(self, group_landings, common_id):
    """
    Args:
      self:            The instance attributes of the GroupLandingInfo object
      group_landings:  The landing_list object split into groups.
      common_id:       A list of id's that appear in more than one group of
                       landings
    Return:
      common_landings: A list of all the landings by the id's in common_id
      group_landings:  The landing_list object split into groups. The
                       common_landings have been removed from the list.
    """
    common_landings = []
    for cid in common_id:
      for g in group_landings:
        common_landings.extend(
            [x for x in self.group_landings[g] if (cid == x.get('ShipID'))])
        group_landings[g] = [x for x in self.group_landings[g] if not (cid == x.get('ShipID'))]

    return (common_landings, group_landings)

  def __iter__(self):
    """
    Args:
      self:  The instance attributes of the GroupLandingInfo object
    Yield:
             A dictionary containing the landings, grouped together
    """
    self.get_groups()
    for s in self.group_landings:
      yield {s:self.group_landings[s]}
      

###################################################
# Main body
###################################################
if __name__ == '__main__': # If run on it's own
  from QueryURL import QueryURL
  from ParseHTML import ParseHTML
  from TotalCatch import TotalCatch
  
  url = {
      'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=1&dagurTil=11.12.2012&magn=Samantekt',
      'url1':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=149&dagurTil=11.12.2012&magn=Samantekt',
      }
  
  url2 = {
      'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?p_fteg=Þorskur+1&p_fra=01.12.2012&p_til=11.12.2012',
      'url1':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?p_fteg=Ufsi+3&p_fra=01.12.2012&p_til=11.12.2012'
      }

  harbour_list = []
  species_list = []
  html = QueryURL(url)
  html2 = QueryURL(url2)
  h_keys = ['Name', 'Gear', 'Catch S', 'Harbour']
  s_keys = ['Name', 'Category', 'Catch US', 'Species']

  for i in html:
    table = ParseHTML(i, [2, 1], ['Date', 'ShipID', 'Name', 'Gear', 'Catch S'],
        range(0,5), 'Harbour')
    for j in table:
      harbour_list.append(j)
      #print j
  
  for i in html2:
    table = ParseHTML(i, [1, 2], ['ShipID', 'Name', 'Category', 'Catch US'],
        range(0,4), 'Species')
    for j in table:
      species_list.append(j)
  
  groups = GroupLandingInfo(harbour_list)
  groupList = {}
  for g in groups:
    groupList.update(g)
   
  for g in groupList:
    #print groupList[g]
    lists = TotalCatch(groupList[g], species_list, h_keys, s_keys)
    landingList = []
    for l in lists:
      landingList.append(l)
    groupList[g] = landingList

  #print groupList

#Authorship information
__author__ = 'Finnur Smári Torfason'
__copyright__ = 'Copyright 2012, www.aflafrettir.com'
__credits__ = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Finnur Smári Torfason'
__email__ = 'finnurtorfa@gmail.com'
__status__ = 'Development'
