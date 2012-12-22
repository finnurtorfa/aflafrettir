#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# File: LandingURL.py
# Author: Finnur Smári Torfason
# Date: 11.12.2012
# About:
#   Class for gathering landing information from the web page of the Directorate
#   of Fisheries in Iceland.
#   The LandingURL class takes as a parameter 2 date objects and returns the URL
#   that will be queried

from urllib import urlencode
from ParseHTML import ParseHTML
from QueryLandingURL import QueryLandingURL

###################################################
# Class: LandingURL
###################################################
class LandingURL(object):
  
  def __init__(self, list_dict, query_url, query_params, new_param):
    
    self.base_url = 'http://www.fiskistofa.is'
    self.list_dict = list_dict
    self.query_url = query_url
    self.query_params = query_params
    self.new_param = new_param

  def _request_urls(self, i, new_param):
    self.query_params.update({new_param:self.list_dict[i]})
    url = self.base_url + self.query_url + urlencode(self.query_params)
    del self.query_params[new_param]
    
    return url

  def __iter__(self):
    for i in self.list_dict:
      result = {}
      result[i] = self._request_urls(i, self.new_param)

      yield result

###################################################
# Main body
###################################################
if __name__ == '__main__': # If run on it's own
  dates = ['01.12.2012', '11.12.2012']
  q_p = {'magn':'Samantekt', 'dagurFra':dates[0], 'dagurTil':dates[1]}
  q_p2 = {'p_fra':dates[0], 'p_til':dates[1]}
  q_url = '/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?'
  q_url2 = '/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?'
  n_p = 'hofn'
  n_p2 = 'p_fteg'

  #landings = LandingURL(q_url, q_p, n_p)
  url_dict = {}
  
  for i in landings:
    url_dict.update(i)

  print url_dict
