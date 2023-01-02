import re

from flask import Flask, jsonify

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flagger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config=swagger_config)

@swag_from("docs/binar_data_science/hello_world.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def hello_world():
    json_response = {
        'status_code': 200,
        'description': "Menyapa Hello World",
        'data': "Hello World",
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/binar_data_science/text_processing.yaml", methods=['POST'])
@app.route('/', methods=['POST'])
def text_processing():
    text = request.form.get('text')
    
    json_response = {
        'status_code': 200,
        'description': "Text processing result",
        'data': re.findall(r'[A-Za-z0-9_.-]{3,20}\@[a-z]{2,15}\.[a-z.]{2,5}', text),
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run()