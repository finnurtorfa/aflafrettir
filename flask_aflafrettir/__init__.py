"""
  flask.aflafrettir
  ~~~~~~~~~~~~~~

  Adds support for fetching data from the Department of Fisheries in Iceland and
  calculating the total catch for certain period of time.
"""
from .soap import DOFService

class Aflafrettir(object):
  """ A collection of functions to configure and fetch data from the SOAP 
  service of the Department of Fisheries in Iceland
  """ 
  def __init__(self, username=None, password=None):
    """ An initialization function for :class Aflafrettir:

    :param self:      An instance attribute of the :class Aflafrettir:
    :param username:  Username to pass to the DOFManager.
    :param password:  Password to pass to the DOFManager.
    """
    self.username = username
    self.password = password
    self.service = None 

    if ( username is not None and 
         password is not None ):
      self.configure(username, password)

  def configure(self, username, password):
    """ 
    :param self:      An instance attribute of the :class Aflafrettir:
    :param username:  Username to pass to the DOFManager.
    :param password:  Password to pass to the DOFManager.
    """
    if ( username is not None and 
         password is not None ):
      self.username = username
      self.password = password

      self.service = DOFService(credentials={'Username':username, 
                                             'Password':password})
    else:
      self.service = None

  def make_list(self, date_from, date_to): 
    """ Takes in two dates, fetches the landings for the period and creates an
    excel sheet with lists of the landings.

    :param self:        An instance attribute of the :class Aflafrettir:
    :param date_from:   A start date of the period
    :param date_to:     An end date of the period.
    """
    pass

__author__      = 'Finnur Smári Torfason'
__copyright__   = 'Copyright 2015, www.aflafrettir.is'
__credits__     = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.2'
__maintainer__  = 'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
