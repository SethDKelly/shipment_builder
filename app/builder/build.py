from app.builder import generate_shipment_id as gen_id
import pandas as pd

def items():
    
    """
    Check app/data/tmp/ for any .csv data
    Append all the data and return the result
    result will be a single DataFrame
    """
    
    import glob
    
    # It's nice to assume clean data, and to be right for once
    
    stock = pd.DataFrame()
    for csv in glob.glob("app/data/tmp/*.csv"):
        stock = stock.append(pd.read_csv(csv))
    
    return (stock.reset_index(drop=True)
                 .sort_values('cubic_volume_ft')
           )
        
def shipments(stock) :
    """
    Takes a pandas DataFrame with assumed columns:
     item_id
     cubic_volume_ft
     item_group
    
    Returns a dictionary with shipment_id's as the keys
    Values stored are pandas DataFrames of item 'bundles'
    """
    # Create a blank shipment sheet
    shipments = {}
    
    while stock.empty == False :

        # Get the largest item by cubic volume and remove from stock
        bundle, stock = stock.tail(1), stock.drop(stock.tail(1).index, axis=0)

        # Filter the remaining stock by what CAN still fit in the box
        # Grab the index of the item and the item

        for index, item in (stock[stock.cubic_volume_ft.values < (1.58 - bundle.cubic_volume_ft.values)]
                            .sort_values("cubic_volume_ft",
                                         ascending=False)
                           ).iterrows():
            
            # If there is no item in stock that could fit into the bundle break out of the matrix
            if (bundle.cubic_volume_ft.sum() + stock.cubic_volume_ft.values.min()) > 1.58 :
                break
                
            # If it fits it sits
            # Add the item to the bundle
            # Drop item from the stock
            elif (bundle.cubic_volume_ft.sum() + item.cubic_volume_ft) <= 1.58 :
                item, stock = (item, stock.drop(index))
                bundle = bundle.append(item)
                
        #Issue a shipment id to the bundle
        shipments[gen_id.generate_shipment_id()] = bundle

    return shipments

def summary(shipments):
    """
    Builds summary statistics from a shipments DataFrame
    Assumes columns within named
     item_id
     cubic_volume_ft
     item_group
    Situationally may use
     shipment_id
    """
    
    # Build initial summaries based on items and cubic volume in feet
    data = {'Total Items' : len(shipments.item_id.values),
            'Total Cubic Volume in Feet' : shipments.cubic_volume_ft.values.sum(),
            'Total Item Groups' : len(shipments.item_group.unique())}
    
    # Check for shipment id and build additional shipment summaries
    if shipment.index.get_level_values(0).any() :
        shipment_id = shipment.index.get_level_values(0).unique()
        data['Total Shipments'] = len(shipment_id)
        data['Shipment Item Ratio'] = round(len(shipments.item_id.values) / len(shipment_id),2)
        data['Cubic Volume not Utilized'] = (1.58*len(shipment_id) - 
                                             shipments.cubic_volume_ft.values.sum())
        data['Percent Cubic Volume not Utilized'] = round(((1.58 * len(shipment_id) - 
                                                            shipments.cubic_volume_ft.values.sum()) / 
                                                     shipments.cubic_volume_ft.values.sum()) * 100, 2)
    # return resulting summary as a DataFrame
    return (pd.DataFrame(data, 
                         index=['Details'])
           )