from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import time
import cv2
import os
from skimage.measure import compare_ssim
import yaml
from differenceFinder import findTheDifference
from flask import jsonify
from flask_cors import CORS, cross_origin



UPLOAD_FOLDER = ''

# importing the config
with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    UPLOAD_FOLDER = data['uploadFolder']


app = Flask(__name__)
# cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})

@app.route('/uploader', methods = ['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def upload_file():
    print("REQUEST: ", request)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    f1 = request.files['fileOne']
    f2 = request.files['fileTwo']  
    
    name1=str(f1.filename)[:-4]+"_"+timestr+str(f1.filename)[-4:]
    name2=str(f2.filename)[:-4]+"_"+timestr+str(f1.filename)[-4:]

    video_path = os.path.abspath('.')+UPLOAD_FOLDER
    f1.save(video_path+secure_filename(name1))
    f2.save(video_path+secure_filename(name2))

    result = findTheDifference(name1, name2, timestr)                   
    return jsonify(result), 201
                
if __name__ == '__main__':
    app.run(debug = True)
