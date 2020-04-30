import time

from src.crawler import Crawler


class MarktplaatsCrawler(Crawler):
    
    def __init__(self, proxy, max_proxy_retries, proxy_check_url, force_custom_proxy, max_get_retries):
        # Initialize base Crawler
        super().__init__(proxy, max_proxy_retries, proxy_check_url, force_custom_proxy, max_get_retries)
    

    # Update the query to be used
    def set_query(self, query):
        self.query = query


    # Does the API calls to Marktplaats and returns the product data
    def crawl_listings(self, query, use_description, postcode, cat1_id, cat2_id, items_per_call=100, offset=0, repeat_delay=0.1, verbose=False):
        all_listings = []
        
        ### Asynchronous
        all_json_data = []

        # Query for the first listings
        url = self.__compose_url(
            query=query,
            use_description=use_description,
            postcode=postcode,
            cat1_id=cat1_id,
            cat2_id=cat2_id,
            limit=items_per_call,
            offset=offset
        )

        # Get the first JSON object
        #if verbose:
        #    print("\nAPI call: '%s'\nGetting listings %d-%d..." % (url, offset, offset + items_per_call))
        response, delta_t = self.get(url, timer=True)
        if response is None:
            if verbose:
                print("\033[91m✗\033[0m ERROR: Could not fetch JSON data (%.1fs)" % delta_t)
            return None
        json_data = response.json()
        all_json_data.append(json_data)

        # Determine the total number of listings for the query
        num_listings = self.get_num_listings(json_data)
        if verbose:
            print("\033[92m✓\033[0m (%.1fs)\n\n%s yields %d listings" % (delta_t, (str("'%s'" % query) if query != '' else '<no query>'), num_listings))
        
        # Create URLs with calculated 'limit' and 'offset'
        urls = [self.__compose_url(
            query=query,
            use_description=use_description,
            postcode=postcode,
            cat1_id=cat1_id,
            cat2_id=cat2_id,
            limit=items_per_call,
            offset=i
            ) for i in range(offset + items_per_call, num_listings, items_per_call)
        ]

        # Get the following async responses
        if len(urls) > 0:
            if verbose:
                print("\nGetting listings %d-%d..." % (items_per_call, num_listings))
            responses, delta_t = self.get_multiple(urls, timer=True)
            
            # Check for invalid responses
            if None in responses:
                # Some of the responses are invalid; remove those
                responses = [r for r in responses if r is not None]
                if len(responses) > 0:
                    if verbose:
                        print("\033[93m✗\033[0m Warning: not all listings are valid; keeping a subset (%.1fs)" % delta_t)
                else:
                    return None
            
            if verbose:
                print("\033[92m✓\033[0m (%.1fs)" % delta_t)
            all_json_data.extend([r.json() for r in responses])
        
        # Get listings from JSON data
        for json_data in all_json_data:
            all_listings.extend(json_data['listings'])

        return all_listings


    # Given JSON output of an API call, returns the total number of listings for the used query
    def get_num_listings(self, json_data):
        try:
            return int(json_data['facets'][1]['categories'][1]['histogramCount'])
        except (IndexError, TypeError, AttributeError, ValueError):
            # The JSON data does not contain an integer at the expected location
            return None


    # # Given Marktplaats parameters, returns the output of an API call
    # def get_json(self, query, use_description, postcode, cat1_id, cat2_id, limit, offset, verbose):
    #     url = self.__compose_url(query, use_description, postcode, cat1_id, cat2_id, limit, offset, verbose)
    #     return self.get(url).json()


    # Given Marktplaats parameters, returns the corresponding API URL
    def __compose_url(self, query, use_description, postcode, cat1_id, cat2_id, limit, offset, verbose=False):
        # NOTE: `limit` maximum is 100; default is 30.
        url = 'https://www.marktplaats.nl/lrp/api/search?%s%slimit=%d&offset=%d%s%s%s' % (
            'l1CategoryId=%d&' % cat1_id if cat1_id is not None else '',
            'l2CategoryId=%d&' % cat2_id if cat2_id is not None else '',
            limit,
            offset,
            '&postcode=%s' % postcode if postcode is not None else '',
            '&searchInTitleAndDescription=%s' % str(use_description).lower() if (query != '' and use_description is not None) else '',
            '&query=%s' % query.replace(' ', '+') if query != '' else ''
            )
        if verbose:
            print(url)
        return url
