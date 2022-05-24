from flask import Flask, render_template, request
from main import hh_serch
# from flask_json import FlaskJSON, JsonError, json_response, as_json
import json
import time
import sqlite3
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

@app.route("/sql/")
def sql():

    conn = sqlite3.connect('HH_search.sqlite')
    cursor = conn.cursor()
    zapros = "select v.id, v.name, v.salary, v.about, v.link, s.skil, s.how_many_skil," \
             " p.name_search, p.where_search from vacancy v, skills_table s, vacancyskil vs, " \
             "params p where vs.vacancy_id=v.id and vs.skil_id=s.id"
    cursor.execute(zapros)
    context = cursor.fetchall()


    # with open('hh_search.json', 'r', encoding='utf-8') as f:  # открыли файл с данными
    #     context = json.load(f)


    return render_template('sql.html', context=context)

if __name__ == "__main__":
    app.run(debug=True)