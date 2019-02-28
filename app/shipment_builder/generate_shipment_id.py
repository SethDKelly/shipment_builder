def generate_shipment_id():
    
    import time
    import random
    
    return str(time.clock()) + str(random.randint(0,1000)/1000)