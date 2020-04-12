from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import time
import cv2
import os
from skimage.measure import compare_ssim
import yaml
from differenceFinder import findTheDifference


UPLOAD_FOLDER = ''

# importing the config
with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    UPLOAD_FOLDER = data['uploadFolder']

app = Flask(__name__, template_folder='./')

@app.route('/upload')
def fy():
    return render_template('q.html')
            
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        timestr = time.strftime("%Y%m%d-%H%M%S")
        f1 = request.files['file']
        f2 = request.files['file2']  
        
        name1=str(f1.filename)[:-4]+"_"+timestr+str(f1.filename)[-4:]
        name2=str(f2.filename)[:-4]+"_"+timestr+str(f1.filename)[-4:]

        video_path = os.path.abspath('.')+UPLOAD_FOLDER
        f1.save(video_path+secure_filename(name1))
        f2.save(video_path+secure_filename(name2))

        result = findTheDifference(name1, name2, timestr)                   

    return str(timestr)

                
if __name__ == '__main__':
    app.run(debug = True)
