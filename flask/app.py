
from flask import Flask, request, jsonify, redirect, url_for, Response, send_file
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
import pandas as pd
from flask import render_template, render_template_string
import json
from equities.discount_weights import equities_discount_weights
from equities.percents import equities_percents
from equities.percents_adjust import equities_percents_adjust
from equities.download import equities_download
from equities.make_dataframes import equities_make_dataframes
from equities.best_combo3 import equities_combo

from hy_fixed_income.discount_weights import hy_fixed_income_discount_weights
from hy_fixed_income.percents_adjust import hy_fixed_income_percents_adjust
from hy_fixed_income.download import hy_fixed_income_download




app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

@app.route('/', methods=['post', 'get'])
@app.route('/home', methods=['post', 'get'])
def equities():
    global index
    global weights
    if request.values.get('index') != None:
        index = str(request.values.get('index'))
    else:
        dicty = open("./equities/dataframes/dicty.json")
        dicty = dicty.read()
        data = json.loads(dicty)
        data = str(data).replace('\'', '').replace('-', '')
        return render_template('sp500_plot.html', data=data)

    discount_weights, cef_data = equities_discount_weights("hey", index)
    assets_adjust, data_points, data_points_adjusted= equities_percents_adjust("hey", index)

    if request.method == 'POST':
        weights = request.form  # access the data inside

        if "download" == request.form["action"]:
            return redirect(url_for('csv'))
        if "reset" != request.form["action"]:
            assets_adjust, data_points, data_points_adjusted= equities_percents_adjust(weights, index)
            discount_weights, cef_data = equities_discount_weights(weights, index)



    cef_data["discount"] = round(cef_data["discount"] * float(data_points["amount_cef"])/100,2)
    cef_data["adjusted_discount"] = round(cef_data["adjusted_discount"] * float(data_points_adjusted["amount_cef"])/100,2)
    cef_data["effective"] = round(cef_data["effective"] * float(data_points["amount_cef"])/100,2)
    cef_data["adjusted_effective"] = round(cef_data["effective"] * float(data_points_adjusted["amount_cef"])/100,2)
    return render_template('hy_home.html',
    assets_adjust=assets_adjust,
    discount_weights=discount_weights,
    data_points=data_points, data_points_adjusted=data_points_adjusted,
    cef_data=cef_data)




@app.route('/csv', methods=['post', 'get'])
def csv():
    print(weights)
    if request.method == 'GET':
        pass
        #weights = request.form
        #print(weights)
    equities_download(weights)
    return send_file('equities/dataframes/download.csv',
                     mimetype='text/csv',
                     attachment_filename='s&p500_closed_end_fund_index.csv',
                     as_attachment=True)


@app.route('/home2', methods=['post', 'get'])
def hy_fixed_income():
    global index
    global weights
    if request.values.get('index') != None:
        index = str(request.values.get('index'))
    else:
        dicty = open("./hy_fixed_income/dataframes/dicty.json")
        dicty = dicty.read()
        data = json.loads(dicty)
        data = str(data).replace('\'', '').replace('-', '')
        return render_template('hy_plot.html', data=data)

    discount_weights, cef_data = hy_fixed_income_discount_weights("hey", index)
    assets_adjust, data_points, data_points_adjusted= hy_fixed_income_percents_adjust("hey", index)
    if request.method == 'POST':
        weights = request.form  # access the data inside

        if "download" == request.form["action"]:
            return redirect(url_for('csv'))
        if "reset" != request.form["action"]:
            assets_adjust, data_points, data_points_adjusted= hy_fixed_income_percents_adjust(weights, index)
            discount_weights, cef_data = hy_fixed_income_discount_weights(weights, index)



    cef_data["discount"] = round(cef_data["discount"] * float(data_points["amount_cef"])/100,2)
    cef_data["adjusted_discount"] = round(cef_data["adjusted_discount"] * float(data_points_adjusted["amount_cef"])/100,2)
    cef_data["effective"] = round(cef_data["effective"] * float(data_points["amount_cef"])/100,2)
    cef_data["adjusted_effective"] = round(cef_data["effective"] * float(data_points_adjusted["amount_cef"])/100,2)
    return render_template('hy_home.html',
    assets_adjust=assets_adjust,
    discount_weights=discount_weights,
    data_points=data_points, data_points_adjusted=data_points_adjusted,
    cef_data=cef_data)








if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
