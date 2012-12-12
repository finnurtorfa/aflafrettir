Aflafrettir
=========

Aflafrettir is an API for fetching landing information from Fiskistofa(Directorate of Fisheries in Iceland).  

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

