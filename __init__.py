from flask import Flask
from flask_dropzone import Dropzone
from flask_session import Session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fd9b2d511e3c303b8936aebe92e2b8ee6d901470b2cb702ae4907f790ab6'


SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

dir_path=os.path.dirname(os.path.realpath(__file__))


app.config.update(
    UPLOADED_PATH=os.path.join(dir_path, '../application/static/images/uploaded_files'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1,
    AUDIO_FILE_UPLOAD = os.path.join(dir_path, '../application/static/images/audio_files')
)
app.config['DROPZONE_REDIRECT_VIEW'] = 'decoded'
dropzone = Dropzone(app)

from application import routes

