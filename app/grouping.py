def get_groups(stock):
    if 'item_group' in stock.keys() :
        return stock.item_group.unique()
    else :
        return None