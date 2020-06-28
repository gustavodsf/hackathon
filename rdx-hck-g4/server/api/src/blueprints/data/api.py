# -*- coding: utf-8 -*-
import json
import os
import random
from os import listdir
from os.path import isfile, join
from flask import jsonify


from flasgger.utils import swag_from
from flask import (Blueprint, Flask, Response, flash, jsonify, redirect,
                   request, send_file, url_for)
from werkzeug.utils import secure_filename

data_blueprint = Blueprint('data_blueprint', __name__, url_prefix="/data")

@data_blueprint.route('/', methods=['GET'])
@swag_from('get.yml', methods=['GET'])
def list_all_files():
    with open('dados.json') as json_file:  
        data = json.load(json_file)
        dados = []
        for i in range(len(data['Data'])):
            dados.append({
                'complexidade':  data["Complexidade"][str(i)],
                'data': data["Data"][str(i)],
                'requerente': data["Requerente"][str(i)],
                'tags': data["Tags"][str(i)],
                "usina": data["Usina"][str(i)]
            })
        return jsonify(dados)
