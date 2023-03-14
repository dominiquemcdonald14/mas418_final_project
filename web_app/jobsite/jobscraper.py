from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os
from datetime import datetime

IMAGE = os.path.join('static','image')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE

@app.route('/home')
def home_page():
	return render_template('home.html')


@app.route('/recommender')
def rec_page():
	return render_template('recommender.html')


@app.route('/recommender/result')
def rec_result_page():
	return render_template('recommender_result.html')

###################
# Now build an API that display image
@app.route("/summary")
def summary():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'density.png')
    return render_template("index.html", user_image = full_filename)


@app.route("/role")
def role():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image2.png')
    return render_template("index.html", user_image = full_filename)


@app.route("/role/table")
def role_table():
    table_data = [
        {'name': 'Data Analyst', 'salary': '74.5'},
        {'name': 'Data Engineer', 'salary': '119.5'},
        {'name': 'Data Scientist', 'salary': '115'},
        {'name': 'Machine Learning', 'salary': '130'},
        {'name': 'Others', 'salary': '125'},
    ]
    
    return render_template('index_table.html', table_data=table_data)

@app.route("/location")
def location():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image3.png')
    return render_template("index.html", user_image = full_filename)


@app.route("/location/table")
def location_table():
    table_data = [
        {'name': 'CT', 'salary': '149.75'},
        {'name': 'CO', 'salary': '149.5'},
        {'name': 'UT', 'salary': '140.25'},
        {'name': 'MI', 'salary': '133.75'},
        {'name': 'MO', 'salary': '132'},
    ]
    
    return render_template('index_table.html', table_data=table_data)

@app.route("/skill")
def skill_table():
    table_data = [
        {'Python': '0', 'SQL': '0', 'salary': '111.52'},
        {'Python': '0', 'SQL': '1', 'salary': '145.31'},
        {'Python': '1', 'SQL': '0', 'salary': '101.78'},
        {'Python': '1', 'SQL': '1', 'salary': '117.54'},
    ]
    
    return render_template('index_table_2.html', table_data=table_data)


##################
# Main method to launch Flask server

if __name__ == "__main__":
    app.run(host="localhost", port=os.getuid() + 50000, debug=True)