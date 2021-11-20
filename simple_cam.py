from multiprocessing import Process, Queue
import time
import sys
import numpy as np
import cv2
import time
from inference_webcam_realsense import main
import flask
from flask import send_file
from copy import copy

frame_queue = Queue()
data_queue = Queue()

app = flask.Flask(__name__)
app.config['DEBUG'] = False

def get_last_from_queues():
    frame = []
    data = []
    length = data_queue.qsize()
    
    for i in range(length):
        frame = frame_queue.get()    
        data = data_queue.get()

    return frame,data

def cvt_list(data):
    list = []
    for i in range(len(data)):
        list.append(float(data[i]))
    return list



def preprocess_data():
    frame,data = get_last_from_queues()
    # data = boxes, scores, labels, rotations, translations
    global last_data
    global last_data_counter
    # Check if data is availabe and is something in frame
    result_dict = {}
    got_any_data = len(frame)>0 
    has_detection = len(data)>0 and len(data[1])>0
    if(got_any_data):
        print("Timestamp",data[5],time.time())
        if (has_detection):
            for i in range(len(data[1])):
                result_dict[i] = {"box":cvt_list(data[0][i]),'score':float(data[1][i]),'rot':cvt_list(data[3][i]),'trans':cvt_list(data[4][i])}
        last_data_counter = 0
        last_data = (result_dict,frame)
    # No Data for x request -> stop sending old stuff
    elif(last_data_counter>30):
        last_data = ({},[])
    print("Got data {} has detection {}, last {}".format(got_any_data,has_detection,last_data_counter))

    last_data_counter += 1
    return last_data[0],last_data[1],data

@app.route('/',methods=['GET'])
def data():
    result_dict,_,_ = preprocess_data()
    return result_dict


@app.route('/get_image')
def get_image():
    _,frame,_ = preprocess_data()
    # Actuall frame
    if(len(frame)>0):
        cv2.imwrite("img/frame.jpg",frame)
    return send_file("img/frame.jpg", mimetype='image/jpg')


last_data = ({},[])
last_data_counter = 0
queues = []
_start = time.time()
writer_p = Process(target=main, args=(([frame_queue,data_queue]),))
writer_p.start()
app.run(host="0.0.0.0")
writer_p.join()
