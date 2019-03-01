from app.builder import generate_shipment_id as gen_id
import pandas as pd

def items():
    import glob
    
    # It's nice to assume clean data, and to be right for once
    
    stock = pd.DataFrame()
    for csv in glob.glob("app/data/tmp/*.csv"):
        stock = stock.append(pd.read_csv(csv))
    
    return stock
        
    

def shipments(stock) :
    # Create a blank shipment sheet
    shipments = pd.DataFrame()

    while stock.empty == False :

        # Get the largest item by cubic volume and remove from stock
        stock, largest_item = stock.drop(stock.tail(1).index, axis=0), stock.tail(1)

        bundle = largest_item

        # Filter the remaining stock by what CAN still fit in the box
        # Grab the index of the item and the item

        for index, item in (stock[stock.cubic_volume_ft.values < (1.58 - largest_item.cubic_volume_ft.values)]
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
                stock, item = (stock.drop(index), item)
                bundle = bundle.append(item)

        #Issue a shipment id to the bundle
        bundle["shipment_id"] = gen_id.generate_shipment_id()

        #Add bundle to the shipment file
        shipments = shipments.append(bundle)
    return shipments

def summary(shipments):
    
    # Build initial summaries based on items and cubic volume in feet
    data = {'Total Items' : len(shipments.item_id),
            'Total Cubic Volume in Feet' : shipments.cubic_volume_ft.sum(),
            'Total Item Groups' : len(shipments.item_group.unique())}
    
    # Check for shipment id and build additional shipment summaries
    if 'shipment_id' in shipments.keys() :
        data['Total Shipments'] = len(shipments.shipment_id.unique())
        data['Cubic Volume not Utilized'] = (1.58*len(shipments.shipment_id.unique()) - shipments.cubic_volume_ft.sum())
        data['Percent Cubic Volume not Utilized'] = round(((1.58 * len(shipments.shipment_id.unique()) - shipments.cubic_volume_ft.sum()) / 
                                                     shipments.cubic_volume_ft.sum()) * 100, 2)
    # return resulting summary as a DataFrame
    return (pd.DataFrame(data, 
                         index=[0])
              .rename({0:'Details'})
           )