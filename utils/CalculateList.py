#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# File: LandingURL.py
# Author: Finnur Smári Torfason
# Date: 11.12.2012
# About:
#   Class for gathering landing information from the web page of the Directorate
#   of Fisheries in Iceland.
#   The CalculateList class calculates the list of landings

from api.LandingURL import LandingURL
from api.QueryLandingURL import QueryLandingURL
from api.ParseHTML import ParseHTML

class CalculateList(object):
  def __init__(self, date1, date2):
    self.date_list = [date1, date2]
    self.landing_urls = LandingURL(self.date_list)

  def get_landing_url(self):
    landing_url = {}
    for url in self.landing_urls:
      landing_url.update(url)

    return landing_url

  def get_data_from_html(self, url_dict):
    html_dict = {}
    landing_list = []
    html = QueryLandingURL(url_dict)
    
    for h in html:
      table = ParseHTML(h)
      for t in table:
        landing_list.append(t)

    return landing_list

