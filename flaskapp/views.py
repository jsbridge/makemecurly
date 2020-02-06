from flask import Flask, render_template
from flask import request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flaskapp import app
from model_image import *
from query import *
import os


upload_folder = 'flaskapp/static/uploads'

app.config['UPLOAD_FOLDER'] = upload_folder

allowed_ext = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        # Check to see if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # If everything looks good, proceed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            predicted_class = predict_class(filepath)

            # List of classes not used in this app
            bad_list = ['straight', 'unsure','braids','dreadlocks','nonhair', 'short']
            if predicted_class in bad_list:
                return render_template('complete.html', predicted_class = predicted_class)

            # Query the product database, return products and amazon URLS for products
            prods, urls = query(predicted_class)

            shampoo, conditioner, leavein,gel,deep,protein,clarify = prods
            ushampoo, uconditioner, uleavein,ugel,udeep,uprotein,uclarify = urls
	
            return render_template('complete.html', predicted_class = predicted_class,
                                    shampoo = shampoo, conditioner=conditioner,
                                    leavein=leavein,gel=gel, deep=deep,protein=protein,
                                    clarify=clarify, ushampoo = ushampoo, uconditioner=uconditioner,
                                    uleavein=uleavein,ugel=ugel, udeep=udeep,uprotein=uprotein,
                                    uclarify=uclarify)
        
            return redirect(url_for('main'))

    return render_template('main.html')


