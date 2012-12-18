Aflafrettir
=========

Aflafrettir is an API for fetching landing information from Fiskistofa(Directorate of Fisheries in Iceland).  

Preparation
---------

To clone the repository:

        git clone https://github.com/finnurtorfa/aflafrettir.git

To start working on the code it is a good idea to have *virtualenv* and *virtualenvwrapper* installed. Then do

        mkvirtualenv aflafrettir

To work on the aflafrettir virtual environment issue a call

        workon aflafrettir

And to leave the virtual environment call
      
        deactivate

To be able to run the code with python it is necessary to install the dependencies. It is a good idea to use *pip* for that. To install the dependencies only for the aflafrettir virtual environment issue the following call while working on that particular environment

        pip install -r requirements.txt

To get wxPython to work with the virtual environment install wxpython as a regular user. On my system I do:
    
        pacman -S wxpython

Then go to your $VIRTUAL\_ENV/aflafrettir/lib/python2.7/site-packages/ folder and make the following symlinks:

        ln -s /usr/lib/python2.7/site-packages/wxversion.py wxversion.py
        ln -s /usr/lib/python2.7/site-packages/wxPython_common-2.8.12.1-py2.7.egg-info wxPython_common-2.8.12.1-py2.7.egg-info
        ln -s /usr/lib/python2.7/site-packages/wx.pth wx.pth
        ln -s /usr/lib/python2.7/site-packages/wx-2.8-gtk2-unicode wx-2.8-gtk2-unicode

Depending on your system and version python and wxPython the symlinks could vary.

LandingURL
---------

*  The LandingURL class takes in a list with 2 date objects, and can be created with:
        
        query_urls = LandingURL([date1, date2]) # date format: dd.mm.yyyy

*  Now it is possible to iterate over the query\_urls objects like so

        for i in query_urls:
          print i

QueryLandingURL
---------

*  The QueryLandingURL class takes in a dictionary of URL's and fetches the HTML of the url.

        html_responses = QueryLandingURL({'url':'www.example.com'})

* Now it is possible to to iterate over the html\_responses like so:

        for i in html_responses:
          print i

ParseHTML
---------

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
