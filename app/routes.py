# import modules
from app import app
from app.models import build, clean, generate, grouping

# import libraries
import pandas as pd
from flask import render_template, Response


"""
Before anything else do:
"""
stock = clean.clean_csv()

# create route that renders index.html template
@app.route("/")
@app.route("/index")
def index():

    # Build shipments
    
    # Generate data
    
    return render_template("index.html", title="Home")

#stock = build.items()


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
    
    shipment = build.shipments(stock)
    
    shipment = pd.concat(shipment.values(), 
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

shipments_filtered = {}

for group in grouping.get_groups(stock):
    
    stock_filtered = stock[stock.item_group.values == group]
    
    shipment_filtered = build.shipments(stock_filtered)
    shipments_filtered[group] = pd.concat(shipment_filtered.values(), 
                                         keys=shipment_filtered.keys())

@app.route('/item_group/<group>')
def show_by_group(group):
    
    summary = build.dfSummary(shipments_filtered[group])
    
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   (shipments_filtered[group].to_html(classes='shipments_all'))],
                           titles = ['All Items and their Shipments'], 
                           shipment_size=summary['Total shipments'][0]
                          )