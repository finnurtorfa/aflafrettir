#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
manager
~~~~~~~~~~~
"""

from suds.client import Client
from suds.sax.date import Date

keys = ['landingCatch', 'landingDate', 'landingHarbour', 'shipGrossTonnage',
    'shipName', 'shipNumber']
groups = {
  'Uppsjávarskip':[u'Loðnunót', u'Síldarnót', u'Flotvarpa', u'Loðnuflotvarpa',
    u'Síldar-/kolmunnaflotvarpa'], 
  'Net':[u'Net', u'Skötuselsnet', u'Grásleppunet', ], 
  'Humar':[u'Humarvarpa'],
  'Lína':[u'Lína'], 
  'Rækja':[u'Rækjuvarpa'], 
  'Botnvörpungar':[u'Botnvarpa'],
  'Dragnót':[u'Dragnót 135 mm'], 
  'Handfæri':[u'Handfæri'],
  'Ýmislegt':[u'Ýmis veiðarfæri', u'Þorskgildra', u'Krabbagildra',
    u'Hörpudiskplógur/Scallop dr.', u'Sjóstöng', u'Ígulkeraplógur',
    u'RMNT', u'KRAL'],
  'Smábátar -8BT': '',
  'Smábátar 8-13BT': '',
  'Smábátar 13-15BT': '',
  'Smábátar +15BT': ''}
 
class Landings(object):
  """ :class Landings: contains info about landings such as catch, total catch,
  shipID, name etc.
  """

  def __init__(self):
    """ Initializes the :class Landings:

    :param self:  An instance attribute of the :class Landings:
    """
    self.totalCatch       = None
    self.landingCatch     = None
    self.maxCatch         = 0
    self.landingDate      = None
    self.landingHarbour   = None
    self.shipGrossTonnage = None
    self.shipName         = None
    self.shipNumber       = None
    self.equipment        = None
    self.group            = None
    self.count            = 1
    
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

  def calc_total_catch(self):
    """ Calculates the total catch, equipment used and which group the equipment
    belongs to, from a single fishing trip.
    
    :param self:  An instance attribute of the :class Landings:
    """
    if self.landingCatch is not None:
      self.totalCatch = 0.0
      catch = dict()
      for i in self.landingCatch:
        if i['species'] not in [u'Loðna', u'Síld', u'Kolmunni']:
          self.totalCatch += float(i['totalCatch'])/1000.0
          catch[i['species']] = float(i['totalCatch'])/1000.0
        else:
          self.totalCatch += i['totalCatch']
          catch[i['species']] = i['totalCatch']
        if self.equipment is None:
          self.equipment = i['equipment']

      self.landingCatch = catch
      self.maxCatch = self.totalCatch

      for k,v in groups.iteritems():
        if (self.shipGrossTonnage <= 8.0 and self.equipment == u'Lína'):
          self.group = 'Smábátar -8BT'
          return
        elif (self.shipGrossTonnage > 8.00 and self.shipGrossTonnage <= 13.0 and
              self.equipment == u'Lína'):
          self.group = 'Smábátar 8-13BT'
          return
        elif (self.shipGrossTonnage > 13.00 and self.shipGrossTonnage < 15.0 and
              self.equipment == u'Lína'):
          self.group = 'Smábátar 13-15BT'
          return
        elif (self.shipGrossTonnage >= 15.00 and
             self.equipment == u'Lína'):
          self.group = 'Smábátar +15BT'
          return

        for e in v:
          if self.equipment in e:
            self.group = k
            return
      else:
        self.group = 'Ýmislegt'
 
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

__author__      = 'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.1'
__maintainer__  = 'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
