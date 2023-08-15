"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, request, send_file
from reverse_video import app
import os
from werkzeug.utils import secure_filename
import cv2
from pydub import AudioSegment
import numpy as np
import subprocess


UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'reversed_videos'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

ALLOWED_EXTENSIONS = {'mp4'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

def reverse(upload_path,reversed_path):

    ffmpeg_cmd = [
        'ffmpeg',            # FFmpeg executable
        '-i', upload_path,    # Input file
        '-vf', 'reverse',    # Video filter to reverse video frames
        '-af', 'areverse',   # Audio filter to reverse audio
        reversed_path         # Output file
    ]
# Run the FFmpeg command
    subprocess.run(ffmpeg_cmd)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(r'C:\Users\jonat\source\repos\reverse video\reverse video\reverse_video\uploads', filename)
        print(upload_path)
        file.save(upload_path)
        reversed_filename = f"reversed_{filename}"
        reversed_path = os.path.join(r'C:\Users\jonat\source\repos\reverse video\reverse video\reverse_video\reversed_videos', reversed_filename)
        
        reverse(upload_path,reversed_path)
        #video_clip = mp.VideoFileClip(upload_path)
        #reversed_clip = video_clip.fl_time(lambda t: video_clip.duration - t)
        #reversed_audio_clip = reversed_clip.audio.fx(mp.audio.fx.audio_fadein, 2)  # Fade in audio at the beginning

        
        
        
        return send_file(reversed_path, as_attachment=True)
    else:
        return "Invalid file format"

