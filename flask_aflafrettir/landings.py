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
    u'Ýmislegt':[15, 16, 17, 18, 19, 20, 21],
    u'Smábátar -8BT': '',
    u'Smábátar 8-13BT': '',
    u'Smábátar 13-15BT': '',
    u'Smábátar +15BT': ''}
 

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
    self.count              = 0
    self.equipment_list     = equipment_list
    self.species_list       = species_list
    
  def insert(self, landing): 
    """ Takes in a single landing, and calculates the total catch, max catch, 
    the group this landing belongs to etc.

    :param self:      An instance attribute of the :class Landings:
    :param landing:   An instance of :class Client: 'getLandings method.
    """
    self.equipment          = self.get_equipment_from_id(
                                landing.landingCatch[0].equipment)
    
    for k in self.keys:
      try:
        val = getattr(landing, k)
        setattr(self, k, val)
      except AttributeError:
        setattr(self, k, None)

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

  def set_variable(self, data):
    """ Checks if attributes from the :class Client: 'getLandings' method
    matching the names of the strings in the 'keys' class variable exist
    and passes them to the :class Landings: instance variables.
    
    :param self:  An instance attribute of the :class Landings:
    :param data:  An instance of :class Client: 'getLandings method.
    """
    for key in keys:
      try:
        val = getattr(data, key)
        setattr(self, key, val)
      except AttributeError:
        setattr(self, key, None)

  def __add__(self, add):
    """ Returns the sum of two :class Landings(): given that the landings were
    performed by the same ship. 
    
    :param self:  An instance attribute of the :class Landings:
    :param add:   Another instance attribute of the :class Landings:
    """
    if self.shipNumber != add.shipNumber:
      raise ValueError('Can only perform addition on landings from the same' 
                        + ' ship')

    self.totalCatch +=  add.totalCatch

    if self.maxCatch < add.maxCatch:
       self.maxCatch = add.maxCatch
    
    for k,v in add.landingCatch.iteritems():
      if k in self.landingCatch:
        self.landingCatch[k] += v
      else:
        self.landingCatch[k] = v

    if type(self.landingDate) == type(list()):
      self.landingDate.append(add.landingDate)
    else:
      self.landingDate = [self.landingDate, add.landingDate]
    
    if type(self.landingHarbour) == type(list()):
      if add.landingHarbour not in self.landingHarbour:
        self.landingHarbour.append(add.landingHarbour)
    else:
      if add.landingHarbour != self.landingHarbour:
        self.landingHarbour = [self.landingHarbour, add.landingHarbour]
      
    if type(self.equipment) == type(list()):
      if add.equipment not in self.equipment:
        self.equipment.append(add.equipment)
    else:
      if add.equipment != self.equipment:
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
  result = dict()
  tmp_dict = dict()
  unique_number = list()

  for k,v in groups.iteritems():
    result[k] = list()
    tmp_dict[k] = [i for i in landings if i.group == k]
    unique_number = list(set([n.shipNumber for n in tmp_dict[k]]))
    
    for i in unique_number:
      tmp = [l for l in landings if l.shipNumber == i and l.group == k]
      tmp = calculate_catch(tmp)
      result[k].append(tmp)

  return result

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

  for l in landings:
    landing = Landings(equipments, species)
    landing.insert(l)
__author__      = u'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = [u'Finnur Smári Torfason', u'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.2'
__maintainer__  = u'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
