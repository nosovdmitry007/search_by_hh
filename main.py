# Поиск вакансий
import requests
import pprint
import json
import time
import sqlite3


def hh_serch(tex, param):

    url = 'https://api.hh.ru/vacancies'
    conn = sqlite3.connect('HH_search.sqlite')
    cursor = conn.cursor()
    #очистка бд
    cursor.execute('DELETE FROM skills_table;', )
    cursor.execute('DELETE FROM vacancyskil;', )
    cursor.execute('DELETE FROM params;', )
    cursor.execute('DELETE FROM vacancy;', )
    conn.commit()

    data = {}
    print(tex)
    print(param)
    data['params'] ={'serc':tex,'search_field': param}
    if param == "name":
        ser = 'В названии вакансии '
    elif param == "company_name":
        ser = 'В названии компании'
    elif param == "description":
        ser ='В описание'
    cursor.execute(f"insert into params (name_search,where_search) VALUES ('{tex}','{ser}')")
    conn.commit()

    data['vacance'] = []
    data['static'] = []
    data['key_skill'] = []
    data['skills'] = []
    vac = 0
    key = []

    for i in range(1):
        time.sleep(1)
        params = {
            'text': tex,
            'search_field': param,
            'page': i,
            'area': 1,
        }

        result = requests.get(url, params=params).json()
        #pprint.pprint(result)

        for z in range(20):
            try:

                data['vacance'].append({
                    'name': result['items'][z]['name'],
                    'url_vacancy': result['items'][z]['alternate_url'],
                    'salary': result['items'][z]['salary'],
                    'snippet': result['items'][z]['snippet'],
                    'skills': requests.get(result['items'][z]['url']).json()['key_skills']
                })
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
                try:
                    cursor.execute("insert into vacancy (name, salary, about, link) VALUES (?, ?, ?, ?)", (result['items'][z]['name'], zp, result['items'][z]['snippet']['responsibility'], result['items'][z]['alternate_url']))
                    conn.commit()
                except:
                    pass

                # print(cursor.fetchall())
                #ищем id вакансии в бд
                cursor.execute(f"select id from vacancy where link='{result['items'][z]['alternate_url']}'")

                id_vac = cursor.fetchall()[0][0]
                #цикл по скилам
                for skills_vac in requests.get(result['items'][z]['url']).json()['key_skills']:
                    skill_vac = skills_vac['name']
                    # print(skill_vac)
                    try:
                        cursor.execute(f"insert into skills_table (skil) VALUES ('{skill_vac}')")
                        conn.commit()
                    except:
                        pass
                    cursor.execute(f"select id from skills_table where skil='{skill_vac}'")
                    id_skill = cursor.fetchall()[0][0]
                    cursor.execute("insert into vacancyskil (vacancy_id, skil_id) VALUES (?, ?)", (id_vac, id_skill))
                    conn.commit()

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
        # добавляем в бд количество скилов
        for k in key_skills:
            cursor.execute(f"select id from skills_table where skil='{k}'")
            id_skil = cursor.fetchall()[0][0]
            cursor.execute(f"update skills_table set how_many_skil = '{key_skills[k]}' where  id = {id_skil}")
            conn.commit()
        #print(key_skills)
        # cursor.execute(f"insert into params (name_search,where_search) VALUES ('{tex}','{param}')")
        # conn.commit()

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
        # pprint.pprint(data)
    else:
        data['luck'] = 'false'
        with open('hh_search.json', "w", encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))



    cursor.execute("select v.id, v.name, v.salary, v.about, v.link, s.skil, s.how_many_skil, p.name_search, p.where_search from vacancy v, skills_table s, vacancyskil vs, params p where vs.vacancy_id=v.id and vs.skil_id=s.id")

    print(cursor.fetchall())