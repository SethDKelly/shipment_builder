# import modules
from app import app
from app.models import build, clean, generate, grouping

# import libraries
import pandas as pd
from flask import render_template, Response, redirect, url_for, request, abort


"""
Before anything else do:
"""

# create route that renders index.html template
@app.route("/")
@app.route("/index")
def index():

    # Build shipments
    
    # Generate data
    
    return render_template("index.html", title="Home")

@app.route("/build/shipment")
def buildShipment():
    from sqlalchemy import create_engine
    
    # Pull all data from app/data/tmp
    stock = build.stockFromDataTMP()

    if not stock.empty: # If there isn't any stock to process
        clean.deleteCSV() # Remove old csv files

        # Build shipments from stock and transform 
        shipment = build.shipments(stock)
        
        engine = create_engine('sqlite:///app/data/db/shipment.db', echo=False)
        
        shipment_df = pd.concat(shipment.values(), 
                         keys=shipment.keys())
        
        # future implementations will increase the dataframe columns:
            # Add in a date, possible timestamp (hour:min)
        shipment_df.to_sql('shipment', con=engine, if_exists='append')     
    
    return redirect(url_for('index', shipment=shipment))

@app.route("/build/data")
def buildData():
    
    # This route will create a new test csv
    # Then redirect back to index
    
    generate.csvTestData()
    return redirect(url_for('index'))

@app.route("/notes")
def notes():
    with open("notes_about_csv_file.txt") as notes :
        return Response(notes.read(), mimetype='text/plain')
    
@app.route("/data")
def show_data():

    summary = build.stockSummary(stock)
    
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   stock.to_html(classes='shipments_all')],
                           titles = ['All Items and their Shipments'])

@app.route("/shipments")
def show_shipments():
    
    if not request.args.get(shipment, None):
        abort(404)
     
    shipment = request.args.get(shipment, None)
    shipment_df = pd.concat(shipment.values(), 
                         keys=shipment.keys())
    summary = build.dfSummary(shipment)
    
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   (shipment.to_html(classes='shipments_all'))],
                           titles = ['All Items and their Shipments'], 
                           shipment_size=summary['Total shipments'][0]
                          )

@app.route("/shipments/json")
def shipment_json_data(shipment):
    return shipment.to_json(orient='records')

""" OLD FORMAT
shipments_filtered = {}

for group in grouping.get_groups(stock):
    
    stock_filtered = stock[stock.item_group.values == group]
    
    shipment_filtered = build.shipments(stock_filtered)
    shipments_filtered[group] = pd.concat(shipment_filtered.values(), 
                                         keys=shipment_filtered.keys())
"""

@app.route('/item_group/<group>')
def show_by_group(group):
    
    summary = build.dfSummary(shipments_filtered[group])
    
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   (shipments_filtered[group].to_html(classes='shipments_all'))],
                           titles = ['All Items and their Shipments'], 
                           shipment_size=summary['Total shipments'][0]
                          )

"""
ERROR Exception handling this section should be refactored at some point
"""

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error404.html'), 404

@app.errorhandler(410)
def page_not_found(e):
    # note that we set the 410 status explicitly
    return render_template('error410.html'), 410