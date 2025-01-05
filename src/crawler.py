import os, sys, time
import grequests                    # asynchronous GET

from json.decoder import JSONDecodeError
from fp.fp import FreeProxy         # https://pypi.org/project/free-proxy/

# Hide the warning about insecure requests; this crawler is too basic to bother with MitM attacks etc.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Hide `grequests 'UserWarning: libuv only supports millisecond timer resolution; [...]'
import warnings
warnings.simplefilter("ignore", category=UserWarning)



# class Crawler(object):

#     def __init__(self, proxy, max_proxy_retries, proxy_check_url, force_custom_proxy, max_get_retries):
#         self.proxy_check_url = proxy_check_url
#         self.max_get_retries = max_get_retries

#         # Set custom proxy.
#         if proxy is not None:
#             print("Using custom proxy: '%s'" % str(proxy))
#             self.__set_proxy(proxy)
#             # Check proxy validity.
#             if self.__is_proxy_ok(url=self.proxy_check_url):
#                 print("\n\033[92m✓\033[0m Proxy OK: %s" % str(proxy))
#             else:
#                 print("\033[93m✗\033[0m Custom proxy is not functional")
#                 if force_custom_proxy:
#                     self.stop("\033[91m✗\033[0m Custom proxy was forced, but does not work.")
#                 # Allow finding another proxy anyway.
#                 proxy = None

#         # Find and set a functional free proxy.
#         self.__find_free_proxy(max_proxy_retries)


#     # Sets a new proxy using `free-proxy`, only if one is found within `max_retries`.
#     def __find_free_proxy(self, max_retries):
#         assert max_retries > 0, "`max_retries` must be a non-negative integer."
#         invalid_count = 0
#         while invalid_count < max_retries:
#             print("\nLooking for a proxy (attempt %d/%d)..." % (invalid_count+1, max_retries))
#             proxy = FreeProxy(timeout=0.5, rand=True).get()
#             # Check whether free-proxy works.
#             if proxy is None:
#                 print("\033[93m✗\033[0m `free-proxy` could not find a proxy")
#                 invalid_count += 1
#                 continue
            
#             # A proxy was found, so use it.
#             print("A proxy was found: '%s'" % str(proxy))
#             self.__set_proxy(proxy)

#             # Check whether this proxy works for the given URL.
#             if not self.__is_proxy_ok(url=self.proxy_check_url):
#                 print("\033[93m✗\033[0m Proxy does not work")
#                 proxy = None
#                 invalid_count += 1
#             else:
#                 print("\n\033[92m✓\033[0m Proxy OK: %s" % str(proxy))
#                 return
        
#         # No functional proxy was found within `max_retries` :(
#         self.stop("\033[91m✗\033[0m None of the attempted %d proxies is functional.\n\nIs `free-proxy` working?" % max_retries)
    

#     # Sets proxies accordingly.
#     def __set_proxy(self, proxy):
#         self.proxy = proxy
#         self.proxies = {
#             "http": proxy,
#             "https": proxy
#         }


#     # Ensures that the supplied URL can be reached from the proxy.
#     def __is_proxy_ok(self, url):
#         print("Checking connection to %s..." % url)
#         return self.get(url).ok


#     # Stops the crawler.
#     def stop(self, err_msg=None):
#         print((err_msg if err_msg is not None else '') + "\nExiting...\n")
#         sys.exit(0)
    

#     # HTTP GET for single URL; returns the response.
#     def get(self, url, verify=False, timer=False):
#         # Start timing.
#         if timer:
#             t_start = time.time()
#         response = self.get_multiple(urls=[url], verify=verify, timer=False)[0]
#         return response if not timer else (response, time.time() - t_start)
    

#     # HTTP GET for multiple URLs; returns the responses.
#     def get_multiple(self, urls, verify=False, timer=False):
#         # Start timing.
#         if timer:
#             t_start = time.time()
        
#         # Allow retries in case of an invalid response.
#         invalid_count = 0
#         while invalid_count < self.max_get_retries:
#             # Get all responses.
#             async_responses = []
#             for url in urls:
#                 response = grequests.get(url, proxies=self.proxies, verify=False)
#                 async_responses.append(response)
#             responses = grequests.map(async_responses)

#             # Check validity.
#             if None in responses:
#                 invalid_count += 1
#                 time.sleep(.5)
#             else:
#                 break

#         return responses if not timer else (responses, time.time() - t_start)

class Crawler(object):
    def __init__(self, proxy=None, max_proxy_retries=0, proxy_check_url=None, force_custom_proxy=False, max_get_retries=3):
        self.proxy_check_url = proxy_check_url
        self.max_get_retries = max_get_retries
        
        # Initialize with no proxy
        self.proxy = None
        self.proxies = None

    def get(self, url, verify=False, timer=False):
        if timer:
            t_start = time.time()
        response = self.get_multiple(urls=[url], verify=verify, timer=False)[0]
        return response if not timer else (response, time.time() - t_start)

    def get_multiple(self, urls, verify=False, timer=False):
        if timer:
            t_start = time.time()
        
        invalid_count = 0
        while invalid_count < self.max_get_retries:
            # Get all responses without proxy
            async_responses = [grequests.get(url, verify=verify) for url in urls]
            responses = grequests.map(async_responses)

            # Check validity
            if None in responses:
                invalid_count += 1
                time.sleep(.5)
            else:
                break

        return responses if not timer else (responses, time.time() - t_start)

    def stop(self, err_msg=None):
        print((err_msg if err_msg is not None else '') + "\nExiting...\n")
        sys.exit(0)