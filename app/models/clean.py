def clean_csv():
    import pandas as pd

    stock = pd.read_csv("app/data/items.csv")

    # Isolate the data to only the three necessary columns:
        # 'item_id', 'item_group', 'cubic_volume_ft'
    # Drop any NaN rows from the data
    # Sort the values based on Cubic volume
        # Will sort smallest to largest
    # Reset the index due to shuffling from sorting
  
    return  (stock.loc[:,['item_id', 'item_group', 'cubic_volume_ft']]
                  .dropna()
                  .sort_values("cubic_volume_ft",
                               ascending=True)
                  .reset_index(drop=True)
            )

def deleteCSV():
    import os
    import glob

    files = glob.glob('app/data/tmp/*.csv')
    for f in files:
        os.remove(f)