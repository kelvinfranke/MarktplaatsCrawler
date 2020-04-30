import json, time
from src.mp_crawler import MarktplaatsCrawler
from src.mp_database import Database

from mp_crawler_params import *


if __name__ == '__main__':
    t_start = time.time()
    print("\nStarting crawler on <%s>" % time.asctime())

    # Initiate the crawler by finding a working proxy.
    crawler = MarktplaatsCrawler(PROXY, max_proxy_retries=PROXY_MAX_RETRIES, proxy_check_url=PROXY_CHECK_URL, force_custom_proxy=FORCE_CUSTOM_PROXY, max_get_retries=HTTP_GET_MAX_RETRIES)

    # Initiate the database.
    db = Database(DATABASE_NAME)

    # Crawl all queries.
    t_formatted = time.strftime('%Y-%m-%dT%H:%M:%SZ')

    for q in QUERIES:
        query = q['query']
        use_description = q['use_description']
        cat1_id = q['cat1_id']
        cat2_id = q['cat2_id']
        postcode = q['postcode']

        print("\n\nChecking query: '%s'..." % (query if query != '' else '<no query>'))

        # With the proxy, we can start crawling Marktplaats.
        listings = crawler.crawl_listings(query, use_description, postcode, cat1_id, cat2_id, verbose=True)

        # Did we fetch all listings, or only a subset (e.g. the apparent maximum of 5000)?
        if listings is not None:
            print("______________________\n\nNumber of listings obtained from this query: %d\n______________________" % len(listings))
        else:
            print("\n\033[91mNo listings this time\033[0m")


        # Let's add the listings we've obtained to our database.
        db.add_listings(listings, t_formatted)
    
    # My job here is done!
    print("\nDone on <%s>" % time.asctime())
    print("Script ran for %.2f minutes in total" % ((time.time() - t_start)/60))
    print("\n==========================\n")
