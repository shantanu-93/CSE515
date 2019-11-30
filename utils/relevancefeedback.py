import pdb
import webbrowser
import os
import numpy as np
import task6_svm as task6_svm
from flask import Flask, request, render_template, send_from_directory,redirect
app = Flask(__name__,template_folder=(os.path.abspath('templates')))
classifier_g = None
query_image_g = None
similar_images_g = None

"""
initial call to relevance feedback. 
Load app server
Set global vars
"""
def relevance_fdbk(data_dir,classifier,query_image,similar_images):
    print(data_dir)
    global classifier_g, query_image_g, similar_images_g

    classifier_g = classifier
    query_image_g = query_image
    similar_images_g = similar_images
    print("\nClick here: http://localhost:4558/similar_images\n")
    app.run(port=4558, debug=True)

"""
Method to load Hand Images on browser page
"""
@app.route(str('/Hands/<filename>'))
def send_image(filename):
    return send_from_directory(os.path.abspath("Hands"), filename)

"""
Method to handle feedback and return revised results 
"""
@app.route('/similar_images', methods = ['GET', 'POST'])
def display_similar_images():
    if request.method == 'POST':
        data = request.form
        global similar_images_g
        similar_images_g = incorporate_feedback(data.to_dict())
        return redirect("http://localhost:4558/similar_images", code=303 )
    elif request.method == 'GET':
        return render_template("relevancefeedback.html", image_names=[query_image_g, similar_images_g])
"""
Method to call the chosen classifier based feedback system
"""    
def incorporate_feedback(data):
    if classifier_g == "SVM":
        rel_similar_images = task6_svm.rewrite_query(data)
    return rel_similar_images    
