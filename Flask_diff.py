from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import time
import cv2
import numpy as np
from numpy import asarray
from PIL import Image
import os
import subprocess,sys
from skimage.measure import compare_ssim
import argparse
import imutils

app = Flask(__name__, template_folder='../flask_code')
a=[]
b=[]

@app.route('/upload')
def fy():
    return render_template('q.html')
            
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        timestr = time.strftime("%Y%m%d-%H%M%S")
        f1 = request.files['file']
        f2 = request.files['file2']        
        name1=f1.filename+"_"+timestr
        name2=f2.filename+"_"+timestr
        f1.save(secure_filename(name1))
        f2.save(secure_filename(name2))
        a.append(name1)
        b.append(name2)
        
        
        
            
        vidcap = cv2.VideoCapture(os.path.join("C:/Users/HP/flask_code",a[0]))
        arr1 = []
            
        def getFrame(sec, count):
                
            vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
            hasFrames,image = vidcap.read()
            if hasFrames:
                cv2.imwrite("C:/Users/HP/Desktop/vid_flask/raw_1/one"+str(count)+"_"+a[0]+".jpg", image)
                arr1.append(image)
                return hasFrames

        count = 0
        sec = 0
        frameRate = 0.05 # it will capture image in each 0.5 second
        success = getFrame(sec, count)

        while success:
            count = count + 1
            sec = sec + frameRate
            sec = round(sec, 2)
            success = getFrame(sec, count)

        print("Converted First video into Frames")
        print("We got ", count, " frames")
        print(len(arr1))
        vidcap = cv2.VideoCapture(os.path.join("C:/Users/HP/flask_code",b[0]))
        arr2 = []
        def getFrame(sec, count):
            vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
            hasFrames,image = vidcap.read()
            if hasFrames:
                arr2.append(image)
                cv2.imwrite("C:/Users/HP/Desktop/vid_flask/raw_2/two"+str(count)+"_"+b[0]+".jpg", image)# save frame as JPG file
            return hasFrames

        count = 0
        sec = 0
        frameRate = 0.05 # it will capture image in each 0.5 second
        success = getFrame(sec, count)

        while success:
            count = count+1
            sec = sec+frameRate
            sec = round(sec, 2)
            success = getFrame(sec, count)

        count = int(count)
        print("\nConverted Second video into Frames")
        print(len(arr2))

        diffarr=[] 
        for i in range(count):
                       
            frameBasePath =  "C:/Users/HP/Desktop/vid_flask/raw_1/one"
            imageA = cv2.imread("C:/Users/HP/Desktop/vid_flask/raw_1/one"+str(i)+"_"+a[0]+".jpg")
            frameBasePath2 =  "C:/Users/HP/Desktop/vid_flask/raw_2/two"
            imageB = cv2.imread("C:/Users/HP/Desktop/vid_flask/raw_2/two"+str(i)+"_"+b[0]+".jpg")

            grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
            grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

            grayA = cv2.bilateralFilter(grayA,9,75,75)
            grayB = cv2.bilateralFilter(grayB,9,75,75)
            (score, diff) = compare_ssim(grayA, grayB, full=True)
            diff = (diff * 255).astype("uint8")
            thresh = cv2.threshold(diff, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cv2.imwrite("C:/Users/HP/Desktop/vid_flask/diff/d"+str(i)+"_"+a[0]+".jpg", thresh) 
            diffarr.append(thresh)
            
        for i in range(count):
            
            frameBasePath =  "C:/Users/HP/Desktop/vid_flask/raw_1/one"
            imageA = cv2.imread("C:/Users/HP/Desktop/vid_flask/raw_1/one"+str(i)+"_"+a[0]+".jpg")
            frameBasePath2 =  "C:/Users/HP/Desktop/vid_flask/raw_2/two"
            imageB = cv2.imread("C:/Users/HP/Desktop/vid_flask/raw_2/two"+str(i)+"_"+b[0]+".jpg")

            grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
            grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

            grayA = cv2.bilateralFilter(grayA,9,75,75)
            grayB = cv2.bilateralFilter(grayB,9,75,75)

                        
            (score, diff) = compare_ssim(grayA, grayB, full=True)
            diff = (diff * 255).astype("uint8")
        
                        
            thresh = cv2.threshold(diff, 0, 255,
                                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
                
            boxA=[]
            boxB=[]
                        # loop over the contours
            for c in cnts:
                
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(imageA,(x, y),(x + w, y + h),(0, 0, 255),2)
                cv2.rectangle(imageB,(x, y),(x + w, y + h),(0, 0, 255),2)
                boxA.append(imageA)
                boxB.append(imageB)
                
            cv2.imwrite("C:/Users/HP/Desktop/vid_flask/mark_1/w"+str(i)+"_"+a[0]+".jpg", imageA) 
            cv2.imwrite("C:/Users/HP/Desktop/vid_flask/mark_2/w"+str(i)+"_"+b[0]+".jpg", imageB)
                
         
                                        
                        

        
            

    return str(a[0])
    



                    
if __name__ == '__main__':
    app.run(debug = True)
