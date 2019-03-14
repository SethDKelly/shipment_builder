# import modules
from app import app
from app.models import build, clean, generate, grouping

# import libraries
import pandas as pd
from flask import render_template, Response, redirect, url_for, request, abort
import sqlalchemy as db

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

@app.route("/loadData")
def loadData():
    
    # Pull all data from app/data/tmp
    stock = build.stockFromDataTMP()

    if stock.empty: # If there isn't any stock to process
        pass
    else:
        clean.deleteCSV() # Remove old csv files
        
        engine = db.create_engine('sqlite:///app/data/db/shipment.db')
        
        # future implementations will increase the dataframe columns:
            # Add in a date, possible timestamp (hour:min)
        stock.to_sql('stock', con=engine, if_exists='replace',index=False, method='multi')
        
        """ POSSIBLE FUTURE IMPLEMENTATION - NEED FOR SPEED
        Session = sessionmaker(bind=dest_db_con)
        session = Session()
        session.bulk_insert_mappings(MentorInformation, df.to_dict(orient="records"))
        session.close()
        """
        
    return redirect(url_for('index'))

@app.route("/makeData")
def makeData():
    
    # This route will create a new test csv
    # Then redirect back to index
    
    generate.csvTestData()
    return redirect(url_for('index'))

"""
Removed feature until this is reworked to fit better
This will implement new notes that will describe
The new test case example once that is built
i.e. items.csv -> bananas.csv or so on

@app.route("/notes")
def notes():
    with open("notes_about_csv_file.txt") as notes :
        return Response(notes.read(), mimetype='text/plain')
"""

@app.route("/data")
def show_data():
    connection = db.create_engine('sqlite:///app/data/db/shipment.db').connect()
    
    stock =pd.read_sql_query("SELECT * FROM stock", con=connection)
    
    summary = build.stockSummary(stock)
    
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   stock.to_html(classes='shipments_all')],
                           titles = ['All Items and their Shipments'])

@app.route("/shipments")
def show_shipments():
    
    connection = db.create_engine('sqlite:///app/data/db/shipment.db').connect()
    
    stock = pd.read_sql_query("SELECT * FROM stock", con=connection)
    shipment = pd.DataFrame(build.shipments(stock))

    summary = build.dfSummary(shipment)
    
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   (shipment.to_html(classes='shipments_all'))],
                           titles = ['All Items and their Shipments'], 
                           shipment_size=summary['Total shipments'][0]
                          )

@app.route("/shipments/json")
def shipment_json_data():
    
    connection = db.create_engine('sqlite:///app/data/db/shipment.db').connect()
    stock = pd.read_sql_query("SELECT * FROM stock", con=connection)
    return pd.DataFrame(build.shipments(stock)).to_json(orient='records')

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
    connection = db.create_engine('sqlite:///app/data/db/shipment.db').connect()
    
    stock = pd.read_sql_query("SELECT * FROM stock", con=connection)
    stock_filtered = stock[stock.item_group.values == group]
    
    shipment = pd.DataFrame(build.shipments(stock_filtered))

    summary = build.dfSummary(shipment)
        
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   (shipment.to_html(classes='shipments_all'))],
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