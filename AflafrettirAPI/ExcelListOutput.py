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

from QueryLandingURL import QueryLandingURL
from ParseHTML import ParseHTML
from TotalCatch import TotalCatch
import xlwt


###################################################
# class: TotalCatch
###################################################
class ExcelListOutput(object):
  
  def __init__(self, landingList, filename, date1, date2):
    self.landing = landingList
    self.landingList = sorted(landingList['Landings'], key=lambda k: k['Catch'],
        reverse=True)
    self.wb = xlwt.Workbook('utf-8')
    self.style0 = xlwt.easyxf('font: name Arial, color-index black',
        num_format_str='#,##0') 
    self.style1 = xlwt.easyxf('font: name Arial, color-index black, bold on',
        num_format_str='#,##0') 
    self.item = ['Skipaskrárnúmer', 'Nafn', 'Fjöldi', 'Heildarafli', 
        'Mesti afli', 'Höfn', 'Veiðarfæri']
    self.key = ['ShipID', 'Name', 'Number', 'Catch', 'Most', 'Harbour', 'Gear']
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
      'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=1&dagurTil=11.12.2012&magn=Samantekt',
      'url1':'http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?dagurFra=01.12.2012&hofn=149&dagurTil=11.12.2012&magn=Samantekt',
      }
  landingList = []
  html = QueryLandingURL(url)

  for i in html:
    table = ParseHTML(i)
    for j in table:
      landingList.append(j)
      #print j

  lists = TotalCatch(landingList)
  landingList = []
  for i in lists:
    landingList.append(i)

  List = {'Group':'Heild', 'Landings':landingList}

  Excel = ExcelListOutput(List, 'Hey.xls', '01.01.01', '01.01.10')
  Excel.save_excel()
