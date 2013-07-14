#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
manager
~~~~~~~~~~~
"""

from suds.client import Client
from suds.sax.date import Date

class SoapManager(object):
  """ :class SoapManager: will fetch data from the SOAP service of the Icelandic
  Directorate of Fisheries
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
