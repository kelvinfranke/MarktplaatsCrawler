# Automatic Proxy Marktplaats Crawler

Are you tired of scrolling through Marktplaats hoping to find that one gem that you think must be hidden somewhere around page 42, except it never is? Do you wish you could analyze the data of ads posted to Marktplaats? Well, whatever it is you wish, say no more.

`run_mp_crawler.py` is a script that, given the parameters and queries set in `mp_crawler_params.py`, crawls Marktplaats for the data and creates a database (currently a *pickled `Pandas` DataFrame*) of the ads/listings and their (meta)data. Worry not about your IP getting blocked; this script will always run with a functional and free proxy. See for yourself!

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


### Known issues
* The Marktplaats API will never yield more than 5,000 ads/listings from a query, even if it claims there are more to be found.
* Bids are currently *not* stored, because the ads/listings do not directly contain this data.
