def split_csv():
    """
    This function reads in data from items.csv
    
    Returns a tuple containing Dataframes: (No NaN, NaN)
    Thus 'splitting' the csv
    This allows the NaN values to be 'preserved'
    and dealt with however the user would like
    
    Future implementation will allow multiple csv files
    In this implementation this module will be deprecated
    A new pipeline package will be implemented containing this file
    """
    
    import pandas as pd

    # Skip the header column,
    # Ignore the trailing comma w/each row
    # Enfore column name scheme
    
    stock = pd.read_csv("app/data/items.csv", 
                        skiprows=0, 
                        index_col=False,
                        usecols= ['item_id', 'item_group', 'cubic_volume_ft'])

    return  (stock.dropna(), stock.isna())

def deleteCSV():
    import os
    import glob

    files = glob.glob('app/data/tmp/*.csv')
    for f in files:
        os.remove(f)