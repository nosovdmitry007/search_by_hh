# Поиск вакансий
import requests
import pprint
import json
import time

url = 'https://api.hh.ru/vacancies'

data = {}

data['vacance'] = []
data['static'] = []
data['key_skill'] = []
vac=0
key=[]
for i in range(1):

    time.sleep(1)
    params = {
        'text': 'python developer',
        # есть страницы т.к. данных много
        'page': i,
        'area': 1,
        'schedule': 'fullDay'
    }

    result = requests.get(url, params=params).json()
    for z in range(20):
        vac += 1
        data['vacance'].append({
            'name': result['items'][z]['name'],
            'url_vacancy': result['items'][z]['alternate_url'],
            'salary': result['items'][z]['salary'],
            'snippet': result['items'][z]['snippet'],
        })
        url = result['items'][z]['url']
        result1 = requests.get(url).json()

        key = key+result1['key_skills']

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

data['key_skill'] = result3
data['static'].append({
    'all_vacancies': result['found'],
    'vacancies found': vac
})
with open('hh_search.json', 'w') as f:
    f.write(json.dumps(data))
pprint.pprint(data)