import cv2
import os
from skimage.measure import compare_ssim
import imutils
import yaml
import numpy as np
from os.path import isfile, join

def findTheDifference(video1, video2, timestamp):

    UPLOAD_FOLDER = ''
    FRAME_RATE = 0.5
    # importing the config
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        UPLOAD_FOLDER = data['uploadFolder']
        FRAME_RATE = data['frameRate']
        NUMBER_OF_GROUPS = data['numberOfGroups']

    def get_right_count(count):
        if count<10:
            count = '000'+str(count)
        elif count<100:
            count = '00'+str(count)
        elif count<1000:
            count = '0'+str(count)
        return count 

    path = os.path.abspath('.')+UPLOAD_FOLDER+video1
    vidcap = cv2.VideoCapture(path)
    arr1 = []       

    def getFrame(sec, count):   
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        count = get_right_count(count)
        if hasFrames:
            print('Saving image')
            cv2.imwrite(os.path.abspath('.')+"/raw_1/"+str(count)+"_"+timestamp+".jpg", image)
            arr1.append(image)
        return hasFrames

    count = 0
    sec = 0
    frameRate = FRAME_RATE # it will capture image in each 0.5 second
    success = getFrame(sec, count)

    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec, count)

    print("Converted First video into Frames")
    print("We got ", count, " frames")
    
    path = os.path.abspath('.')+UPLOAD_FOLDER+video2
    vidcap = cv2.VideoCapture(path)
    arr2 = []

    def getFrame(sec, count):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        count = get_right_count(count)
        if hasFrames:
            print('Saving image')
            arr2.append(image)
            cv2.imwrite(os.path.abspath('.')+"/raw_2/"+str(count)+"_"+timestamp+".jpg", image)# save frame as JPG file
        return hasFrames

    count = 0
    sec = 0
    frameRate = FRAME_RATE # it will capture image in each 0.5 second
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

    # finding the number of frames per group
    n_per_group = int(count / NUMBER_OF_GROUPS)
    score_list = []
    dissimilar_image_list = []

    for i in range(count):

        i = get_right_count(i)
        
        frameBasePath =  os.path.abspath('.')+"/raw_1/"
        imageA = cv2.imread(frameBasePath+str(i)+"_"+timestamp+".jpg")
        frameBasePath2 =  os.path.abspath('.')+"/raw_2/"
        imageB = cv2.imread(frameBasePath2+str(i)+"_"+timestamp+".jpg")

        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        grayA = cv2.bilateralFilter(grayA,9,75,75)
        grayB = cv2.bilateralFilter(grayB,9,75,75)

        (score, diff) = compare_ssim(grayA, grayB, full=True)
        score_list.append(score)

        diff = (diff * 255).astype("uint8")
        thresh = cv2.threshold(diff, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cv2.imwrite(os.path.abspath('.')+"/diff/"+str(i)+"_"+timestamp+".jpg", thresh) 
        diffarr.append(thresh)
        
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
            
        cv2.imwrite(os.path.abspath('.')+"/mark_1/"+str(i)+"_"+timestamp+".jpg", imageA) 
        cv2.imwrite(os.path.abspath('.')+"/mark_2/"+str(i)+"_"+timestamp+".jpg", imageB)  


    avg_list= list()
    sum = 0
    n = 0
    i = 0

    for index, score in enumerate(score_list):
        i+=1
        sum+=round(score, 2)
        if i == n_per_group or index == len(score_list)-1:
            avg = sum / i
            avg_list.append(avg)
            i=0
            sum=0
            avg=0

    print(avg_list)

    print("We have ", int(len(avg_list)), "segments")
    segment = 0
    for index, score in enumerate(score_list):
        if round(score, 2) < avg_list[segment]:
            c = get_right_count(index)
            image_name = c + "_" + timestamp + ".jpg"
            dissimilar_image_list.append(image_name)
        i+=1
        if i == n_per_group or index == len(score_list)-1:
            print("In Segment ", segment+1)
            if segment < len(avg_list)-1:
                segment += 1
            i=0

    print(len(dissimilar_image_list))
    print(dissimilar_image_list)
    # print(score_list)

    def convert_frames_to_video(pathIn,pathOut,fps):
        frame_array = []
        
        print('Path: ', pathIn)
        print('PathOut: ', pathOut)
        images_id = timestamp + '.jpg'
        files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f)) and str(f).endswith(images_id)]
    
        #for sorting the file names properly
        files.sort()

        print(files)
    
        for i in range(len(files)):
            filename=pathIn + files[i]
            #reading each files
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            print(filename)
            #inserting the frames into an image array
            frame_array.append(img)
    
        out = cv2.VideoWriter(pathOut,0x7634706d, fps, size)
    
        for i in range(len(frame_array)):
            # writing to a image array
            out.write(frame_array[i])
        out.release()

    pathIn = os.path.abspath('.')+'/mark_1/'
    pathOut = os.path.abspath('.')+'/marked_videos/videoOut1'+timestamp+'.mp4'
    fps = 1 / FRAME_RATE
    convert_frames_to_video(pathIn, pathOut, fps)

    pathIn = os.path.abspath('.')+'/mark_2/'
    pathOut = os.path.abspath('.')+'/marked_videos/videoOut2'+timestamp+'.mp4'
    fps = 1 / FRAME_RATE
    convert_frames_to_video(pathIn, pathOut, fps)

    result = {
        'status': 'success',
        'unique_timestamp': timestamp,
        'dissimilar_image_list': dissimilar_image_list,
        'n_dissimilar_images': len(dissimilar_image_list),
        'total_frames': count,
        'markedVideosPath': os.path.abspath('.')+'\\marked_videos\\',
        'rawVideoOneFramesPath': os.path.abspath('.')+'\\raw_1\\',
        'rawVideoTwoFramesPath': os.path.abspath('.')+'\\raw_2\\',
        'boxedFramesVideoOnePath': os.path.abspath('.')+'\\mark_1\\',
        'boxedFramesVideoTwoPath': os.path.abspath('.')+'\\mark_2\\',
    }

    return result