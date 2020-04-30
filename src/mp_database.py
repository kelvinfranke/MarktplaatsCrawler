import os
import pandas as pd


"""
    For now, the database is a pickled Pandas dataframe where each row contains
    a product and its (meta)data.

"""


class Database(object):

    def __init__(self, save_path='marktplaats.db'):
        # TODO: load existing dataframe
        self.__save_path = save_path
        if os.path.exists(save_path):
            self.__load_dataframe_from_db()
        else:
            self.__df = None
    

    # Save the DataFrame, pickled.
    def __save_dataframe_to_db(self):
        self.__df.to_pickle(self.__save_path)


    # Load a pickled DataFrame.
    def __load_dataframe_from_db(self):
        self.__df = pd.read_pickle(self.__save_path)


    # Returns the Pandas DataFrame.
    def get_dataframe(self):
        return self.__df


    # Takes a list of Marktplaats listings, and stores this in the database.
    def add_listings(self, listings, fetch_time):
        # Can't do anything if the input is erroneous.
        if listings is None:
            return

        data = self.__listings_to_dict(listings, fetch_time)
        new_df = pd.DataFrame(data)

        if self.__df is None:
            # No DataFrame? Use the newly obtained one.
            self.__df = new_df
        else:
            # DataFrame exists? Concatenate but remove duplicates where product ID and fetch time is the same.
            # This keeps multiples of one product ID only if the fetch time differs;
            # This is valuable information since it means the product ad is still online after some time.
            self.__df = pd.concat([self.__df, new_df], sort=False)
            self.__df = self.__df.drop_duplicates(subset=['product_id', 'datetime_fetched'])

        # Update the pickled DataFrame file
        self.__save_dataframe_to_db()
    

    # Takes a list of Marktplaats listings, and returns a dictionary representation thereof.
    def __listings_to_dict(self, listings, fetch_time):
        # Define initial dictionary keys (more are later dynamically created as needed)
        keys = [
            'product_id',
            'product_name',
            'product_description',
            'category',
            'price_type',
            'price',
            'price_readable',
            'seller_id',
            'seller_name',
            'location_name',
            'location_distance_m',
            'priority_product',
            'urgency_feature_active',
            'nap_available',
            'datetime_created',
            'datetime_fetched',
            'href'
            ]
        data = {key: [] for key in keys}

        # Fill dictionary keys
        for i, listing in enumerate(listings):
            data['product_id'].append(listing['itemId'])
            data['product_name'].append(listing['title'])
            data['product_description'].append(listing['description'])
            data['category'].append(listing['categoryId'])
            data['price_type'].append(listing['priceInfo']['priceType'])
            data['price'].append(float(listing['priceInfo']['priceCents'])/100)
            data['price_readable'].append('€%.2f' % (float(listing['priceInfo']['priceCents'])/100))
            data['seller_id'].append(listing['sellerInformation']['sellerId'])
            data['seller_name'].append(listing['sellerInformation']['sellerName'])
            data['location_name'].append(listing['location']['cityName'] if 'cityName' in listing['location'] else None)
            data['location_distance_m'].append(listing['location']['distanceMeters'])
            data['priority_product'].append(listing['priorityProduct'])
            data['urgency_feature_active'].append(listing['urgencyFeatureActive'])
            data['nap_available'].append(listing['napAvailable'])
            data['datetime_created'].append(listing['date']) # Format: time.strftime('%Y-%m-%dT%H:%M:%SZ')
            data['datetime_fetched'].append(fetch_time)
            data['href'].append('http://www.marktplaats.nl/' + listing['vipUrl'])

            # Damnit Marktplaats, why did you have to create a list of dicts like:
            #   [{'key': 'condition', 'value': 'Zo goed als nieuw'}, {'key': 'delivery', ...}]
            # if you could've just done:
            #   {'condition': 'Zo goed als nieuw', 'delivery': ...}
            # :-(

            # Refactor 'attributes' because of Marktplaats' poor programming
            if 'attributes' in listing.keys():
                attributes = {attribute['key']: attribute['value'] for attribute in listing['attributes']}
                for key in attributes.keys():
                    # Modify key name
                    key_name = 'attribute_' + key
                    # Ensure the key exists
                    if key_name not in data.keys():
                        # Key did not exist; fill with `None` for previous listings
                        data[key_name] = [None] * (i - 1)
                        # add key and fill with [None] * i
                    data[key_name].append(attributes[key])
            
            # Ensure all keys have some value
            # NOTE: not the most efficient, to loop over keys again to check whether we missed something. ¯\_(ツ)_/¯
            for key in data.keys():
                if len(data[key]) == i: # length of a filled key list should be `i + 1`, since `i` starts at 0
                    # Fill in a None because we don't have a value for this key yet
                    data[key].append(None)

        return data
