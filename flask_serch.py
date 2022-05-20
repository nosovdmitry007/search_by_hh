from flask import Flask, render_template, request
from main import hh_serch
# from flask_json import FlaskJSON, JsonError, json_response, as_json
import json
import time
app = Flask(__name__)
# FlaskJSON(app)
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/form/", methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        hh_serch(request.form['query_string'], request.form['where'])
        # time.sleep(4)
        with open('hh_search.json', 'r', encoding='utf-8') as f:  # открыли файл с данными
            context = json.load(f)

        return render_template('results.html', **context)
    else:
        return render_template('form.html')


@app.route("/results/")
def results():
    with open('hh_search.json', 'r', encoding='utf-8') as f:  # открыли файл с данными
        context = json.load(f)


    return render_template('results.html', **context)



if __name__ == "__main__":
    app.run(debug=True)