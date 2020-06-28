# -*- coding: utf-8 -*-
import json
import os
import random
from os import listdir
from os.path import isfile, join

from flasgger.utils import swag_from
from flask import (Blueprint, Flask, Response, flash, jsonify, redirect,
                   request, send_file, url_for)
from werkzeug.utils import secure_filename

files_blueprint = Blueprint('files_blueprint', __name__, url_prefix="/voice")

@files_blueprint.route('/list', methods=['GET'])
@swag_from('get.yml', methods=['GET'])
def list_all_files():
    onlyfiles = [f for f in listdir(".\\dataset\\") if isfile(join(".\\dataset\\", f))]
    onlyfiles  = list(filter(lambda x: '.txt' not in x, onlyfiles))
    return str(onlyfiles)
