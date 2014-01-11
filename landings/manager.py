#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
manager.py
~~~~~~~~~~~

Contains :class LandingsManager: a manager class for the SOAP service provided
by the Directorate of Fisheries in Iceland. Specifically this class is used for
fetching landings information from the service.
"""

from suds.client import Client
from suds.sax.date import Date

class LandingsManager(object):
  """ :class LandingsManager: will fetch landings data from the SOAP service of the 
  Icelandic Directorate of Fisheries
  """
  def __init__(self):
    self.url = 'http://ship.fiskistofa.is/ship/ShipService?wsdl'
    self.headers = None
    self.client = None
    self.dates = None

  def set_credentials(self, username, password):
    """ Sets the header dictionary used when the :class: 'suds.client.Client' is
    initialized
    """
    self.headers = {'Username':username, 'Password':password}

  def get_client(self):
    """ Initializes the :class: 'suds.client.Client' object
    """
    if self.headers:
      self.client = Client(self.url, headers=self.headers)
    else:
      raise ValueError('Missing headers(Username and Password)')

  def call_method(self, method, *args):
    """ Returns a list, containing response from the Icelandic Directorate of
    Fisheries's SOAP service. Raises an AttributeError if the method does not
    exist. Raises a suds.WebFault in case of other errors such as insufficient
    number of arguments etc.

    :param method: String, containing the name of the method to call
    :param args:   An arbitrary number of arguments, which the SOAP methods take
    """
    return getattr(self.client.service, method)(*args)
  
  def get_landings(self, date_from, date_to):
    """ Returns a list, containing response from the Icelandic Directorate of
    Fisheries's SOAP 'getLandings' method. Raises an AttributeError if the method does not
    exist. Raises a suds.WebFault in case of other errors such as insufficient
    number of arguments etc.

    :param date_from: A string containing a date to get the landings from 
    :param date_from: A string containing a date to get the landings to
    """
    date_from = Date(date_from)
    date_to = Date(date_to)

    if date_from > date_to:
      (date_from, date_to) = (date_to, date_from)

    return self.call_method('getLandings', date_from, date_to)

if __name__ == '__main__':
  manager = LandingsManager()

__author__      = u'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = [u'Finnur Smári Torfason', u'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.1'
__maintainer__  = u'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
