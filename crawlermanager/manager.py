#!/usr/bin/python
# *-* encoding: utf-8 *-*

import Queue

from PySide.QtCore import QThread, Signal
from webscraper import DOFWebScraper


class WebCrawler(QThread):
  """ :class WebCrawler: object which crawls the website of Directorate of
  Fisheries and feeds the HTML code to the :class: 'DOFWebScraper' object.
  """
  fetchReady = Signal(str)
  fetchDone = Signal(bool)

  def __init__(self, url, queue_in, queue_out, param_name, params=None, harbour=True):
    """ Initializes the :class: 'WebCrawler' object.

    :param self: instance attribute of :class: 'WebCrawler' object
    :param url: a URL used by various methods
    :param queue_in: a :class: 'Queue' object
    :param param_name: the name of the variable GET parameters
    :param params: the variable GET parameters
    :param harbour: a boolean value to indicate whether the :class:
                    'WebCrawler' object is querying the DOF database for
                    harbours or species.
    """
    QThread.__init__(self)

    self.url = url
    self.queue_in = queue_in
    self.queue_out = queue_out
    self.param_name = param_name
    self.params = params
    self.harbour = harbour
    
    self.new_params = self.get_params(url, {'name':param_name})

    self.daemon = True

  def run(self):
    """ Runs the 'WebCrawler' thread. Runs continuously checking if the input
    queue is empty, if not, calls the callback function that is popped of the
    queue and stores the returning data in the output queue.

    :param self: instance attribute of :class: 'WebCrawler' object
    """
    self.populate_queue(self.new_params)
    while True:
      get_html_cb = self.queue_in.get()
      resp = get_html_cb[0](self.url, **get_html_cb[1])
      if self.harbour:
        self.fetchReady.emit(get_html_cb[2]['hofn'])
        ws = DOFWebScraper(resp.text, get_html_cb[2])
      else:
        self.fetchReady.emit(get_html_cb[2]['p_fteg'])
        ws = DOFWebScraper(resp.text, get_html_cb[2], False)

      if ws.table is not None:
        data = ws.get_data(ws.table)
        if data:
          self.queue_out.put(data)

      self.queue_in.task_done()

      if self.queue_in.empty():
        print "Þráður Búinn"
        self.fetchDone.emit(True)


  def get_html(self, url, **kwargs):
    """ Sends a GET request, returns :class: 'Response' object

    :param self: instance attribute of :class: 'WebCrawler' object
    :param url: a URL for the new :class: 'Request' object
    :param **kwargs: optional parameters that 'request' takes
    """
    import requests
    
    return requests.get(url, params=kwargs)

  def get_params(self, url, param):
    """ Passes :params: 'url' and 'param' to :function: 'get_html', returns
    :dict: object

    :param self: instance attribute of :class: 'WebCrawler' object
    :param url: a URL for the new :class: 'Request' object
    :param param: An arguments that :class: 'BeautifulSoup' takes
    """
    from bs4 import BeautifulSoup

    result = dict()
    select = BeautifulSoup(self.get_html(url).text).find('select', param)
    
    for option in select.find_all('option'):
      result.update({option.string:option.get('value')})

    if 'hofn' in param.values():
      result.update({u'Noregur' : u'163'})
      result.update({u'Færeyjar' : u'167'})

    return result

  def set_params(self, params):
    self.params = params

  def populate_queue(self, new_params):
    """ Adds items to a :class: 'Queue' object

    :param self: instance attribute of :class: 'WebCrawler' object
    :param new_params: the name of the variable GET parameter
    """

    for p in new_params:
      tmp_params = self.params.copy()
      tmp_params[self.param_name] = new_params[p]
      self.queue_in.put((self.get_html, tmp_params, {self.param_name:p}))

def main():
  base_url = 'http://www.fiskistofa.is/veidar/aflaupplysingar/'
  h_url = base_url + 'landanir-eftir-hofnum/landanir.jsp'
  s_url = base_url + 'afliallartegundir/aflastodulisti_okvb.jsp'
  
  h_queue_in = Queue.Queue()
  h_queue_out = Queue.Queue()
  s_queue_in = Queue.Queue()
  s_queue_out = Queue.Queue()

  h_params = (
      h_url, 
      h_queue_in,
      h_queue_out,
      'hofn',
      {'dagurFra':'01.01.2013', 'dagurTil':'10.01.2013', 'magn':'Sundurlidun'})
  s_params = (
      s_url,
      s_queue_in,
      s_queue_out,
      'p_fteg',
      {'p_fra':'01.01.2013', 'p_til':'10.01.2013'},
      False)

  h_thread = WebCrawler(*h_params)
  s_thread = WebCrawler(*s_params)
  h_thread.start()
  s_thread.start()

  while (not h_queue_in.empty()) and (not s_queue_in.empty()):
    pass

if __name__ == '__main__':
  main()

__author__      = 'Finnur Smári Torfason'
__copyright__   = 'Copyright 2012, www.aflafrettir.com'
__credits__     = ['Finnur Smári Torfason', 'Gísli Reynisson']

__license__     = 'GPL'
__version__     = '0.1'
__maintainer__  = 'Finnur Smári Torfason'
__email__       = 'finnurtorfa@gmail.com'
__status__      = 'Development'
