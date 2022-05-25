from flask import Flask, render_template, request
from main import hh_serch
import json

import sqlite3
from orm import *
from sqlalchemy import create_engine,update
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


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

    return render_template('sql.html', context=context)


@app.route("/SQL_orm/")
def sql_orm():
    engine = create_engine('sqlite:///HH_search_orm.sqlite', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()



    context =  session.query(Vacancy.id, Vacancy.name, Vacancy.salary, Vacancy.about, Vacancy.link,
                           Skills_table.skil, Skills_table.how_many_skil,
                           Params.name_search, Params.where_search).filter((Vacancyskil.c.vacancy_id == Vacancy.id) &( Vacancyskil.c.skil_id == Skills_table.id)).all()


    return render_template('SQL_orm.html', context=context)

if __name__ == "__main__":
    app.run(debug=True)