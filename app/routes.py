# import modules
from app import app
from app.builder import build
from app import clean
from app import grouping

# import libraries
import pandas as pd
from flask import render_template, Response

# create route that renders index.html template
@app.route("/")
@app.route("/index")
def index():

    # Build shipments
    
    # Generate data
    
    return render_template("index.html", title="Home")

#stock = build.items()
stock = (clean.clean_csv()
              .sort_values('cubic_volume_ft')
        )
shipments = build.shipments(stock)

@app.route("/notes")
def notes():
    with open("notes_about_csv_file.txt") as notes :
        return Response(notes.read(), mimetype='text/plain')
    
@app.route("/data")
def show_data():    
    summary = build.summary(stock)
    
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   stock.to_html(classes='shipments_all')],
                           titles = ['All Items and their Shipments'])

@app.route("/shipments")
def show_shipments():
    summary = build.summary(shipments)
    
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   (shipments.set_index('shipment_id')
                                             .to_html(classes='shipments_all'))],
                           titles = ['All Items and their Shipments'], 
                           shipment_size=summary['Total Shipments'][0]
                          )

@app.route("/shipments/json")
def shipment_json_data(shipments):
    return shipments.to_json(orient='records')

shipments_filtered = {}
for group in grouping.get_groups(stock):
    stock_filtered = stock[stock.item_group.values == group]
    shipments_filtered[group] = build.shipments(stock_filtered)

@app.route('/item_group/<group>')
def show_by_group(group):
    
    summary = build.summary(shipments_filtered[group])
    
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   (shipments_filtered[group].set_index('shipment_id')
                                                             .to_html(classes='shipments_all'))],
                           titles = ['All Items and their Shipments'], 
                           shipment_size=summary['Total Shipments'][0]
                          )