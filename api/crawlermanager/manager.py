#!/usr/bin/python
# *-* encoding: utf-8 *-*

import Queue

from threading import Thread

class WebCrawler(object):
  def __init__(self, **kwargs):
    self.h_url = kwargs['h_url']
    self.s_url = kwargs['s_url']
    
    (self.harbours, self.species) = self.fetch_get_params()

    self.h_url += 'landanir.jsp'
    self.s_url += 'aflastodulisti_okvb.jsp'

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

  def fetch_get_params(self):
    """ Passes :params: to :function: 'get_params', returns :tuple: object:
    
    :param self: instance attribute of :class: 'WebCrawler' object
    """
    new_params = (
        (self.h_url, {'name':'hofn'}),
        (self.s_url, {'name':'p_fteg'})
        )
    
    result = ()

    for p in new_params:
      result = result + (self.get_params(p[0], p[1]), )

    return result

  def set_get_params(self, h_params, s_params):
    """ Sets the GET params for querying the website of Directorate of
    Fisheries(DOF) in Iceland.

    :param self: instance attribute of :class: 'WebCrawler' object
    :param h_params: GET parameters for harbours
    :param s_params: GET parameters for species
    """
    self.h_params = h_params
    self.s_params = s_params

  def populate_queue(self, param_name, queue, harbour=True):
    """ Adds items to a :class: 'Queue' object

    :param self: instance attribute of :class: 'WebCrawler' object
    :param param_name: the name of the variable GET parameter
    :param queue: a :class: 'Queue' object that items are added to
    :param harbour: a boolean value to distinguish between harbours and species
    """
    if harbour:
      p_dict = self.h_dict
      p_url = self.h_url
      params = self.harbours
    else:
      p_dict = self.s_dict
      p_url = self.s_url
      params = self.species

    for p in params:
      tmp_dict = p_dict.copy()
      tmp_dict.update({param_name:params[p]})
      queue.put((self.get_html, p_url, tmp_dict, p, harbour))

class WebCrawlerThread(Thread):
  def __init__(self, crawler, param_name, queue):
    Thread.__init__(self)
    
    self.crawler = crawler
    self.param_name = param_name
    self.queue = queue

    self.daemon = True

  def run(self):
    while True:
      get_params_cb = self.queue.get()
      resp = get_params_cb[0](get_params_cb[1], **get_params_cb[2])
      print resp.url, resp

      self.queue.task_done()

def main():
  base_url = 'http://www.fiskistofa.is/veidar/aflaupplysingar/'
  h_url = base_url + 'landanir-eftir-hofnum/'
  s_url = base_url + 'afliallartegundir/'
  url_dict = {'h_url':h_url, 's_url':s_url}
  url_params = (
      {'dagurFra':'01.01.2013', 'dagurTil':'10.01.2013', 'magn':'Sundurlidun'}, 
      {'p_fra':'01.01.2013', 'p_til':'10.01.2013'}
      )
  h_queue = Queue.Queue()
  s_queue = Queue.Queue()
  crawler = WebCrawler(**url_dict)
  crawler.set_get_params(*url_params)
  crawler.populate_queue('hofn', h_queue)
  crawler.populate_queue('p_fteg', s_queue, False)

  h_thread = WebCrawlerThread(crawler, 'hofn', h_queue)
  s_thread = WebCrawlerThread(crawler, 'p_fteg', s_queue)

  h_thread.start()
  s_thread.start()

  while (not h_queue.empty()) and (not s_queue.empty()):
    pass

if __name__ == '__main__':
  main()
