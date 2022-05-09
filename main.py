# Поиск вакансий
import requests
import pprint
import json

url = 'https://api.hh.ru/vacancies'
data={}
data['vacance'] = []
data['static']=[]
vac=0
for i in range(10):
    params = {
        'text': 'python developer',
        # есть страницы т.к. данных много
        'page': i,
        'area': 1,
        'schedule': 'fullDay'
    }

    result = requests.get(url, params=params).json()
    for z in range(20):#len(result['items']):

        vac += 1
        data['vacance'].append({
            'name': result['items'][z]['name'],
            'url_vacancy': result['items'][z]['alternate_url'],
            'salary': result['items'][z]['salary'],
            'snippet': result['items'][z]['snippet'],
        })
    #pprint.pprint(result)
   # print(result['items'][0]['url'])
   # print(result['items'][0]['alternate_url'])
data['static'].append({
    'all_vacancies': result['found'],
    'vacancies found': vac
})
with open('hh_search.json', 'w') as f:
    f.write(json.dumps(data))
pprint.pprint(data)