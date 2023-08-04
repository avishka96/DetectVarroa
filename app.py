from flask import Flask, render_template, request, jsonify, session
import os
import json
import pandas as pd
import io
import numpy as np
from enum import Enum
from Utils import allowed_file
from main import runmain
import warnings
from time import sleep
warnings.filterwarnings("ignore")


app = Flask(__name__,  template_folder='templates', static_folder='static')

# Set Environment Variables
UPLOAD_FOLDER = os.path.join('static', 'uploads')
OUTPUT_FOLDER = os.path.join('static', 'output')

# Output vidoe will always be inside OUTPUT_FOLDER as result.avi
output_image_path = os.path.join(OUTPUT_FOLDER, 'result.avi')
print(output_image_path)

#The config is actually a subclass of a dictionary and can be modified just like any dictionary

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'xyz'
#app.config["MONGO_URI"] = "mongodb://localhost:27017/"
os.path.dirname("../templates")

@app.route('/')
def main():
    return render_template("index.html")


@app.route('/', methods=["POST"])
def uploadFile():
    if not os.path.exists(app.config['UPLOAD_FOLDER']): # Create Directory for the uploaded static
        os.mkdir(app.config['UPLOAD_FOLDER'])

    _img = request.files['file-uploaded']
    filename = _img.filename
    allowed_file(filename)
    _img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    return render_template('index.html', success = True)


@app.route('/show_file')
def displayImage():
    img_file_path = session.get('uploaded_img_file_path', None)
    if img_file_path.split(".")[-1] in ("mp4", "avi"):
        return render_template('show_file.html', user_image=img_file_path, is_image = False, is_show_button=True)
    

@app.route('/detect_object')
def detectObject():

    uploaded_image_path = session.get('uploaded_img_file_path', None)
    #output_image_path, response, file_type = detect_and_draw_box(uploaded_image_path)
    runmain(uploaded_image_path)

    sleep(3)

    return render_template('show_file.html',  user_image= output_image_path, is_image= False, is_show_button=False)

# @app.route('/get-items')
#
# def get_items():
#     return jsonify(aws_controller.get_items())

if __name__ == '__main__':
    app.run(debug=True)
    
    
