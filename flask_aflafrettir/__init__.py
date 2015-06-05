"""
  flask.aflafrettir
  ~~~~~~~~~~~~~~

  Adds support for fetching data from the Department of Fisheries in Iceland and
  calculating the total catch for certain period of time.
"""
from .soap import DOFService
from .landings import Landings
from .excel import save_excel

class Aflafrettir(object):
  """ A collection of functions to configure and fetch data from the SOAP 
  service of the Department of Fisheries in Iceland
  """ 
  def __init__(self, app=None, username=None, password=None):
    """ An initialization function for :class Aflafrettir:

    :param self:      An instance attribute of the :class Aflafrettir:
    :param app:       A Flask applications instance
    :param username:  Username to pass to the DOFManager.
    :param password:  Password to pass to the DOFManager.
    """
    self.username = username
    self.password = password
    self.service = None 
    self.app = None

    if ( username is not None and 
         password is not None ):
      self.configure(username, password)

    if app is not None:
      self.init_app(app)

  def init_app(self, app, username=None, password=None):
    """ Initialize the Flask-Aflafrettir extension for the specified app

    :param self:  An instance attribute of the :class Aflafrettir:
    :param app:   A Flask applications instance
    """
    if ( username is not None and
         password is not None ):
      self.configure(username, password)

    if not hasattr(app, 'extensions'):
      app.extension = {}

    if 'aflafrettir' in app.extensions:
      raise ValueError('Flask-Aflafrettir has already been initialized on this'
                       'application: {0}'.format(app))
    else:
      app.extensions['aflafrettir'] = self

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

  def make_list(self, name, date_from, date_to): 
    """ Takes in two dates, fetches the landings for the period and creates an
    excel sheet with lists of the landings.

    :param self:        An instance attribute of the :class Aflafrettir:
    :param name:        A name for the excel file
    :param date_from:   A start date of the period
    :param date_to:     An end date of the period.
    """
    if self.service is None:
      return

    try: 
      landings_list = self.service.get_all_landings(date_from, date_to)
      equipment_list = self.service.get_fishing_equipment()
      species_list = self.service.get_species()
    except Exception:
      pass
    landings = []

    for l in landings_list:
      landing = Landings(equipment_list, species_list)
      landing.insert(l)
      landings.append(landing)

    landings_sorted = sort(landings)
    save_excel(name, landings_sorted)

__author__      = 'Finnur Smári Torfason'
__copyright__   = 'Copyright 2015, www.aflafrettir.is'
__credits__     = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__     = 'GPL v3'
__version__     = '0.2'
__maintainer__  = 'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
