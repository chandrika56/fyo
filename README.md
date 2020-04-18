# FYO

Flask api for differencing and returning captions.

#### Create the folders if they do no exist, in the same directories

- diff
- mark_1
- mark_2
- marked_videos
- raw_1
- raw_2
- videos

### run the app.py to start the Server

#### Use python3 to run.

### Dependencies:

- Flask
- Opencv
- numpy
- matplotlib
- skimage
- imutils
- pyyaml
- flask-cors

**Note:** You will be able to change the Framerate by changing the Framerate in the config.yaml file. This `FRAME_RATE` must be give as how often the frame has to be captured. So it is actually **1 / framesPerSecond**

**Note:** Number of groups in the config denotes the number of segments/groups that you wish to have in the frames. Typically try to have less than 10 - 15 groups based on the number of frames that you produce.

_Example:_

- 300 frames - 10 groups - so 30 frames per segment
- 30 frames - 5 groups - so 6 frames per segment

It is a hyperparameter

#### End Points

**POST** request to **http://127.0.0.1:5000/uploader** along with files with names **file** and **file2** returns you with a response which looks like:

    {
        "boxedFramesVideoOnePath": "D:\\MyLife\\Final Year Project\\codes\\fyo\\mark_1\\",
        "boxedFramesVideoTwoPath": "D:\\MyLife\\Final Year Project\\codes\\fyo\\mark_2\\",
        "dissimilar_image_list": [
            "0003_20200413-094415.jpg",
            "0004_20200413-094415.jpg",
            "0027_20200413-094415.jpg",
            "0028_20200413-094415.jpg",
            "0029_20200413-094415.jpg"
        ],
        "markedVideosPath": "D:\\MyLife\\Final Year Project\\codes\\fyo\\marked_videos\\",
        "n_dissimilar_images": 5,
        "rawVideoOneFramesPath": "D:\\MyLife\\Final Year Project\\codes\\fyo\\raw_1\\",
        "rawVideoTwoFramesPath": "D:\\MyLife\\Final Year Project\\codes\\fyo\\raw_2\\",
        "status": "success",
        "total_frames": 30,
        "unique_timestamp": "20200413-094415"
    }
