from app.models.generate import shipment_id
import pandas as pd

def stockFromDataTMP():
    
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
    # Create a blank shipment dictionary
    shipment = {}
    
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
        shipment[shipment_id()] = bundle

    return shipment

def items_summary(shipment):
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
    data = {'Total Items' : len(shipment.item_id.values),
            'Total Cubic Volume in Feet' : (shipment.cubic_volume_ft.values.sum())}
    
    # When the table only contains a single item don't include it in the summary
    if len(shipment.item_group.unique()) > 1:
        data['Total Item Groups'] = len(shipment.item_group.unique())
        
    # Check for shipment id and build additional shipment summaries
    if 'shipment_id' in shipment.keys() :
        data['Total shipments'] = len(shipment.shipment_id.unique())
        data['Shipment Item Ratio'] = len(shipment.item_id.values) / len(shipment.shipment_id.unique())
        data['Cubic Volume not Utilized'] = (1.58*len(shipment.shipment_id.unique()) - shipment.cubic_volume_ft.values.sum())
        data['Percent Cubic Volume not Utilized'] = round(((1.58 * len(shipment.shipment_id.unique()) -
                                                            shipment.cubic_volume_ft.values.sum()) / 
                                                           shipment.cubic_volume_ft.values.sum()) * 100, 2)
    # return resulting summary as a DataFrame
    return (pd.DataFrame(data, 
                         index=['Details'])
           )

def dataframe_summary(shipment):
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
    data = {'Total Items' : len(shipment.item_id.values),
            'Total Cubic Volume in Feet' : shipment.cubic_volume_ft.values.sum(),
            'Total Item Groups' : len(shipment.item_group.unique())}
    
    # Check for shipment id and build additional shipment summaries
    if shipment.index.get_level_values(0).any() :
        shipment_id = shipment.index.get_level_values(0).unique()
        data['Total shipments'] = len(shipment_id)
        data['Shipment Item Ratio'] = round(len(shipment.item_id.values) / len(shipment_id),2)
        data['Cubic Volume not Utilized'] = (1.58*len(shipment_id) - 
                                             shipment.cubic_volume_ft.values.sum())
        data['Percent Cubic Volume not Utilized'] = round(((1.58 * len(shipment_id) - 
                                                            shipment.cubic_volume_ft.values.sum()) / 
                                                     shipment.cubic_volume_ft.values.sum()) * 100, 2)
    # return resulting summary as a DataFrame
    return (pd.DataFrame(data, 
                         index=['Details'])
           )