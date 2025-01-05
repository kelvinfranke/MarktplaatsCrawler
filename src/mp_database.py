import os
import sqlite3
from datetime import datetime
import pandas as pd

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.__create_tables()

    def __create_tables(self):
        """Create the necessary tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Create the main listings table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            product_name TEXT,
            product_description TEXT,
            category TEXT,
            price_type TEXT,
            price REAL,
            price_readable TEXT,
            seller_id TEXT,
            seller_name TEXT,
            location_name TEXT,
            location_distance_m INTEGER,
            priority_product BOOLEAN,
            urgency_feature_active BOOLEAN,
            nap_available BOOLEAN,
            datetime_created TEXT,
            datetime_fetched TEXT,
            href TEXT,
            UNIQUE(product_id, datetime_fetched)
        )''')

        # Create a separate table for dynamic attributes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS listing_attributes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            listing_id INTEGER,
            attribute_key TEXT,
            attribute_value TEXT,
            FOREIGN KEY(listing_id) REFERENCES listings(id),
            UNIQUE(listing_id, attribute_key)
        )''')

        self.conn.commit()

    def add_listings(self, listings, fetch_time):
        if listings is None:
            return

        cursor = self.conn.cursor()

        for listing in listings:
            # Prepare main listing data
            listing_data = {
                'product_id': listing['itemId'],
                'product_name': listing['title'],
                'product_description': listing['description'],
                'category': listing['categoryId'],
                'price_type': listing['priceInfo']['priceType'],
                'price': float(listing['priceInfo']['priceCents'])/100,
                'price_readable': '€%.2f' % (float(listing['priceInfo']['priceCents'])/100),
                'seller_id': listing['sellerInformation']['sellerId'],
                'seller_name': listing['sellerInformation']['sellerName'],
                'location_name': listing['location'].get('cityName'),
                'location_distance_m': listing['location']['distanceMeters'],
                'priority_product': listing['priorityProduct'],
                'urgency_feature_active': listing['urgencyFeatureActive'],
                'nap_available': listing['napAvailable'],
                'datetime_created': listing['date'],
                'datetime_fetched': fetch_time,
                'href': 'http://www.marktplaats.nl/' + listing['vipUrl']
            }

            # Insert main listing data
            try:
                cursor.execute('''
                INSERT INTO listings (
                    product_id, product_name, product_description, category,
                    price_type, price, price_readable, seller_id, seller_name,
                    location_name, location_distance_m, priority_product,
                    urgency_feature_active, nap_available, datetime_created,
                    datetime_fetched, href
                ) VALUES (
                    :product_id, :product_name, :product_description, :category,
                    :price_type, :price, :price_readable, :seller_id, :seller_name,
                    :location_name, :location_distance_m, :priority_product,
                    :urgency_feature_active, :nap_available, :datetime_created,
                    :datetime_fetched, :href
                )''', listing_data)
                
                # Get the ID of the inserted listing
                listing_id = cursor.lastrowid

                # Handle attributes if they exist
                if 'attributes' in listing:
                    for attr in listing['attributes']:
                        cursor.execute('''
                        INSERT OR REPLACE INTO listing_attributes (listing_id, attribute_key, attribute_value)
                        VALUES (?, ?, ?)
                        ''', (listing_id, attr['key'], attr['value']))

            except sqlite3.IntegrityError:
                # Skip if this product_id and datetime_fetched combination already exists
                continue

        self.conn.commit()

    def get_dataframe(self, query=None):
        """
        Get data as a pandas DataFrame
        If query is None, returns all listings
        Otherwise executes the provided SQL query
        """
        if query is None:
            query = '''
            SELECT l.*, GROUP_CONCAT(a.attribute_key || ': ' || a.attribute_value) as attributes
            FROM listings l
            LEFT JOIN listing_attributes a ON l.id = a.listing_id
            GROUP BY l.id
            '''
        
        return pd.read_sql_query(query, self.conn)

    def execute_query(self, query, parameters=None):
        """Execute a custom SQL query"""
        cursor = self.conn.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        """Ensure database connection is closed when object is deleted"""
        if hasattr(self, 'conn'):
            self.conn.close()