#from enum import Flag
import flask
from flask import Flask, request
import werkzeug
import time
from Process_Image import Start_Solving, GUI_And_Processing
import os
import signal

flag = False
file_name = "1.png"

def handler(signum, frame):
    if flag == True:
        print("\nImage Processing begins!\n")
        Start_Solving(file_name)
        print("\nDeleting image file now")
        os.remove(file_name)
    exit(1)
signal.signal(signal.SIGINT, handler)

app = flask.Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def handle_request():
    global flag
    global file_name
    flag = True
    File_Names = list(flask.request.files)
    print("\nNumber of Received Images : ", len(File_Names))
    image_num = 1
    for File_Name in File_Names:
        print("Saving Image ", str(image_num), "/", len(File_Names))
        imagefile = flask.request.files[File_Name]
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        file_name = timestr + '_' + filename
        print("Image Filename : " + file_name)
        imagefile.save(timestr + '_' + filename)
        image_num = image_num + 1

        print("\nEnter ctrl C to shutdown the server!")
        print("The reason is once a picture is received, its processing begins")
        print("And we do not wish to have another picture uploaded during initial pictures processing!\n")
        #func = request.environ.get('werkzeug.server.shutdown')
        #func()
        #print("Hello world")
        #raise RuntimeError
        #Start_Solving(file_name)
        #print("Deleting image file now")
        #os.remove(file_name)
    return "Image(s) Uploaded Successfully. Come Back Soon."

app.run(host = "0.0.0.0", port = 5000, debug = True)
#if flag == True:
    #Start_Solving(file_name)
    #print("Deleting image file now")
    #os.remove(file_name)
    #print("Hello")