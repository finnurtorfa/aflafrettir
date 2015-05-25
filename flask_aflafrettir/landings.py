#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
flask.aflafrettir.landings
==========================


"""
from suds.client import Client
from suds.sax.date import Date

class Landings(object):
  """ :class Landings: contains info about landings such as catch, total catch,
  shipID, name etc.
  """
  keys = ['landingDate', 'landingHarbour', 'shipGrossTonnage', 'shipName', 
          'shipNumber']
  groups = {
    u'Uppsjávarskip':[5, 9, 10],
    u'Net':[1, 2, 3, 4],
    u'Humar':[7],
    u'Lína':[12, 13], 
    u'Rækja':[8], 
    u'Botnvörpungar':[6],
    u'Dragnót':[11], 
    u'Handfæri':[14],
    u'Ýmislegt':[15, 16, 17, 18, 19, 20, 21]}
    
  line_groups = {
      u'Smábátar -8BT': [0, 8.0],
      u'Smábátar 8-13BT': [8.0, 13.0],
      u'Smábátar 13-15BT': [13.0, 15.0],
      u'Smábátar +15BT': [15.0, 30.0]}
 

  def __init__(self, equipment_list, species_list):
    """ Initializes the :class Landings:

    :param self:            An instance attribute of the :class Landings:
    :param equipment_list:  A list of available equipments
    :param species_list:    A list of available species
    """
    self.equipment          = None
    self.landingDate        = None
    self.landingHarbour     = None
    self.shipGrossTonnage   = None
    self.shipName           = None
    self.shipNumber         = None

    self.totalCatch         = 0.0
    self.landingCatch       = dict()
    self.maxCatch           = 0.0
    self.groupName          = None
    self.count              = 1
    self.equipment_list     = equipment_list
    self.species_list       = species_list

  def __repr__(self):
    return "Landing: \n\tID: {}\n\tName: {}\n\tTonnage: {}\n\tHarbour: {}\n\t" \
           "Date: {}\n\tTotal Catch: {}\n\tMax Catch: {}\n\t" \
           "Landing Catch: {}\n\tEquipment: {}\n\tGroup: {}\n\tCount: {}" \
        .format(self.shipNumber,
                self.shipName,
                self.shipGrossTonnage,
                self.landingHarbour,
                self.landingDate,
                self.totalCatch,
                self.maxCatch,
                self.landingCatch,
                self.equipment,
                self.groupName,
                self.count)
    
  def insert(self, landing): 
    """ Takes in a single landing, and calculates the total catch, max catch, 
    the group this landing belongs to etc.

    :param self:      An instance attribute of the :class Landings:
    :param landing:   An instance of :class Client: 'getLandings method.
    """
    self.equipment = self.get_equipment_from_id(
        landing.landingCatch[0].equipment)
    
    for k in self.keys:
      try:
        val = getattr(landing, k)
        setattr(self, k, val)
      except AttributeError:
        setattr(self, k, None)

    self.get_group(landing.landingCatch[0].equipment, self.shipGrossTonnage)
    self.calc_total_catch(landing.landingCatch)

  def get_equipment_from_id(self, equipment_id):
    """ Translates a fishing equipments id into a name

    :param self:          An instance attribute of the :class Landings:
    :param equipment_id:  An equipment id
    """
    for e in self.equipment_list:
      if e.id == equipment_id:
        return e.name

    return "Annað"

  def get_species_from_id(self, species_id):
    """ Translates species id into a name 

    :param self:        An instance attribute of the :class Landings:
    :param species_id:  A species id
    """
    for s in self.species_list:
      if s.id == species_id:
        return s.name

    return "Annað"

  def get_group(self, equipment_id, gross_tonnage):
    """ Translates equipment id's and the ships gross tonnage into groups. 

    :param self:            An instance attribute of the :class Landings:
    :param equipment_id:    An equipment id
    :param gross_tonnage:   A ship's gross tonnage
    """
    for g in self.groups:
      if equipment_id in self.groups[g]:
        self.groupName = g
        break

    if self.groupName == "Lína":
      for lg in self.line_groups:
        if ( self.line_groups[lg][0] < gross_tonnage and \
             self.line_groups[lg][1] >= gross_tonnage ):
          self.groupName = lg
  
  def calc_total_catch(self, catch):
    """ Calculates the total catch in a fishing trip and places it in an 
    appropriate group.

    :param self:    An instance attribute of the :class Landings:
    :param catch:   The landing catch from a single fishing trip.
    """
    for c in catch:
      if self.get_species_from_id(c.species) not in self.landingCatch:
        self.landingCatch[self.get_species_from_id(c.species)] = 0.0

      self.landingCatch[self.get_species_from_id(c.species)] += c.totalCatch
      self.totalCatch += c.totalCatch

    self.maxCatch = self.totalCatch

  def __add__(self, add):
    """ Returns the sum of two :class Landings(): given that the landings were
    performed by the same ship. 
    
    :param self:  An instance attribute of the :class Landings:
    :param add:   Another instance attribute of the :class Landings:
    """
    if self.shipNumber != add.shipNumber:
      raise ValueError('Can only perform addition on landings from the same' \
                       ' ship')

    self.totalCatch +=  add.totalCatch

    if self.maxCatch < add.maxCatch:
       self.maxCatch = add.maxCatch
    
    for k in add.landingCatch:
      if k in self.landingCatch:
        self.landingCatch[k] += add.landingCatch[k]
      else:
        self.landingCatch[k] = add.landingCatch[k]

    try:
      self.landingDate.append(add.landingDate)
      self.landingHarbour.append(add.landingHarbour)
      self.equipment.append(add.equipment)
    except AttributeError:
      self.landingDate = [self.landingDate, add.landingDate]
      self.landingHarbour = [self.landingHarbour, add.landingHarbour]
      self.equipment = [self.equipment, add.equipment]
    
    self.count = len(self.landingDate)

    return self

  def __lt__(self, other):
    """ Compares the size of totalCatch of two :class Landings: object and
    returns the result
    
    :param self:  An instance attribute of the :class Landings:
    :param other: Another instance attribute of the :class Landings:
    """
    return self.totalCatch < other.totalCatch

def sort_landings(landings):
  """ Returns a dictionary. The dictionary keys represent the categories of
  which the data is sorted by.

  :param landings: a list of :class Landings:
  """
  groups = dict()
  results = dict()

  for l in landings:
    if l.groupName not in groups:
      groups[l.groupName] = []
      results[l.groupName] = []

    groups[l.groupName].append(l)

  for k in groups:
    unique_id  = list(set([n.shipNumber for n in groups[k]]))
    for i in unique_id:
      tmp = [l for l in groups[k] if l.shipNumber == i]
      tmp = calculate_catch(tmp)
      results[k].append(tmp)


  return results

def calculate_catch(landings):
  """ Takes in a list of :class Landings: with landings by a single ship and
  returns a :class Landings: where the total catch, number of landings etc. has
  been calculated
  
  :param landings: a list of :class Landings:
  """
  tmp = landings.pop()
  for i in landings:
    tmp = tmp + i

  return tmp

if __name__ == '__main__':
  from soap import DOFManager

  manager = DOFManager(credentials={'Username': 'Username', 
                                    'Password': 'Password'})

  landings = manager.get_all_landings('2015-02-01', '2015-02-02')
  equipments = manager.get_fishing_equipment()
  species = manager.get_species()
  lan = []

  for l in landings:
    landing = Landings(equipments, species)
    landing.insert(l)
    lan.append(landing)

  result = sort_landings(lan)
  for k in result:
    print("\n   {}   \n".format(k))
    print(result[k])

__author__      = u'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = [u'Finnur Smári Torfason', u'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.2'
__maintainer__  = u'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
