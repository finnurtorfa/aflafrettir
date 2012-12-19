#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# File: gui.py
# Author: Finnur Smári Torfason
# Date: 17.12.2012
# About:
#   GUI class for the application. The GUI will use the Aflafrettir web scraping
#   API to gather data and manipulate it.

import wx
from api.LandingURL import LandingURL

class AflafrettirGUI(wx.Frame):

  def __init__(self, parent, id, title):
    wx.Frame.__init__(self, parent, id, title, size=(400, 370))
    self.Show()

    menu = wx.MenuBar() # A new menubar

    # Filemenu on the menubar
    file = wx.Menu()
    quit = wx.MenuItem(file, 101, '&Quit\tCtrl+W', 'Loka forriti')
    quit.SetBitmap(wx.Image('gui/imgs/stock_exit_24.png',
      wx.BITMAP_TYPE_PNG).ConvertToBitmap())
    file.AppendItem(quit)

    # Append the menu's to the menubar
    menu.Append(file, '&File')

    # Create a notebook
    nb = wx.Notebook(self, wx.ID_ANY)

    # Main page
    self.page1 = AflafrettirMainPage(nb)

    # Add page to the notebook
    nb.AddPage(self.page1, u'Útbúa lista')

    # Event bindings
    self.Bind(wx.EVT_MENU, self.OnQuit, id=101)
    self.Bind(wx.EVT_BUTTON, self.OnGatherInfo, id=201)

    # Create the menubar and a statusbar
    self.SetMenuBar(menu)
    self.CreateStatusBar()

  def OnQuit(self, event):
    self.Close()

  def OnGatherInfo(self, event):
    date1 = self.page1.date1.GetValue().Format("%d.%m.%Y")
    date2 = self.page1.date2.GetValue().Format("%d.%m.%Y")
    
    landings = LandingURL([date1, date2])

    for l in landings:
      print l

class AflafrettirMainPage(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent, wx.ID_ANY)

    self.SetBackgroundColour('Grey')
    
    # Date controls
    wx.StaticText(self, -1, 'Dagsetning 1:', pos=(10,10))
    self.date1 = wx.DatePickerCtrl(self, -1, pos=(155,10), size=(150,-1))
    wx.StaticText(self, -1, 'Dagsetning 2:', pos=(10,45))
    self.date2 = wx.DatePickerCtrl(self, -1, pos=(155,45), size=(150,-1))

    self.catBtn = wx.Button(self, 201, label='Byrja', pos = (10,80),
        size=(90,30))

    self.msgBox = wx.TextCtrl(self, -1, pos=(10,120), size=(370,140),
        style=wx.TE_MULTILINE|wx.TE_READONLY)
class AflafrettirApp(wx.App):

  def OnInit(self):
    frame = AflafrettirGUI(None, -1, u'Aflafréttir')
    return True

  def ReturnValue():
    val = self.GetValue()
    return val

def main():
  app = AflafrettirApp(0)
  app.MainLoop()

if __name__ == '__main__':
 main() 
