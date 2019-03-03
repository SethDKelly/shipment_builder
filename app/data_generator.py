from app.clean import clean_csv()
import pandas as pd

def dataframe_generator():
    
    # Builds anywhere from 150-250 rows of data that matches what comes from items.csv
    # Creates random 'keys' that it merges with the stock data based on index
    # returns the data as pandas DataFrame
    
    import random
    
    return (pd.DataFrame(data = {'key': [random.randint(0,199) for x in range(random.randint(150,250))]})
              .merge(clean_csv(), 
                     left_on='key', 
                     right_index=True)
              .drop('key',
                    axis = 1)
              .reset_index(drop=True)
           )

def csv_generator():    
    # Builds anywhere from 150-250 rows of data that matches what comes from items.csv
    # Creates random 'keys' that it merges with the stock data based on index
    # returns the data as .csv's
    
    import random
    import glob
    import re
    
    count = sorted([int(re.sub("[^0-9]", "", files)) for files in glob.glob("app/data/tmp/*.csv")])[-1] + 1
    if not count: 
        count = '1'        
    
    return (pd.DataFrame(data = {'key': [random.randint(0,199) for x in range(random.randint(150,250))]})
              .merge(clean_csv(), 
                     left_on='key', 
                     right_index=True)
              .drop('key',
                    axis = 1)
              .reset_index(drop=True)
           ).to_csv("app/data/tmp/items"+str(count)+".csv", 
                    index=False)