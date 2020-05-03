# Marktplaats Crawler

Are you tired of scrolling through Marktplaats hoping to find that one gem that you think must be hidden somewhere around page 42, except it never is? Do you wish you could analyze the data of ads posted to Marktplaats? Whatever it is you wish, say no more.

`run_mp_crawler.py` is a script that, given the parameters and queries set in `mp_crawler_params.py`, crawls Marktplaats for the data and creates a database (currently a *pickled `Pandas` DataFrame*) of the ads/listings and their (meta)data. This script works in conjunction with Python library `free-proxy`, which allows it to run from a proxy. 

Most of the queries are fetched within seconds. However, given the occasionally poor quality of randomly assigned proxies, it may take a few minutes.

*If you have any questions, remarks, or additions, do not hesitate to let me know. Here's to hoping Marktplaats won't change their API structure too much...* 🤔

### Requirements*
```
Python:
  Python 3.6.8

Libraries:
  free-proxy==1.0.1
  grequests==0.6.0
  pandas==0.24.2
```
*\* Note that other Python and libary versions may work just as well.*


### Important and necessary remarks
Please note that I am not responsible nor liable for you using and/or running this code on any machine. Anything that results from this, be it a lawsuit due to improper use of APIs, your computer burning down, or your husband/wife leaving you, is the responsibility of the user and the user only. I hereby merely provide code that, in theory, functions.

Please also make sure -- if you *do* decide to run the code -- that it is permitted by your local law to crawl for such data. Again, determining whether or not this is the case is purely the responsibility of the user.

Finally, for the love of all that is holy, make sure you **limit your usage** . This should be common courtesy when crawling for data. Please be respectful towards Marktplaats for even allowing you to crawl for data using the API.


### Known issues

* The Marktplaats API will not yield more than 5,000 ads/listings from a query, even if there are supposedly more to be found.
* Bids on an ad/listing are not stored, since this data is not present in the currently used API calls.
