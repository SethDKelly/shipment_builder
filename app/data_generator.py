def data_generator():
    
    # Builds anywhere from 150-250 rows of data that matches what comes from items.csv
    # Creates random 'keys' that it merges with the stock data based on index
    # returns the data as... pandas DataFrame
    
    import random
    import pandas as pd
    
    return (pd.DataFrame(data = {'key': [random.randint(0,199) for x in range(random.randint(150,250))]})
              .merge(clean_csv(), 
                     left_on='key', 
                     right_index=True)
              .drop('key',
                    axis = 1)
              .reset_index(drop=True)
           )

'''
Future implmentations will return this as .csv data that will be required to be loaded in
"app/data/tmp/<DataName>.csv"

To do this data_generator will take an integer parameter
Create csv's from the integer, 3 will make 3 .csv files
check what the name is and build the names dynamically by what's already stored
'''