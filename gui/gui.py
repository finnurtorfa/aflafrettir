#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# File: gui.py
# Author: Finnur Smári Torfason
# Date: 17.12.2012
# About:
#   GUI class for the application. The GUI will use the Aflafrettir web scraping
#   API to gather data and manipulate it.

import wx, logging, datetime, os.path
from utils.CalculateList import CalculateList as cl
from utils.event import MessageEvent
from threading import Thread

EVT_RESULT_ID = 104

class calcThread(Thread):
  def __init__(self, notify_window, filename, date1, date2):
    Thread.__init__(self)
    
    self._notify_window = notify_window
    self.filename = filename
    self.date1 = date1
    self.date2 = date2
    self.start()

  def run(self):
    now = datetime.datetime.now()
    msg = 'Byrja að reikna lista klukkan %s\n' % now.strftime('%H:%M:%S')
    wx.PostEvent(self._notify_window, MessageEvent(msg, 1))
    
    the_list = cl(self._notify_window, self.date1, self.date2)
    
    h_list, s_list = the_list.get_lists([self.date1, self.date2])
    harbour_list = the_list.get_data_from_html(h_list, [2,1], ['ShipID', 'Name',
      'Gear', 'Catch'], range(1,5))
    species_list = the_list.get_data_from_html(s_list, [1,2], ['ShipID', 'Name',
      'Category', 'Catch'], range(0,4))

    landing_list = the_list.calc_total_catch(harbour_list, species_list)

    wx.PostEvent(self._notify_window, MessageEvent('Útbý excel skjal\n', 1))
    the_list.save_data(landing_list, self.filename, self.date1, self.date2)
    
    later = datetime.datetime.now()
    msg = 'Klára að reikna lista klukkan %s\n' % later.strftime('%H:%M:%S')
    wx.PostEvent(self._notify_window, MessageEvent(msg, 1))
 
class AflafrettirGUI(wx.Frame):

  def __init__(self, parent, id, title):
    wx.Frame.__init__(self, parent, id, title, size=(400, 370))
    
    self.Show()

    # Some basic settings
    self.dirname = os.path.join(os.path.dirname(__file__), '..')
    self.filename = ''

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
    self.EVT_RESULT(self, self.postMsg)

    # Create the menubar and a statusbar
    self.SetMenuBar(menu)
    self.CreateStatusBar()

  def OnQuit(self, event):
    self.Close()

  def OnGatherInfo(self, event):
    date1 = self.page1.date1.GetValue().Format("%d.%m.%Y")
    date2 = self.page1.date2.GetValue().Format("%d.%m.%Y")
    
    if date1 > date2:
      tmp = date1
      date1 = date2
      date2 = tmp
    elif date1 == date2:
      msg = 'Viðvörun: Dagsetningar þær sömu\n'
      wx.PostEvent(self, MessageEvent(msg, 1))
      return

    dlg = wx.FileDialog(self, 'Choose a file', self.dirname, '', '*.*', 
        wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

    if dlg.ShowModal() == wx.ID_OK:
      self.dirname = dlg.GetDirectory()
      self.filename = dlg.GetFilename()
      
      filename = os.path.join(self.dirname, self.filename)
      calcThread(self, filename, date1, date2)

    dlg.Destroy()

  def EVT_RESULT(self, win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)

  def postMsg(self, e):
    self.page1.msgBox.AppendText(e.data)

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
