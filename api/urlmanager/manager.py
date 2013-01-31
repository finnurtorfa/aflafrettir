#!/usr/bin/python
# *-* encoding: utf-8 *-*

import Queue
from threading import Thread

class WebCrawler(object):
  def __init__(self, **kwargs):
    self.base_url = 'http://www.fiskistofa.is/veidar/aflaupplysingar/'
    self.h_url = self.base_url + 'landanir-eftir-hofnum/'
    self.s_url = self.base_url + 'afliallartegundir/'
    
    (self.harbours, self.species) = self.fetch_get_params()

    self.h_url += 'landanir.jsp'
    self.s_url += 'aflastodulisti_okvb.jsp'
    self.h_dict = kwargs['harbour']
    self.s_dict = kwargs['species']

  def get_html(self, url, **kwargs):
    """ Sends a GET request, returns :class: 'Response' object

    :param url: a URL for the new :class: 'Request' object
    :param **kwargs: optional parameters that 'request' takes
    """
    import requests
    
    return requests.get(url, params=kwargs)

  def get_params(self, url, param):
    """ Passes :params: 'url' and 'param' to :function: 'get_html', returns
    :dict: object

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
    """
    new_params = (
        (self.h_url, {'name':'hofn'}),
        (self.s_url, {'name':'p_fteg'})
        )
    
    result = ()

    for p in new_params:
      result = result + (self.get_params(p[0], p[1]), )

    return result

  def populate_queue(self, param_name, queue, harbour=True):
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
      queue.put((self.get_html, p_url, p, tmp_dict))

class WebCrawlerThread(Thread):
  def __init__(self, crawler, param_name, queue):
    Thread.__init__(self)
    
    self.crawler = crawler
    self.param_name = param_name
    self.queue = queue

    self.daemon = True

  def run(self):
    while True:
      chunk = self.queue.get()
      resp = chunk[0](chunk[1], **chunk[3])

      self.queue.task_done()

def main():
  args = {
      'harbour':{'dagurFra':'01.01.2013', 'dagurTil':'10.01.2013', 'magn':'Sundurlidun'}, 
      'species':{'p_fra':'01.01.2013', 'p_til':'10.01.2013'}
      }
  h_queue = Queue.Queue()
  s_queue = Queue.Queue()
  crawler = WebCrawler(**args)
  crawler.populate_queue('hofn', h_queue)
  crawler.populate_queue('p_fteg', s_queue, False)
  
  h_thread = WebCrawlerThread(crawler, 'hofn', h_queue)
  s_thread = WebCrawlerThread(crawler, 'p_fteg', s_queue)

  h_thread.start()
  s_thread.start()

  while (not h_queue.empty()) and (not s_queue.empty()):
    pass

  print "Done"

if __name__ == '__main__':
  main()
