from app.models.clean import clean_csv
import pandas as pd
from re import sub
from random import randint

def dfTestData():
    
    # Builds anywhere from 150-250 rows of data that matches what comes from items.csv
    # Creates random 'keys' that it merges with the stock data based on index
    # returns the data as pandas DataFrame
        
    return (pd.DataFrame(data = {'key': [random.randint(0,199) for x in range(random.randint(150,250))]})
              .merge(clean_csv(), 
                     left_on='key', 
                     right_index=True)
              .drop('key',
                    axis = 1)
              .reset_index(drop=True)
           )

def csvTestData():    
    # Builds anywhere from 150-250 rows of data that matches what comes from items.csv
    # Creates random 'keys' that it merges with the stock data based on index
    # returns the data as .csv's
    
    import random
    import glob
    import re
    
    # Checks to make sure there are no files
    # If there are no files, file name should start with 1
    if not sorted([int(re.sub("[^0-9]", "", files)) for files in glob.glob("app/data/tmp/*.csv")]):
        count = '1'
    else : # Start naming at whatever we're at +1
        count = sorted([int(re.sub("[^0-9]", "", files)) for files in glob.glob("app/data/tmp/*.csv")])[-1] + 1

    return (pd.DataFrame(data = {'key': [random.randint(0,199) for x in range(random.randint(150,250))]})
              .merge(clean_csv(), 
                     left_on='key', 
                     right_index=True)
              .drop('key',
                    axis = 1)
              .reset_index(drop=True)
           ).to_csv("app/data/tmp/items"+str(count)+".csv", 
                    index=False)

def shipment_id():
    """
    Generates an interger shipment id based on datetime
    Year Month Day Hour Minute Seconds Milleseconds
    """
    
    import datetime
    
    return int(sub("[^0-9]", "", str(datetime.datetime.today()))[:17])