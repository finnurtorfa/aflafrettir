"""
  flask.flask_aflafrettir.soap.manager
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Add a manager class for the Directorate of Fisheries of Iceland's SOAP
  service.
"""

from suds.client import Client
from suds.sax.date import Date

class SOAPManager(object):
  """ A 'SOAPManager' object that manages connection to a SOAP service
  """
  def __init__(self, url=None, **kwargs):
    """ Initialize the :class SOAPManager:

    :param url: The URL for the WSDL description of a SOAP service.
    :param headers: A dict containing headers for a HTTP/HTTPS SOAP request
    :param kwargs: A list of keyworded arguments to pass to the client
    """
    self.url = url
    self.client = None

    if self.url:
      self.get_client(**kwargs)

  def get_client(self, **kwargs):
    """ Initializes the :class: 'suds.client.Client' object
    """
    self.client = Client(self.url, **kwargs)

  def call_method(self, method, *args):
    """ Returns a  response from a SOAP service.

    :param method: String, containing the name of the method to call
    :param args:   An arbitrary number of arguments, which the SOAP methods take
    """
    return getattr(self.client.service, method)(*args)
  

class DOFManager(SOAPManager):
  """ A 'DOFManager' object that manages connection to the Department of
  Fisheries in Iceland's SOAP service
  """
  def __init__(self, credentials, **kwargs):
    """ Initialize the :class DOFManager: object.

    :param credentials:   A dictionary containing username and password to the
                          DOF's SOAP service.
    :param kwargs:        A list of other keyword arguments to pass to DOF's
                          SOAP service.
    """
    self.url = 'https://soap.fiskistofa.is/landing/v1/LandingService?wsdl'
    super().__init__(url=self.url, headers=credentials, **kwargs)

  def get_api_version(self):
    """ Fetch the API version of the service.
    """
    return self.call_method('getAPIVersion')

  def get_fishing_areas(self):
    """ Fetch the registered fishing areas.
    """
    return self.call_method('getFishingAreas')

  def get_fishing_equipment(self):
    """ Fetch t
    """
    return self.call_method('getFishingEquipment')

  def get_fishing_stocks(self):
    """ Fetch the registered fishing stocks.
    """
    return self.call_method('getFishingStocks')

  def get_species(self):
    """ Fetch the registered fish species.
    """
    return self.call_method('getSpecies')

  def get_states(self):
    """ Fetch the registered states.
    """
    return self.call_method('getStates')

  def get_storage_methods(self):
    """ Fetch the registered states.
    """
    return self.call_method('getStorageMethods')

  def get_all_landings(self, date_from, date_to):
    """ Fetch all landings for a period of time. It is assumed that 
    :param date_from" is less than or equal to :param date_to: or it will result
    in an empty query.
    
    :param date_from:   A string|datetime|date object containing the start date
    :param date_to:     A string|datetime|date object containing the end date
    """
    date_from = Date(date_from)
    date_to = Date(date_to)

    return self.call_method('getAllLandings', date_from, date_to)

  def get_landings(self, date_from, date_to, ship_id):
    """ Fetch all landings for a specific boat for a period of time. It is 
    assumed that:param date_from" is less than or equal to :param date_to: or it
    will result in an empty query.

    :param date_from:   A string|datetime|date object containing the start date
    :param date_to:     A string|datetime|date object containing the end date
    :param ship_id:     A string with the ship's id
    """
    date_from = Date(date_from)
    date_to = Date(date_to)

    return self.call_method('getLandings', date_from, date_to, ship_id)

