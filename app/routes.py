# import modules
from app import app
from app.shipment_builder import build_shipments
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
    
    return render_template('view.html',
                           tables=[stock.to_html(classes='shipments_all')],
                           titles = ['All Items and their Shipments'])

@app.route("/shipments")
def shipments_by_item():
    import pandas as pd
    
    stock = clean.clean_csv()
    shipments = build_shipments.build_shipments(stock)
    length = len(shipments.package_id.unique())
    
    return render_template('view.html',
                           tables=[shipments.to_html(classes='shipments_all')],
                           titles = ['All Items and their Shipments'], 
                           shipment_size=len(shipments.package_id.unique())
                          )
@app.route("/shipments/json")
def json_data():
    import pandas as pd
    
    return (build_shipments.build_shipments(clean.clean_csv())
                           .to_json(orient='records')
           )

@app.route("/grouped_shipments")
def group_by_shipment():
    import pandas as pd
    
    stock = clean.clean_csv()
    shipments = build_shipments.build_shipments(stock)
    
    shipment_view = (shipments.drop(['item_id', 'item_group'],
                                    axis=1)
                              .groupby('package_id')
                              .agg(['count','sum'])
                    )["cubic_volume_ft"]
    
    return render_template('view.html',
                           tables=[shipment_view.to_html(classes='shipments_all')],
                           titles = ['All Shipments'],
                           shipment_size=len(shipment_view.index)
                          )

if __name__ == "__main__":
    app.run(debug=True)