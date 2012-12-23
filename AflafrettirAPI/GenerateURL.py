#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
  File: GenerateURL.py

  The GenerateURL class is used by the Aflafrettir API, a web scraping API. The
  API is used to gather information on landings from the website of Directorate
  of Fisheries in Iceland.

  The GenerateURL class is initialized with a base_url, query_params, new_param
  and an optional parameter called species, as described by the __init__
  docstring. It returns a dictionary with a URL that can be used to query the
  database of the website of Directorate of Fisheries in Iceland in a desired
  way.
"""
from urllib import urlencode
from ParseHTML import ParseHTML
from QueryURL import QueryURL

class GenerateURL(object):
  """
  class: GenerateURL
  """
  
  def __init__(self, base_url, query_params, new_param, species=False):
    """
    Initialize function. To Initialize the GenerateURL object upon creation
    Input:
      base_url: The base URL for querying
      query_params: The HTTP GET parameters
      new_param: An extra query_param that is appended to the query_params when
        it's value is known
      species: A boolean variable used to distinguish between types of queries,
        as explained in the _reques_urls() function
    """
    self.base_url = base_url
    self.query_params = query_params
    self.new_param = new_param
    self.species = species
    self.param_dict = self.get_params()

  def _request_urls(self, i):
    """
    This function returns the query url used to query the database of
    Directorate of Fisheries in Iceland.
    If self.species is True, this function returns a url for querying the
    database for landings per harbours
    If self.species is False, this function returns a url for querying the
    database for how much each ship has caught of each species.
    """
    self.query_params.update({self.new_param:self.param_dict[i]})
    url = self.base_url + urlencode(self.query_params)
    del self.query_params[self.new_param]
    
    return url
  
  def get_params(self):
    """
    This function fetches the query parameters from the website of Directorate
    of Fisheries in Iceland. 
    If self.species is True, then this function returns a dictionary of species
    available
    If self.species is False, then this function returns a dictionary of
    harbours and their id's.
    """
    key = 'None'
    html = QueryURL({'url':self.base_url}, key)
    for h in html:
      result = ParseHTML(h, key).get_list(self.species)

    return result
 
  def __iter__(self):
    """
    Iterate over the param_dict dictionary to yield a complete request URL to
    query later.
    """
    for i in self.param_dict:
      result = {}
      result[i] = self._request_urls(i)

      yield result

if __name__ == '__main__':
  """
  For testing purposes. This part of the program is only run if the class is
  called explicitly
  """
  dates = ['01.12.2012', '11.12.2012']
  
  q_url ='http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?'
  q_p = {'magn':'Samantekt', 'dagurFra':dates[0], 'dagurTil':dates[1]}
  n_p = 'hofn'
  
  q_url2 = 'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?'
  q_p2 = {'p_fra':dates[0], 'p_til':dates[1]}
  n_p2 = 'p_fteg'

  urls = GenerateURL(q_url, q_p, n_p)
  urls2 = GenerateURL(q_url2, q_p2, n_p2, True)
  
  harbours = {}
  species = {}
  
  for i in urls:
    harbours.update(i)
  for i in urls2:
    species.update(i)

  print harbours
 print species

# Authorship information
__author__ = 'Finnur Smári Torfason'
__copyright__ = 'Copyright 2012, www.aflafrettir.com'
__credits__ = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Finnur Smári Torfason'
__email__ = 'finnurtorfa@gmail.com'
__status__ 'Development'

