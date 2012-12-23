#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# File: QueryLandingURL.py
# Author: Finnur Smári Torfason
# Date: 11.12.2012
# About:
#   Class for gathering landing information from the web page of the Directorate
#   of Fisheries in Iceland.
#   The QueryLandingURL class takes as a parameter a url object and returns the
#   HTML code representing the queried URL

import urllib2, socket, logging, time

socket.setdefaulttimeout(10) # 10 sec timeout

###################################################
# Class: QueryLandingURL
###################################################
class QueryURL(object):
  
  def __init__(self, url_list):
    self.url_list = url_list
    self.new_key = 'name'
    
  def get_html_content(self, url, timeout):
    for attempts in range(3):
      try:
        content = urllib2.urlopen(url)
        content = unicode(content.read(),
            content.headers['content-type'].split('charset=')[-1])
        result = {'error':0, 'content':content}
      except (urllib2.URLError, socket.timeout), e:
        logging.exception('%s', e.args)
        time.sleep(timeout)
        result = {'error':-1, 'content':url}

    return result

  def __iter__(self):
    for url in self.url_list:
      result = self.get_html_content(self.url_list[url], 0.5)
      result[self.new_key] = url
      yield result


if __name__ == '__main__': # If run on it's own
  url = {
      'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=149&dagurTil=11.12.2012&magn=Samantekt',
      'url1':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=1&dagurTil=11.12.2012&magn=Samantekt'
      }
      
  html = QueryLandingURL(url)
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
