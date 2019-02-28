from app.shipment_builder import generate_shipment_id as gen_id
import pandas as pd

def build_shipments(stock) :
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
        bundle["package_id"] = gen_id.generate_shipment_id()

        #Add bundle to the shipment file
        shipments = shipments.append(bundle)
    return shipments