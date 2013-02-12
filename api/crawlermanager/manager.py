#!/usr/bin/python
# *-* encoding: utf-8 *-*

import Queue

from threading import Thread

class WebCrawler(Thread):
  def __init__(self, url, queue, param_name, params, harbour=True):
    """ Initializes the :class: 'WebCrawle' object.

    :param self: instance attribute of :class: 'WebCrawler' object
    :param url: a URL used by various methods
    :param queue: a :class: 'Queue' object
    :param param_name: the name of the variable GET parameters
    :param params: the variable GET parameters
    :param harbour: a boolean value to indicate whether the :class:
                    'WebCrawler' object is querying the DOF database for
                    harbours or species.
    """
    Thread.__init__(self)
    
    self.url = url
    self.queue = queue
    self.param_name = param_name
    self.params = params
    
    self.new_params = self.get_params(url, {'name':param_name})
    self.populate_queue(self.new_params)

    self.daemon = True

  def run(self):
    while True:
      get_html_cb = self.queue.get()
      resp = get_html_cb[0](self.url, **get_html_cb[1])
      print resp.url, resp

      self.queue.task_done()

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

  def populate_queue(self, new_params):
    """ Adds items to a :class: 'Queue' object

    :param self: instance attribute of :class: 'WebCrawler' object
    :param new_params: the name of the variable GET parameter
    """

    for p in new_params:
      tmp_params = self.params.copy()
      tmp_params[self.param_name] = new_params[p]
      self.queue.put((self.get_html, tmp_params))

def main():
  base_url = 'http://www.fiskistofa.is/veidar/aflaupplysingar/'
  h_url = base_url + 'landanir-eftir-hofnum/landanir.jsp'
  s_url = base_url + 'afliallartegundir/aflastodulisti_okvb.jsp'
  
  h_queue = Queue.Queue()
  s_queue = Queue.Queue()

  h_params = (
      h_url, 
      h_queue,
      'hofn',
      {'dagurFra':'01.01.2013', 'dagurTil':'10.01.2013', 'magn':'Sundurlidun'})
  s_params = (
      s_url,
      s_queue,
      'p_fteg',
      {'p_fra':'01.01.2013', 'p_til':'10.01.2013'},
      False)

  h_thread = WebCrawler(*h_params)
  s_thread = WebCrawler(*s_params)
  h_thread.start()
  s_thread.start()

  while (not h_queue.empty()) and (not s_queue.empty()):
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
