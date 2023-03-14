# Import flash and other stuff we will need
import pandas as pd
import numpy as np
from flask import Flask, escape, request, render_template
import os
from datetime import datetime

IMAGE = os.path.join('static','image')

# This is how we initiate a flask app to then build it
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE

#################
# Lets start with building a hello world API
#
# > http://$HOSTNAME/v1 -- return Hello World!
# > http://$HOSTNAME/v1?name=some_name -- return Hello $some_name
@app.route("/v1")
def hello():
    name = request.args.get("name", "World")
    return f"Hello, {escape(name)}!"


# Let's make the API more RESTful
#
# > http://$HOSTNAME/v2/some_name -- return Hello $some_name
@app.route("/v2/<name>", methods=["GET"])
def hello2(name):
    return f"Hello, {escape(name)} (v2)"


# Let's add some basic things:
#
# > http://$HOSTNAME/v3 --  Hello world
# > http://$HOSTNAME/v3/$some_name -- Hello $some_name
# > http://$HOSTNAME/test/hello-world -- Hello World
@app.route("/v3", methods=["GET"])
@app.route("/test/hello-world", methods=["GET"])
@app.route("/v3/<string:name>", methods=["GET"])
def hello3(name="World"):
    return f"Hello, {escape(name)} (v3)"


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

@app.route('/form', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form.get("fname")
       # getting input with name = lname in HTML form
       last_name = request.form.get("lname")
       return "Your name is "+first_name + last_name
    return render_template("form.html")


##################
# Main method to launch Flask server
#
# --> host: makes it bind publically (could have als been 0.0.0.0 instead). If
# we did not specify this it would only bind to 127.0.0.1 which means it would
# only be accessible from the local computer
#
# --> port: set the "port" we bind to to be based on our Linux user ID. This
# way if multiple users try to launch flask servers each will run on a
# different port to avoid conflicts
#
# --> debug: enable debugging and more verbose information since we are still
# developing the app and not running it in a production environment
if __name__ == "__main__":
    app.run(host="localhost", port=os.getuid() + 50000, debug=True)
