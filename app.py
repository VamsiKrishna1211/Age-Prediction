import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from model_generator import get_model, load_model_weights
from utils import Get_Croped_image, detect_faces, image_resize_and_preprocessing, age_class_to_age_range, draw_rect_put_text
import tensorflow as tf
from tensorflow.python.keras.models import load_model
#from tensorflow.python.keras.backend import set_session
from tensorflow import keras

import cv2
import numpy as np
import sys

#session = keras.backend.get_session()
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
graph = tf.get_default_graph()
keras.backend.set_session(session)

# session = keras.backend.get_session()
# init = tf.global_variables_initializer()
# session.run(init)
model = load_model_weights("./imdb_age_recog_acc_85_resnet50_15_classes_weights.h5")


UPLOAD_FOLDER = "./images_upload"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
no_faces = False
image_filename = ""



web_app = Flask(__name__)
web_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
web_app.config['SECRET_KEY'] = 'someRandomKey'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@web_app.route("/predict_age", methods=["GET", "POST"])
def predict_age():
    global session
    global graph
    with graph.as_default():
        keras.backend.set_session(session)
        img = cv2.imread("./images_upload/{}".format(image_filename))
        os.remove("./images_upload/{}".format(image_filename))
        print(image_filename+"printed")
        # if len(img) == 0:
        #     raise "Image path not valid"
        all_faces_bb_data = detect_faces(img)
        if ( isinstance(all_faces_bb_data, int) ):
            global no_faces
            no_faces = True
            print("Entered all_faces check if")
            return redirect(url_for(".upload_file"))
        print("Entering for loop")
        no_faces = False
        for bb_data in all_faces_bb_data:
            crp_image = Get_Croped_image(img, bb_data)
            crp_image = image_resize_and_preprocessing(crp_image, (224,224))
            print(crp_image.shape)
            pred_class_values = model.predict(crp_image)
            pred_class = int(np.squeeze(np.argmax(pred_class_values,axis=1)))
            if pred_class != 0:
                pred_class -= 1
            pred_age_range = age_class_to_age_range(pred_class)
            isinstance(pred_age_range, str)
            img = draw_rect_put_text(img, bb_data, pred_age_range)
        cv2.imwrite("./static/"+image_filename.split(".")[0]+"mod."+image_filename.split(".")[1], img)

    return render_template("predict.html", image_show_path=image_filename.split(".")[0]+"mod."+image_filename.split(".")[1])



@web_app.route("/", methods=["GET", "POST"])
def upload_file():
    print("Start")
    #global no_faces
    if request.method == "POST":
        print("entered post")
        if "file" not in request.files:
            print("no file part")
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        print(request.files)

        if file.filename == "":
            print("no file")
            flash("No file given")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            print("all cond satisfied")
            filename = secure_filename(file.filename)
            global image_filename
            image_filename = filename
            file.save(os.path.join(web_app.config["UPLOAD_FOLDER"], filename))
            print("Success")
            return predict_age()#redirect(url_for(".predict_age", _external=True))
        else:
            print("file name none")

    return render_template("index.html", no_faces=no_faces)


if __name__ == "__main__":
    #web_app.run(host='192.168.0.107')
    web_app.run(host='0.0.0.0')
