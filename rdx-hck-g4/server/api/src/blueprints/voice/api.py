# -*- coding: utf-8 -*-
import json
import os
import random
from os import listdir

from flasgger.utils import swag_from
from flask import (Blueprint, Flask, Response, flash, jsonify, redirect,
                   request, send_file, url_for)
from werkzeug.utils import secure_filename

from api.src.google_tools import GoogleTools

voice_blueprint = Blueprint('voice_blueprint', __name__, url_prefix="/voice")
ALLOWED_EXTENSIONS = set(['wav'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@voice_blueprint.route('/', methods=['POST'])
@swag_from('post.yml', methods=['POST'])
def upload_file():
  file = request.files.copy()['upfile']
  file.save('upload.wav')
  googleTools = GoogleTools()
  return googleTools.from_speech_to_text('upload.wav')

@voice_blueprint.route('/<nome_arquivo>', methods=['GET'])
@swag_from('get.yml', methods=['GET'])
def send_audio_file(nome_arquivo):
  return send_file(".\\..\\dataset\\"+nome_arquivo, mimetype="audio/wav",  attachment_filename=nome_arquivo)
