#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# File: ExcelListOutput.py
# Author: Finnur Smári Torfason
# Date: 11.12.2012
# About:
#   Class for gathering landing information from the web page of the Directorate
#   of Fisheries in Iceland.
#   The ExcelListOutput class takes in as a parameter a list of dictionaries
#   containing landing info and sorts the list in descending order by the catch.
#   Then it puts the list in an excel(.xls) format.

from QueryURL import QueryURL
from ParseHTML import ParseHTML
from TotalCatch import TotalCatch
import xlwt


###################################################
# class: TotalCatch
###################################################
class ExcelListOutput(object):
  
  def __init__(self, landingList, filename, date1, date2):
    self.landing = landingList
    self.landingList = sorted(landingList['Landings'], key=lambda k: k['Catch US'],
        reverse=True)
    self.wb = xlwt.Workbook('utf-8')
    self.style0 = xlwt.easyxf('font: name Arial, color-index black',
        num_format_str='#,##0') 
    self.style1 = xlwt.easyxf('font: name Arial, color-index black, bold on',
        num_format_str='#,##0') 
    self.item = ['Skipaskrárnúmer', 'Nafn', 'Fjöldi', 'Heildarafli reiknað e. höfnum', 
        'Heildarafli reiknað e. teg.', 'Mesti afli', 'Höfn', 'Veiðarfæri']
    self.key = ['ShipID', 'Name', 'Number', 'Total S', 'Total US', 'Most S', 'Harbour', 'Gear']
    self.filename = filename
    self.date1 = date1
    self.date2 = date2


  def save_excel(self):
    ws = self.wb.add_sheet(self.landing['Group'])
    header = u'Afli fyrir tímabilið frá %s til %s' % (self.date1, self.date2)
    ws.write(0, 0, header, self.style0)
    ctr = 0
    for i in self.item:
      ws.write(1, ctr, i, self.style1)
      ctr += 1
    
    row = 0
    for l in self.landingList:
      col = 0
      for i in self.key:
        ws.write(row+2, col, l[i])
        col += 1
      row += 1

    self.wb.save(self.filename)


###################################################
# Main body
###################################################
if __name__ == '__main__': # If run on it's own

  url = {
      'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=1&dagurTil=11.12.2012&magn=Sundurlidun',
      'url1':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=149&dagurTil=11.12.2012&magn=Sundurlidun',
      }
      
  url2 = {
      u'Síld 30':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?p_fteg=Þorskur+1&p_fra=01.12.2012&p_til=11.12.2012',
      u'Loðna 31':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?p_fteg=Ufsi+3&p_fra=01.12.2012&p_til=11.12.2012'
      }

  harbour_list = []
  species_list = []
  landing_list = []
  html = QueryURL(url)
  html2 = QueryURL(url2)
  h_keys = ['Date', 'ShipID', 'Name', 'Gear', 'Catch S', 'Harbour']
  s_keys = ['Name', 'Category', 'Catch US', 'Species']

  for i in html:
    table = ParseHTML(i, [2, 1], ['Date', 'ShipID', 'Name', 'Gear', 'Stuff', 'Catch S'],
        range(0,6), 'Harbour')
    for j in table:
      harbour_list.append(j)
      print j
  
  for i in html2:
    table = ParseHTML(i, [1, 2], ['ShipID', 'Name', 'Category', 'Catch US'],
        range(0,4), 'Species')
    for j in table:
      print j
      species_list.append(j)
  
  lists = TotalCatch(harbour_list, species_list, h_keys, s_keys)
  for i in lists:
    landing_list.append(i)

  List = {'Group':'Heild', 'Landings':landing_list}

  Excel = ExcelListOutput(List, 'Hey.xls', '01.01.01', '01.01.10')
  Excel.save_excel()
