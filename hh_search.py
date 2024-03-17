import requests
import re
import json
from bs4 import BeautifulSoup
from fake_headers import Headers



headers_generator = Headers(os="win", browser="firefox")
BASE_URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
job_openings = []
count_clicks = 0
count_true = 0
count_false = 0

for i in range(0, 5):
    response = requests.get(f'{BASE_URL}&page={i}', headers=headers_generator.generate())
    main_html_data = response.text
    soup = BeautifulSoup(main_html_data, 'lxml')
    vacancies = soup.find_all('div', class_='serp-item')

    for vacancy in vacancies:
        count_clicks += 1
        link = vacancy.find('a', class_='bloko-link')
        link_relative = link['href']

        salary = vacancy.find('span', class_='bloko-header-section-2')
        if salary:
            salary = salary.text.strip().replace('\u202F', ' ')
        else:
            salary = 'Не указана'

        company = vacancy.find('div', class_='vacancy-serp-item__meta-info-company')
        if company:
            company = company.text.strip().replace('ООО\xa0', '')
        else:
            company = 'Не указана'

        city = vacancy.find('div', class_='vacancy-serp-item-company')
        if city:
            pattern = 'Москва|Санкт-Петербург'
            city = re.findall(pattern, city.text)
            if city:
                city = city[0]
        else:
            city = 'Не указан'

        response = requests.get(f'{link_relative}', headers=headers_generator.generate())
        main_html_data = response.text
        soup = BeautifulSoup(main_html_data, 'lxml')
        description_tag = soup.find('div', class_='bloko-tag-list')
        if description_tag:
            description_tags = description_tag.find_all('span', class_='bloko-tag__section bloko-tag__section_text')
            description_list = []
            for tag in description_tags:
                description = tag.text.lower()
                description_list.append(description)

            if 'django' in description_list or 'flask' in description_list:
                job_openings.append({
                    'link': link_relative,
                    'salary': salary,
                    'company': company,
                    'city': city,
                })
                count_true += 1
            else:
                count_false += 1

with open('vacancies.json', 'w', encoding='utf-8') as file:
    json.dump(job_openings, file, ensure_ascii=False, indent=4)


print(f'Подходящих вакансий записано: {count_true}')
print(f'Вакансий отсеяно: {count_false}')
