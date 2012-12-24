#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Class: QueryURL
=========

*  The QueryURL class is used by the Aflafrettir API, a web scraping API. The API is used to gather information on landings from the website of Directorate of Fisheries in Iceland.

*  The QueryURL class is initialized with a url_list and returns a html document
corresponding to each of the url's in the url_list.

*  Example use of the class:

        # Initialization parameters
        url = {
        'url':'www.fiskistofa.is',
        'url1':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?'
        }
        
        html = QueryURL(url)
        for i in html:
          print i
"""
import urllib2, socket, logging, time

socket.setdefaulttimeout(10) # 10 sec timeout

class QueryURL(object):
  
  def __init__(self, url_list):
    """
    Args:
      self:     The instance attributes of the QueryURL object
      url_list: A list of dictionaries containing the URL's to be queried
    Returns:
      None
    """
    self.url_list = url_list
    self.new_key = 'name'
    
  def get_html_content(self, url, timeout):
    """
    Args:
      self:     The instance attributes of the QueryURL object
      url:      The url to be queried
      timeout:  Timeout parameter, in case of some exception
    Returns:
      result:   A dictionary containing the error code, and html content.
                In case of a failure the content is the url that failed
    """
    for attempts in range(3):
      try:
        content = urllib2.urlopen(url)
        content = unicode(content.read(),
            content.headers['content-type'].split('charset=')[-1])
        result = {'error':0, 'content':content}
        break
      except (urllib2.URLError, socket.timeout), e:
        logging.exception('Attempt %d failed while fetching %s\n%s',attempt, url, e.args)
        time.sleep(timeout)
        result = {'error':-1, 'content':url}

    return result

  def __iter__(self):
    """
    Args:
      self:   The instance attributes of the QueryURL object
    Yields:
      result: A dictionary containing the html content of the queried URL, the
              error code and the key of the queried url
    """
    for key in self.url_list:
      result = self.get_html_content(self.url_list[key], 0.5)
      result[self.new_key] = key
      yield result


if __name__ == '__main__': # If run on it's own
  url = {
      'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=149&dagurTil=11.12.2012&magn=Samantekt',
      'url1':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?p_fteg=Tindaskata+12&p_fra=01.12.2012&p_til=11.12.2012'
      }
      
  html = QueryURL(url)
  for i in html:
    print i

# Authorship information
__author__ = 'Finnur Smári Torfason'
__copyright__ = 'Copyright 2012, www.aflafrettir.com'
__credits__ = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Finnur Smári Torfason'
__email__ = 'finnurtorfa@gmail.com'
__status__ = 'Development'
