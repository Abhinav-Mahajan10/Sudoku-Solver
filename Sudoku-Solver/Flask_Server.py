import flask
from flask import Flask, request
import werkzeug
import time
from Process_Image import Start_Solving, GUI_And_Processing
import os

app = flask.Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def handle_request():
    File_Names = list(flask.request.files)
    print("\nNumber of Received Images : ", len(File_Names))
    image_num = 1
    for File_Name in File_Names:
        print("\nSaving Image ", str(image_num), "/", len(File_Names))
        imagefile = flask.request.files[File_Name]
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        file_name = timestr + '_' + filename
        print("Image Filename : " + file_name)
        imagefile.save(timestr + '_' + filename)
        image_num = image_num + 1
        print("\n")
        Start_Solving(file_name)
        print("Deleting image file now")
        os.remove(file_name)
    return "Image(s) Uploaded Successfully. Come Back Soon."

app.run(host = "0.0.0.0", port = 5000, debug = True)