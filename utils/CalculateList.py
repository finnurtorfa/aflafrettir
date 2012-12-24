#!/usr/bin/python
# -*- coding: cp1252 -*-
# 
# File: LandingURL.py
# Author: Finnur Smári Torfason
# Date: 11.12.2012
# About:
#   Class for gathering landing information from the web page of the Directorate
#   of Fisheries in Iceland.
#   The CalculateList class calculates the list of landings

import logging
from wx import PostEvent
from utils.event import MessageEvent
from AflafrettirAPI import *

class CalculateList(object):
  def __init__(self, notify_window, date1, date2):
    self._notify_window = notify_window
    self.date_list = [date1, date2]

  def get_lists(self, date_list):
    msg = 'Útbý vefslóðir vegna fyrirspurna\n'
    PostEvent(self._notify_window, MessageEvent(msg, 1))
    
    q_urls =[
        'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?',
        'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?'
        ]
    q_params = [
        {'magn':'Samantekt', 'dagurFra':date_list[0], 'dagurTil':date_list[1]},
        {'p_fra':date_list[0], 'p_til':date_list[1]}
        ]
    n_params = ['hofn', 'p_fteg']

    harbours = DOF_URLGenerator(q_urls[0], q_params[0], n_params[0])
    species = DOF_URLGenerator(q_urls[1], q_params[1], n_params[1], True)

    h_urls = {}
    s_urls = {}
 
    for h in harbours:
      h_urls.update(h)
    for s in species:
      s_urls.update(s)

    return (h_urls, s_urls)
 

  def get_landing_url(self):
    msg = 'Útbý vefslóðir vegna fyrirspurna'
    PostEvent(self._notify_window, MessageEvent(msg, 1))
    
    harbour_url = {}
    species_url = {}
    
    q_url = '/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?'
    q_p = {'magn':'Samantekt', 'dagurFra':self.date_list[0], 'dagurTil':self.date_list[1]}
    n_p = 'hofn'
    
    q_url2 = '/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?'
    q_p2 = {'p_fra':self.date_list[0], 'p_til':self.date_list[1]}
    n_p2 = 'p_fteg'
    
    harbours, species = self.get_lists()
    h_urls= LandingURL(harbours, q_url, q_p, n_p)
    s_urls= LandingURL(species, q_url2, q_p2, n_p2)

    for url in h_urls:
      harbour_url.update(url)

    for url in s_urls:
      species_url.update(url)

    return (harbour_url, species_url)

  def get_data_from_html(self, url_dict, new_key, species=False):
    html_dict = {}
    landing_list = []
    html = QueryURL(url_dict)
    
    for h in html:
      msg = 'Sæki upplýsingar vegna %s\n' % str(h['name'])
      PostEvent(self._notify_window, MessageEvent(msg, 1))
      logging.info("Fetching data for %s", h['name'])
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
