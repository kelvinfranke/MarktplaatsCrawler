from mp_crawler_params import *
from src.mp_database import Database

if __name__ == '__main__':
    db = Database(DATABASE_NAME)
    print(db.get_dataframe())