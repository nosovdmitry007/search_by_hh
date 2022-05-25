# Поиск вакансий
import requests
import pprint
import json
import time
import sqlite3
from orm import *
from sqlalchemy import create_engine,update
from sqlalchemy.orm import sessionmaker



def hh_serch(tex, param):
#подключение к бд orm
    engine = create_engine('sqlite:///HH_search_orm.sqlite', echo=False)
    Session = sessionmaker(bind=engine)
    # create a Session
    session = Session()

#подключение бд
    url = 'https://api.hh.ru/vacancies'
    conn = sqlite3.connect('HH_search.sqlite')
    cursor = conn.cursor()
    #очистка бд
    cursor.execute('DELETE FROM skills_table;', )
    cursor.execute('DELETE FROM vacancyskil;', )
    cursor.execute('DELETE FROM params;', )
    cursor.execute('DELETE FROM vacancy;', )
    conn.commit()


    session.query(Vacancy).delete(synchronize_session='fetch')
    session.query(Params).delete(synchronize_session='fetch')
    session.query(Vacancyskil).delete(synchronize_session='fetch')
    session.query(Skills_table).delete(synchronize_session='fetch')

    session.commit()

    data = {}

#sqlite
    if param == "name":
        ser = 'В названии вакансии '
    elif param == "company_name":
        ser = 'В названии компании'
    elif param == "description":
        ser ='В описание'
    cursor.execute(f"insert into params (name_search,where_search) VALUES ('{tex}','{ser}')")
    conn.commit()

    session.add_all([Params(tex,ser)])
#json
    data['params'] ={'serc':tex,'search_field': param}
    data['vacance'] = []
    data['static'] = []
    data['key_skill'] = []
    data['skills'] = []
    vac = 0
    key = []
    skills=[]
    for i in range(1):
        time.sleep(1)
        params = {
            'text': tex,
            'search_field': param,
            'page': i,
            'area': 1,
        }

        result = requests.get(url, params=params).json()

        for z in range(20):
            try:
                #json
                data['vacance'].append({
                    'name': result['items'][z]['name'],
                    'url_vacancy': result['items'][z]['alternate_url'],
                    'salary': result['items'][z]['salary'],
                    'snippet': result['items'][z]['snippet'],
                    'skills': requests.get(result['items'][z]['url']).json()['key_skills']
                })

                #sqllite
                if result['items'][z]['salary']:
                    if result['items'][z]['salary']['from'] :

                        zp1='от ' + str(result['items'][z]['salary']['from'])
                    else:
                        zp1=''
                    if result['items'][z]['salary']['to']:
                       zp2 = ' до ' + str(result['items'][z]['salary']['to'])
                    else:
                        zp2=''
                    zp=zp1 + zp2 + ' ' + result['items'][z]['salary']['currency']
                else:
                    zp = 'Не указана'
                    #sql

                cursor.execute("insert into vacancy (name, salary, about, link) VALUES (?, ?, ?, ?)", (result['items'][z]['name'], zp, result['items'][z]['snippet']['responsibility'], result['items'][z]['alternate_url']))
                conn.commit()

                #orm
                session.add_all([Vacancy(result['items'][z]['name'], zp, result['items'][z]['snippet']['responsibility'], result['items'][z]['alternate_url'])])
                session.commit()

                #ищем id вакансии в бд
                cursor.execute(f"select id from vacancy where link='{result['items'][z]['alternate_url']}'")

                id_vac = cursor.fetchall()[0][0]

                id_vac_orm = session.query(Vacancy.id).filter(Vacancy.link == result['items'][z]['alternate_url']).first()
                id_vac_orm = id_vac_orm[0]
                #цикл по скилам
                for skills_vac in requests.get(result['items'][z]['url']).json()['key_skills']:
                    skill_vacancy = skills_vac['name']
                    # print(skill_vac)

                    if skill_vacancy not in skills:
                        skills.append(skill_vacancy)
                        #sql
                        cursor.execute(f"insert into skills_table (skil) VALUES ('{skill_vacancy}')")
                        conn.commit()

                        #orm
                        session.add_all([Skills_table(skill_vacancy, "")])
                        session.commit()

                    cursor.execute(f"select id from skills_table where skil='{skill_vacancy}'")
                    id_skill = cursor.fetchall()[0][0]

                    id_skill_orm = session.query(Skills_table.id).filter(Skills_table.skil == skill_vacancy).first()
                    id_skill_orm = id_skill_orm[0]
                    cursor.execute("insert into vacancyskil (vacancy_id, skil_id) VALUES (?, ?)", (id_vac, id_skill))
                    conn.commit()

                    session.execute(Vacancyskil.insert().values(vacancy_id=id_vac_orm,skil_id=id_skill_orm))
                    session.commit()


                url = result['items'][z]['url']
                result1 = requests.get(url).json()

                key = key+result1['key_skills']
                vac += 1
            except:
                pass
        skills = []
        for k in range(len(key)):
            skills.append(key[k]['name'])

        key_skills = {}
        for item in skills:

            if item in key_skills:
                key_skills[item] += 1
            else:
                key_skills[item] = 1
        # добавляем в бд количество скилов sqlite
        for k in key_skills:
            cursor.execute(f"select id from skills_table where skil='{k}'")
            id_skil = cursor.fetchall()[0][0]
            cursor.execute(f"update skills_table set how_many_skil = '{key_skills[k]}' where  id = {id_skil}")
            conn.commit()

            stmt = update(Skills_table).where(Skills_table.skil == k).values(how_many_skil=key_skills[k]). \
                execution_options(synchronize_session="fetch")

            session.execute(stmt)
            session.commit()

#json
        result3 = sorted(key_skills.items(), key=lambda x: x[1], reverse=True)

        data['key_skill'] = result3
        data['static'].append({
            'all_vacancies': result['found'],
            'vacancies found': vac
        })

    if len(data['vacance'])>1:
        data['luck'] = 'true'
        with open('hh_search.json', "w", encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
    else:
        data['luck'] = 'false'
        with open('hh_search.json', "w", encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
