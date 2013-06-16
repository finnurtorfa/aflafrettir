#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
manager
~~~~~~~~~~~
"""

from suds.client import Client

class SoapManager(object):
  """ :class SoapManager: will fetch data from the SOAP service of the Icelandic
  Directorate of Fisheries
  """
  def __init__(self):
    self.url = 'http://shiptest.fiskistofa.is/ship/ShipService?wsdl'
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
