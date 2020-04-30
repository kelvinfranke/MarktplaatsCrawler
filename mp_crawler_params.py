"""
Have you read the README.md? :-)
You may change these parameters to your liking!

"""


### Proxy parameters
PROXY = None                                                    # Allows a custom proxy; keep as 'None' to automatically find a proxy instead.
FORCE_CUSTOM_PROXY = False                                      # If True, automatic proxy finding is disabled; the program will simply quit if the custom proxy does not work.
PROXY_CHECK_URL = 'https://www.marktplaats.nl'                  # URL for checking proxy validity; use the root of the website you're going to crawl.
PROXY_MAX_RETRIES = 20                                          # Maximum number of attempts for automatically finding a proxy; irrelevant if you force-use a custom proxy (`float('inf')` is allowed but not recommended).
HTTP_GET_MAX_RETRIES = 10                                       # Maximum number of attempts to ensure a valid GET response (`float('inf')` is allowed but not recommended).


### Database parameters
DATABASE_NAME = 'marktplaats.db'                                # Name of the database file that will be created.
# NOTE: if you wish to use different data or a different database, feel free to write your own `Database` object which implements the same methods.


### Search parameters
## Possible values:
# query                         <String> used for search (may contain spaces); None is NOT allowed; empty string is.
# use_description               <Boolean> whether to use the ad description as well, or only check ad titles; None is allowed.
# cat1_id                       <Integer> determining main category (31 yields 'Audio, TV en Foto'); None is allowed.
# cat2_id                       <Integer> determining sub-category (495 yields 'Fotografie | Lenzen en Objectieven'); None is allowed.
# postcode                      <String> determining the location for distance measures; None is allowed.

QUERIES = [                                                     # List of queries, each a dictionary of search parameters for that query.
    {
        "query": "sony",
        "use_description": False,
        "cat1_id": 31,
        "cat2_id": 495,
        "postcode": "9711AA"
    },
    {
        "query": "m42",
        "use_description": True,
        "cat1_id": 31,
        "cat2_id": None,
        "postcode": "9711AA"
    },
    {
        "query": "minolta",
        "use_description": True,
        "cat1_id": 31,
        "cat2_id": None,
        "postcode": "9711AA"
    },
    {
        "query": "nikon",
        "use_description": False,
        "cat1_id": 31,
        "cat2_id": 495,
        "postcode": "9711AA"
    },
    {
        "query": "canon",
        "use_description": False,
        "cat1_id": 31,
        "cat2_id": 495,
        "postcode": "9711AA"
    }#,
    # {
    #     "query": "",
    #     "use_description": False,
    #     "cat1_id": 31,
    #     "cat2_id": None,
    #     "postcode": "9711AA"
    # }
]
