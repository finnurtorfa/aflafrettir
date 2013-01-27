#!/usr/bin/python
# *-* encoding: utf-8 *-*

class URLManager(object):
  def __init__(self, *args, **kwargs):
    pass

  def get_html(self, url, **kwargs):
    """ Sends a GET request, returns :class: 'Response' object

    :param url: a URL for the new :class: 'Request' object
    :param **kwargs: optional parameters that 'request' takes
    """
    import requests
    
    return requests.get(url, params=kwargs)

  def get_params(self, url, **kwargs):
    """ Sends a GET request, returns :dict: object

    :param url: a URL for the new :class: 'Request' object
    :param **kwargs: optional arguments that :class:  takes
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

def main():
  url_manager = URLManager()
  new_param = {'name':'hofn'}
  new_param2 = {'name':'p_fteg'}
  print url_manager.get_params('http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/', **new_param)
  print url_manager.get_params('http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/', **new_param2)

if __name__ == '__main__':
  main()
