import os

from flask import Flask, send_from_directory
from flask_restful import Api
from api.ApiHandler import ApiHandler

app = Flask(__name__, static_url_path='', static_folder='frontend')
api = Api(app)


@app.route("/")
def serve():
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(ApiHandler, '/api')

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))