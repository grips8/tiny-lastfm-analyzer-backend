from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from api.ApiHandler import ApiHandler

app = Flask(__name__, static_url_path='', static_folder='frontend')
CORS(app)
api = Api(app)


@app.route("/")
def serve():
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(ApiHandler, '/api')
