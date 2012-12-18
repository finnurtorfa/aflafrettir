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

class AflafrettirGUI(wx.Frame):

  def __init__(self, parent, id, title):
    wx.Frame.__init__(self, parent, id, title, size=(300, 200))
    self.Show()

    menu = wx.MenuBar() # A new menubar

    # Filemenu on the menubar
    file = wx.Menu()
    quit = wx.MenuItem(file, 101, '&Quit\tCtrl+W', 'Loka forriti')
    quit.SetBitmap(wx.Image('/usr/share/gtk-doc/html/pygtk/icons/stock_exit_24.png',
      wx.BITMAP_TYPE_PNG).ConvertToBitmap())
    file.AppendItem(quit)

    # Append the menu's to the menubar
    menu.Append(file, '&File')

    # Create the menubar and a statusbar
    self.SetMenuBar(menu)
    self.CreateStatusBar()

class AflafrettirApp(wx.App):

  def OnInit(self):
    frame = AflafrettirGUI(None, -1, u'Aflafréttir')
    return True


if __name__ == '__main__':
  app = AflafrettirApp(0)
  app.MainLoop()
  
