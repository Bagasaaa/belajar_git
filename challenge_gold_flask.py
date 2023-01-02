import pandas as pd
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')

@app.route("/data_before_cleansing", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        csv_file = request.files.get("file")
        x_test = pd.read_csv("C:/Users/Acer/docs/binar_data_science/data.csv", encoding='latin-1')
        return x_test.to_html()
    return '''
    <!doctype html>
    <title>View .csv File Before Preprocessing (Cleansing)</title>
    <h1>View .csv File Before Preprocessing (Cleansing)</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''       

@app.route("/data_after_cleansing", methods=["GET", "POST"])
def text_processing():
    if request.method == "POST":
        tweet = request.form.getlist('tweet') # How to limit the tweet wanted to clean
    
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

    def replaceThreeOrMore(text):
        # Pattern to look for three or more repetitions of any character, including newlines (contoh goool -> gool).
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", text)

    json_response = {
        'library_to_clean_data': "RegEx",
        'data_before_cleansing': "data.csv",
        'description': "cleansing_df['Tweet']",
        'clean_tweet': df['Tweet'].apply(cleansing).apply(replaceThreeOrMore).to_list()
    }

    response_data = jsonify(json_response)
    return response_data

from flask import Flask, render_template, request, redirect, url_for
import re

@app.route("/", methods=['GET', 'POST'])
def clean():
    if request.method == 'POST':
        val1 = request.form['val1']
        val1 = str(val1)

        print(val1, type(val1))

        if val1 == object:
            val1 = re.sub(r'(user|rt|retweet)', '', val1)
            return val1
        return redirect(url_for("cleansing", clean=re.sub(r'(user|rt|retweet)', '', val1)))

    return render_template("index_2.html")

@app.route("/<clean>", methods=['GET'])
def cleansing(clean):
    return f'Cleansing result: {clean}'

if __name__ == '__main__':
    app.run(debug=True)