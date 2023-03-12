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
@app.route("/image")
def show_image():
    full_filename1 = os.path.join(app.config['UPLOAD_FOLDER'], 'density.png')
    full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], 'image2.png')
    full_filename3 = os.path.join(app.config['UPLOAD_FOLDER'], 'image3.png')
    return render_template("index.html", user_image = full_filename1, user_image2 = full_filename2, user_image3 = full_filename3)



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