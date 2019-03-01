def generate_shipment_id():
    
    # Generates an interger shipment id based on datetime
    #Year Month Day Hour Minute Seconds Milleseconds
    
    import re
    import datetime
    
    return int(re.sub("[^0-9]", "", str(datetime.datetime.today()))[:17])