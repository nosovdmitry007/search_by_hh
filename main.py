# Поиск вакансий
import requests
import pprint
import json
import time

def hh_serch(tex, param):

    url = 'https://api.hh.ru/vacancies'

    data = {}
    print(tex)
    print(param)
    data['params'] ={'serc':tex,'search_field': param}
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
        pprint.pprint(result)

        for z in range(20):
            try:

                data['vacance'].append({
                    'name': result['items'][z]['name'],
                    'url_vacancy': result['items'][z]['alternate_url'],
                    'salary': result['items'][z]['salary'],
                    'snippet': result['items'][z]['snippet'],
                    'skills': requests.get(result['items'][z]['url']).json()['key_skills']
                })
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

        result3 = sorted(key_skills.items(), key=lambda x: x[1], reverse=True)

        # data['skills'].append(key)
        data['key_skill'] = result3
        data['static'].append({
            'all_vacancies': result['found'],
            'vacancies found': vac
        })

    if len(data['vacance'])>1:
        data['luck'] = 'true'
        with open('hh_search.json', "w", encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
        pprint.pprint(data)
    else:
        data['luck'] = 'false'
        with open('hh_search.json', "w", encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))

