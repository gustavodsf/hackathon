# -*- coding: utf-8 -*-
import json
import os
import random
import time

from flasgger.utils import swag_from
from flask import (Blueprint, Flask, Response, flash, jsonify, redirect,
                   request, send_file, url_for)
from werkzeug.utils import secure_filename

from api.src.ibm_tools import IbmTools

text_blueprint = Blueprint('text_blueprint', __name__, url_prefix="/text")

@text_blueprint.route('/generate/', methods=['POST'])
@swag_from('post.yml', methods=['POST'])
def from_text_to_speech():
    text = request.form['text_to_speech']
    ibmTools = IbmTools()
    ibmTools.from_text_to_speech(text) 
    return "Sucesso";

@text_blueprint.route('/speech', methods=['GET'])
@swag_from('get.yml', methods=['GET'])
def from_get_text():
    return send_file(".\\..\\speech.wav", mimetype="audio/wav" ,attachment_filename="speech.wav")

