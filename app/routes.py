# import modules
from app import app
from app.builder import build
from app import clean

# import libraries
from flask import render_template, Response

# create route that renders index.html template
@app.route("/")
@app.route("/index")
def index():

    return render_template("index.html", title="Home")

@app.route("/notes")
def notes():
    with open("notes_about_csv_file.txt") as notes :
        return Response(notes.read(), mimetype='text/plain')
    
@app.route("/data")
def show_data():
    import pandas as pd
    
    stock = clean.clean_csv()
    summary = build.summary(stock)
    
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   stock.to_html(classes='shipments_all')],
                           titles = ['All Items and their Shipments'])

@app.route("/shipments")
def shipments():
    import pandas as pd
    
    stock = clean.clean_csv()
    shipments = build.shipments(stock)
    summary = build.summary(shipments)
    
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   shipments.to_html(classes='shipments_all')],
                           titles = ['All Items and their Shipments'], 
                           shipment_size=summary['Total Shipments'][0]
                          )
@app.route("/shipments/json")
def json_data():
    import pandas as pd
    
    return (build.shipments(clean.clean_csv())
                           .to_json(orient='records')
           )

@app.route('/item_group/<group>')
def some_place_page(group):
    import pandas as pd
    
    # Pull in stock data and filter by group
    stock = clean.clean_csv()
    stock = stock[stock.item_group.values == group]
    
    # Build shipment and summary tables after filtering
    shipments = build.shipments(stock)
    summary = build.summary(shipments)
    
    return render_template('table_viewer.html',
                           tables=[summary.to_html(classes='shipments_all'),
                                   shipments.to_html(classes='shipments_all')],
                           titles = ['All Items and their Shipments'], 
                           shipment_size=summary['Total Shipments'][0]
                          )

if __name__ == "__main__":
    app.run(debug=True)