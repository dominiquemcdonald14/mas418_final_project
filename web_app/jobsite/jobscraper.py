from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os
from datetime import datetime
import string
import csv

IMAGE = os.path.join('static','image')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE

@app.route('/home')
def home_page():
	return render_template('home.html')


#@app.route('/recommender')
#def rec_page():
	#return render_template('recommender.html')


@app.route('/recommender/result')
def rec_result_page():
	return render_template('recommender_result.html')

@app.route('/recommender', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       location = request.form.get("loc")
       # getting input with name = lname in HTML form
       skills = request.form.get("sk")
       # getting input with name = lname in HTML form
       education = request.form.get("ed")
       
       df = pd.read_csv('salary.csv', encoding= 'unicode_escape')

       loc_recommend_df = df[(df['location'] == location) | (df['High_Ed'] == education) | (df['Python'] == skills)]
    
       # sort DataFrame by salary in descending order and return top 5 observations
       top_salaries = loc_recommend_df.sort_values(by='salary', ascending=False).head(5)
       
       return top_salaries[['companyName', 'company_starRating', 'company_offeredRole' , 'salary', 'requested_url']].to_dict()
       #return render_template('index_table_4.html', table_data=table_data)
    return render_template("form.html")

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
        {'name': 'Data Analyst', 'salary': '76'},
        {'name': 'Data Engineer', 'salary': '119.5'},
        {'name': 'Data Scientist', 'salary': '106'},
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
        {'name': 'MO', 'salary': '132'},
        {'name': 'DC', 'salary': '130.25'},
    ]
    
    return render_template('index_table.html', table_data=table_data)

@app.route("/education")
def education():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image4.png')
    return render_template("index.html", user_image = full_filename)


@app.route("/education/table")
def education_table():
    table_data = [
        {'PhD': '0', 'Master': '0', 'Bachelor': '1', 'salary': '111.06'},
        {'PhD': '0', 'Master': '1', 'Bachelor': '1', 'salary': '94.95'},
        {'PhD': '0', 'Master': '1', 'Bachelor': '0', 'salary': '91.71'},
        {'PhD': '1', 'Master': '1', 'Bachelor': '1', 'salary': '114.0'},
        {'PhD': '1', 'Master': '1', 'Bachelor': '0', 'salary': '128.55'},
        {'PhD': '1', 'Master': '0', 'Bachelor': '0', 'salary': '145.75'},
    ]
    
    return render_template('index_table_3.html', table_data=table_data)

@app.route("/skill")
def skill_table():
    table_data = [
        {'Python': '0', 'SQL': '0', 'salary': '107.8'},
        {'Python': '0', 'SQL': '1', 'salary': '126.3'},
        {'Python': '1', 'SQL': '0', 'salary': '101.95'},
        {'Python': '1', 'SQL': '1', 'salary': '111.38'},
    ]
    
    return render_template('index_table_2.html', table_data=table_data)


##################
# Main method to launch Flask server

if __name__ == "__main__":
    app.run(host="localhost", port=os.getuid() + 50000, debug=True)