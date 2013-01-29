#!/usr/bin/python
# *-* encoding: utf-8 *-*

import Queue
from threading import Thread

class URLManager(object):
  def __init__(self, *args, **kwargs):
    (self.harbours, self.species) = self.init_params()

  def get_html(self, url, **kwargs):
    """ Sends a GET request, returns :class: 'Response' object

    :param url: a URL for the new :class: 'Request' object
    :param **kwargs: optional parameters that 'request' takes
    """
    import requests
    
    return requests.get(url, params=kwargs)

  def get_params(self, url, **kwargs):
    """ Passes :params: to :function: 'get_html', returns :dict: object

    :param url: a URL for the new :class: 'Request' object
    :param **kwargs: optional arguments that :class: 'BeautifulSoup' takes
    """
    from bs4 import BeautifulSoup

    result = dict()
    select = BeautifulSoup(self.get_html(url).text).find('select', kwargs)
    
    for option in select.find_all('option'):
      result.update({option.string:option.get('value')})

    if 'hofn' in kwargs.values():
      result.update({u'Noregur' : u'163'})
      result.update({u'Færeyjar' : u'167'})

    return result

  def init_params(self):
    """ Passes :params: to :function: 'get_params', returns :tuple: object:
    """
    base_url = 'http://www.fiskistofa.is/veidar/aflaupplysingar/'
    new_params = (
        (base_url + 'landanir-eftir-hofnum/', {'name':'hofn'}),
        (base_url + 'afliallartegundir', {'name':'p_fteg'})
        )
    
    result = ()

    for p in new_params:
      result = result + (self.get_params(p[0], **p[1]), )

    return result

  def populate_queue(self, params, queue):
    for p in params:
      queue.put({p:params[p]})


class URLManagerThread(Thread):
  def __init__(self, url_manager, param_name, queue):
    Thread.__init__(self)
    
    self.url_manager = url_manager
    self.param_name = param_name
    self.queue = queue

    self.daemon = True

  def run(self):
    while True:
      chunk = self.queue.get()
      self.queue.task_done()

def main():
  h_queue = Queue.Queue()
  s_queue = Queue.Queue()
  url_manager = URLManager()
  url_manager.populate_queue(url_manager.harbours, h_queue)
  url_manager.populate_queue(url_manager.species, s_queue)
  
  h_thread = URLManagerThread(url_manager, 'hofn', h_queue)
  s_thread = URLManagerThread(url_manager, 'p_fteg', s_queue)

  h_thread.start()
  s_thread.start()

  while (not h_queue.empty()) and (not s_queue.empty()):
    pass

  print "Done"


if __name__ == '__main__':
  main()
