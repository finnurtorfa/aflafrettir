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

import logging
from AflafrettirAPI import *
#from AflafrettirAPI import LandingURL, QueryLandingURL, ParseHTML
#from AflafrettirAPI import GroupLandingInfo, TotalCatch, ExcelListOutput
from utils.event import MessageEvent
from wx import PostEvent

class CalculateList(object):
  def __init__(self, notify_window, date1, date2):
    self._notify_window = notify_window
    self.date_list = [date1, date2]
    self.landing_urls = LandingURL(self.date_list)

  def get_landing_url(self):
    PostEvent(self._notify_window, MessageEvent('Útbý vefslóðir vegna' +
      ' fyrirspurna\n', 1))
    landing_url = {}
    for url in self.landing_urls:
      landing_url.update(url)

    return landing_url

  def get_data_from_html(self, url_dict):
    html_dict = {}
    landing_list = []
    html = QueryLandingURL(url_dict)
    
    for h in html:
      PostEvent(self._notify_window, MessageEvent('Sæki upplýsingar um' +
        ' landanir í/á %s\n' % h['Harbour'], 1))
      logging.info("Fetching data for harbour of %s", h['Harbour'])
      table = ParseHTML(h)
      for t in table:
        landing_list.append(t)

    return landing_list

  def save_data(self, landingList, filename, date1, date2):
    totalList = {'Group':'Heild', 'Landings':landingList}
    
    excel = ExcelListOutput(totalList, filename, date1, date2)
    excel.save_excel()

  def calc_total_catch(self, landing_list):
    PostEvent(self._notify_window, MessageEvent('Reikna út heildarafla\n', 1))
    groups = GroupLandingInfo(landing_list)
    landing_list = []
    for g in groups:
      for key in g:
        logging.info("Calculating %s", key)
        lists = TotalCatch(g[key])
      for l in lists:
        landing_list.append(l)

    return landing_list
