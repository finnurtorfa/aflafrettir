Aflafrettir
=========

Aflafrettir is an API for fetching landing information from Fiskistofa(Directorate of Fisheries in Iceland).  

Preparation
---------

To clone the repository:

        git clone https://github.com/finnurtorfa/aflafrettir.git

To start working on the code it is a good idea to have *virtualenv* and *virtualenvwrapper* installed. To create a virtualenvironment issue the following call in terminal:

        mkvirtualenv aflafrettir

To work on the aflafrettir virtual environment issue a call:

        workon aflafrettir

And to leave the virtual environment call:
      
        deactivate

To be able to run the code with python it is necessary to install some 3rd party libraries. It is a good idea to use *pip* for that. To install the dependencies only for the aflafrettir virtual environment issue the following call while working on that particular environment:
        
        workon aflafrettir
        pip install -r requirements.txt

Unfortunately wxPython can not be installed via *pip*, so to get wxPython to work with the virtual environment install wxpython. On my system I do, as a root:
    
        pacman -S wxpython

Then go to your $VIRTUAL\_ENV/aflafrettir/lib/python2.7/site-packages/ folder and make the following symlinks:

        ln -s /usr/lib/python2.7/site-packages/wxversion.py wxversion.py
        ln -s /usr/lib/python2.7/site-packages/wxPython_common-2.8.12.1-py2.7.egg-info wxPython_common-2.8.12.1-py2.7.egg-info
        ln -s /usr/lib/python2.7/site-packages/wx.pth wx.pth
        ln -s /usr/lib/python2.7/site-packages/wx-2.8-gtk2-unicode wx-2.8-gtk2-unicode

Depending on your system and version python and wxPython the symlinks could vary.

Class: DOF\_URLGenerator.py
---------

*  The DOF\_URLGenerator class is used by the Aflafrettir API, a web scraping API. The API is used to gather information on landings from the website of Directorate of Fisheries in Iceland.

*  The DOF\_URLGenerator class is initialized with a base\_url, query\_params, new\_param and an optional parameter called species, as described by the \_\_init\_\_ docstring. It returns a dictionary with a URL that can be used to query the database of the website of Directorate of Fisheries in Iceland in a desired way.

*  Example use of the class:
        
        # Initialization parameters
        base_url ='http://www.fiskistofa.is/veidar/aflaupplysingar/landanir-eftir-hofnum/landanir.jsp?'
        query_param = {'magn':'Samantekt','dagurFra':'01.01.2012,'dagurTil':'02.02.2012'}
        new_param = 'hofn'

        urls = DOF_URLGenerator(base_url, query_params, new_param)

        # Iterate over the DOF_URLGenerator object to get the query_urls
        for u in urls:
          print u

Class: QueryURL
---------

*  The QueryURL class is used by the Aflafrettir API, a web scraping API. The API is used to gather information on landings from the website of Directorate of Fisheries in Iceland.

*  The QueryURL class is initialized with a url\_list and returns a html document corresponding to each of the url's in the url\_list.

*  Example use of the class:

        # Initialization parameters
        url = {
        'url':'www.fiskistofa.is',
        'url1':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?'
        }
        
        html = QueryURL(url)
        for i in html:
          print i


Class: ParseHTML
---------

*  The ParseHTML class is used by the Aflafrettir API, a web scraping API. The API is used to gather information on landings from the website of Directorate of Fisheries in Iceland.

*  The ParseHTML class is initialized with a html\_dict, tbl\_row\_no, fields, field\_range, as described by the \_\_init\_\_ docstring. It returns a dictionary with all the values of the html page that was given as a input.

*  Example use of the class:
        
        # Initialization parameters
        url = {'url':'http://www.fiskistofa.is/veidar/aflaupplysingar/afliallartegundir/aflastodulisti_okvb.jsp?p_fteg=Ýsa+2&p_fra=01.12.2012&p_til=22.12.2012'}
          
          html = QueryURL(url)
          for h in html:
            info = ParseHTML(h, [1, 2], ['ShipID', 'Name', 'Gear', 'Catch'], range(0,4))
            for i in info:
              print i
*  The ParseHTML class takes in a dictionary containing a HTML content and an error code. The error code states whether or not the HTML content had been retrieved. An object of the class can be made like so:

        info = ParseHTML(html_cont)

*  And then it is possible to iterate over the info like so:

        for i in info:
          print i

TotalCatch
---------

*  The TotalCatch takes in a list of landings, and calculates the total catch for each unique ShipID.
        
        total_catch = TotalCatch(landingList)

*  Then it is possible to iterate over the total\_catch like so:

        for c in total_catch:
          print c

GroupLandingInfo
---------

*  The GroupLandingInfo takes in a list of dictionaries containing the landing info and groups all the landings by gear.

        groups = GroupLandingInfo(landingList)

*  Then it is possible to iterate over the groups like so:
        
        for g in groups:
          print g

ExcelListOutput
---------

*  The ExcelListOutput takes in a landing list and can output the said list in an Excel format.

        excel = ExcelListOutput(landingList)

*  The class method save\_excel() takes care of the operation of putting the list in excel format and can be called like this:

        excel.save_excel()
