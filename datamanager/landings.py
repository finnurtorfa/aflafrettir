#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
manager
~~~~~~~~~~~
"""

from suds.client import Client
from suds.sax.date import Date

class Landings(object):
  """ :class Landings: contains info about landings such as catch, total catch,
  shipID, name etc.
  """
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
      u'RMNT', u'KRAL']
    }
 
  def __init__(self):
    """ Initializes the :class Landings:
    """
    self.totalCatch       = None
    self.landingCatch     = None
    self.landingDate      = None
    self.landingHarbour   = None
    self.shipGrossTonnage = None
    self.shipName         = None
    self.shipNumber       = None
    self.equipment        = None
    self.group            = None
    
  def set_variable(self, data):
    """ Checks if attributes from the :class Client: 'getLandings' method
    matching the names of the strings in the 'keys' class variable exist
    and passes them to the :class Landings: instance variables.
    """
    for key in Landings.keys:
      val = getattr(data, key)
      setattr(self, key, val)

  def calc_total_catch(self):
    """ Calculates the total catch, equipment used and which group the equipment
    belongs to, from a single fishing trip.
    """
    if self.landingCatch is not None:
      self.totalCatch = 0
      for i in self.landingCatch:
        self.totalCatch += i['totalCatch']
        if self.equipment is None:
          self.equipment = i['equipment']

      for k,v in Landings.groups.iteritems():
        for e in v:
          if self.equipment in e:
            self.group = k
            return
      else:
        self.group = 'Ýmislegt'

if __name__ == '__main__':
  manager = SoapManager()

__author__      = 'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.1'
__maintainer__  = 'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
