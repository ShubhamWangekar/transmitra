from application import app
from flask import render_template, url_for,request,redirect, session
import secrets
import os
from application.forms import Myform
from . import utils
import cv2
import pytesseract
import numpy as np
from gtts import gTTS

#from flask import Flask

#app = Flask(__name__,template_folder='template')

@app.route("/")
def index():
    return render_template('index.html' , title = "Home page")

@app.route("/upload" , methods=("POST","GET"))
def upload():
    if request.method == "POST":

        sentence=""

        f = request.files.get("file")
        # something .jpg >> ["somrthing","jpg"]
        # filename, extension = f.filename.split(",")
        filename, extension = os.path.splitext(f.filename)
        generated_filename =secrets.token_hex(10) + extension
    

        file_location = os.path.join(app.config["UPLOADED_PATH"], generated_filename)

        f.save(file_location)
        pytesseract.pytesseract.tesseract_cmd = 'C:/Users/Akanksha/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
        img = cv2.imread(file_location)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        boxes =pytesseract.image_to_data(img)

        for i, box in enumerate(boxes.splitlines()):
            if i == 0:
                continue
            box = box.split()

            if len(box) == 12:
                sentence += box[11]+ " "
            
        # print(sentence)
        session["sentence"] = sentence
        os.remove(file_location)

        return redirect("/decoded/")
    
    else:
        return render_template("upload.html" , title="Upload")

@app.route("/decoded" , methods=["POST","GET"])
def decoded():

    sentence = session.get("sentence")
    form = Myform()

    if request.method == "POST":

        generated_audio_filename = secrets.token_hex(10)+ ".mp4"

        text_data = form.text_field.data
        translate_to = form.language_field.data
        # print("Translate to : ",translate_to)

        translated_text = utils.translate_text(text_data,translate_to)
        # print(translated_text)
        
        tts = gTTS(translated_text,lang=translate_to)

        file_location = os.path.join(app.config["AUDIO_FILE_UPLOAD"],generated_audio_filename)

        tts.save(file_location)
        form.text_field.data = translated_text
        return render_template("decoded.html",title="translation", form = form, audio = True, file= generated_audio_filename)


    else:
        form.text_field.data = sentence
        session["sentence"] = " "
        return render_template("decoded.html", form = form, audio = False)