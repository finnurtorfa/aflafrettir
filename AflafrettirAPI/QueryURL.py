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

import urllib2, socket, logging

socket.setdefaulttimeout(10) # 10 sec timeout

###################################################
# Class: QueryLandingURL
###################################################
class QueryURL(object):
  
  def __init__(self, url_list, new_key):
    self.url_list = url_list
    self.new_key = new_key
    
  def _get_html_content(self, url):
    try:
      content = urllib2.urlopen(self.url_list[url])
      content = unicode(content.read(),
          content.headers['content-type'].split('charset=')[-1])
    except(urllib2.URLError, socket.timeout), e:
      logging.exception('%s', e.args)
      return {
          'error':-1, 
          'content':self.url_list[url]
          }

    return {
        'error':0, 
        'content':content
        }

  def __iter__(self):
    for url in self.url_list:
      result = self._get_html_content(url)
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

