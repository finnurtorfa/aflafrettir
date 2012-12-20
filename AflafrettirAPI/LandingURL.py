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

###################################################
# Class: LandingURL
###################################################
class LandingURL(object):
  
  def __init__(self, date_list):
    
    if len(date_list) is not 2: #If for some reason only 1 date object
      print "The length of the object passed to the LandingURL class must be 2...\nExiting!"
      exit()

    self.base_url = 'http://www.fiskistofa.is/'
    self.query_url = 'veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?'
    self.query_params = {
        'magn':'Samantekt',
        'dagurFra':date_list[0],
        'dagurTil':date_list[1],
        }
    self.harbours = {'Vestmannaeyjar':'1', 'Þorlákshöfn':'11', 'Grindavík':'13', 'Sandgerði':'17',
        'Keflavík':'21', 'Vogar':'25', 'Hafnarfjörður':'27', 'Kópavogur':'31', 'Reykjavík':'33', 
        'Akranes':'35', 'Hvalseyjar':'36', 'Arnarstapi':'38', 'Rif':'42', 'Ólafsvík':'43', 
        'Grundarfjörður':'45', 'Stykkishólmur':'47', 'Brjánslækur ':'55', 'Haukabergsvaðall':'56', 
        'Patreksfjörður':'57', 'Tálknafjörður':'59', 'Bíldudalur':'61', 'Þingeyri':'63', 
        'Flateyri':'65', 'Suðureyri':'67', 'Bolungarvík':'69', 'Ísafjörður':'73', 'Súðavík':'75', 
        'Norðurfjörður ':'77', 'Drangsnes':'79', 'Hólmavík':'81', 'Hvammstangi':'83', 'Blönduós':'85', 
        'Skagaströnd':'87', 'Sauðárkrókur':'89', 'Hofsós':'91', 'Haganesvík':'92', 'Siglufjörður':'93', 
        'Ólafsfjörður':'95', 'Grímsey':'97', 'Hrísey':'99', 'Dalvík':'101', 'Árskógssandur':'103', 
        'Hauganes':'104', 'Hjalteyri':'105', 'Akureyri':'107', 'Grenivík':'111', 'Húsavík':'115', 
        'Kópasker':'117', 'Raufarhöfn':'119', 'Þórshöfn':'121', 'Bakkafjörður':'123', 
        'Vopnafjörður':'125', 'Borgarfjörður Eystri':'129', 'Seyðisfjörður':'131', 'Mjóifjörður':'133', 
        'Neskaupstaður':'135', 'Eskifjörður':'137', 'Reyðarfjörður':'139', 'Fáskrúðsfjörður':'141', 
        'Stöðvarfjörður':'143', 'Breiðdalsvík':'145', 'Djúpivogur':'147', 'Hornafjörður':'149', 
        'Ýmsir staðir':'150'}

  def _request_urls(self, i):
    self.query_params.update({'hofn':self.harbours[i]})
    url = self.base_url + self.query_url + urlencode(self.query_params)
    del self.query_params['hofn']
    
    return url

  def __iter__(self):
    for i in self.harbours:
      result = {}
      result[i] = self._request_urls(i)
      yield result

###################################################
# Main body
###################################################
if __name__ == '__main__': # If run on it's own
  dates = ['01.12.2012', '11.12.2012']
  #dates = ['01.12.2012']
  
  landings = LandingURL(dates)
  url_dict = {}
  
  for i in landings:
    url_dict.update(i)

  print url_dict
