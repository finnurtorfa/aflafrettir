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

