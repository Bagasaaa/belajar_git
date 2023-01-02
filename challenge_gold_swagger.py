import re
import json
from flask import Flask, jsonify
import pandas as pd

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
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flagger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

@swag_from("./templates/text_processing.yaml", methods=['GET'])
@app.route('/docs', methods=['GET'])
def text_processing():
    df = pd.read_csv("C:/Users/Acer/docs/binar_data_science/data.csv", encoding='latin-1')
    # Preprocessing Data (Cleansing Data)
    def cleansing(text):
        # Make sentence being lowercase
        text = text.lower()
        # Remove user, rt, \n, retweet, \t, url, xd
        pattern_1 = r'(user|^rt|\\n|^retweet|\\t|\\r|url|xd)'
        text = re.sub(pattern_1, '', text)
        # Remove mention
        pattern_2 = r'@[^\s]+'
        text = re.sub(pattern_2, '', text)
        # Remove hashtag
        pattern_3 = r'#([^\s]+)'
        text = re.sub(pattern_3, '', text)
        # Remove general punctuation, math operation char, etc.
        pattern_4 = r'[\,\@\*\_\-\!\:\;\?\'\.\"\)\(\{\}\<\>\+\%\$\^\=\#\/\`\~\|\&\|]'
        text = re.sub(pattern_4, '', text)
        # Remove single character
        pattern_5 = r'\b[a-zA-Z]\b'
        text = re.sub(pattern_5, '', text)
        # Remove emoji
        pattern_6 = r'\\[a-z0-9]{1,5}'
        text = re.sub(pattern_6, '', text)
        # Remove digit character
        pattern_7 = r'\d+'
        text = re.sub(pattern_7, '', text)
        # Remove url start with http or https
        pattern_8 = r'(http:|https:)'
        text = re.sub(pattern_8, '', text)
        # Remove (\); ([); (])
        pattern_9 = r'[\\\]\[]'
        text = re.sub(pattern_9, '', text)
        # Remove character non ASCII
        pattern_10 = r'[^\x00-\x7f]'
        text = re.sub(pattern_10, '', text)
        # Remove character non ASCII
        pattern_11 = r'(\\u[0-9A-Fa-f]+)'
        text = re.sub(pattern_11, '', text)
        # Remove multiple whitespace
        pattern_12 = r'\s+'
        text = re.sub(pattern_12, ' ', text)
        # Remove whitespace at the first and end sentences
        text = text.rstrip()
        text = text.lstrip()
        return text
    df['Tweet'] = df['Tweet'].apply(cleansing)

    def replaceThreeOrMore(text):
        # Pattern to look for three or more repetitions of any character, including newlines (contoh goool -> gool).
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", text)

    json_response = {
        'status_code': "200",
        'description': "cleansing_data",
        'clean_tweet': df['Tweet'].apply(replaceThreeOrMore).to_list()
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run(debug=True)