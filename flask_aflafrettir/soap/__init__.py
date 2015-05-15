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
  
