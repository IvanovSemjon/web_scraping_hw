from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import json


def wait_element(browser, delay_seconds=1, by=By.TAG_NAME, value=None):
    return WebDriverWait(browser, delay_seconds).until(
        expected_conditions.presence_of_element_located((by, value))
    )


chrome_webdriver_path = ChromeDriverManager().install()
browser_service = Service(executable_path=chrome_webdriver_path)
options = Options()
options.add_argument("--headless")
browser = Chrome(service=browser_service, options=options)


browser.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2")
browser.maximize_window()

vacancy_list = wait_element(browser, 1, By.XPATH, '//*[@id="a11y-main-content"]')
vacancyes = vacancy_list.find_elements(By.TAG_NAME, 'serp-item vacancy-serp-item_clickme serp-item_link')
vacancies = []

for vacancy_element in vacancyes:
    vacancy_link = wait_element(vacancy_element, 1, By.TAG_NAME, "a").get_attribute("href")
    vacancy_title = wait_element(vacancy_element, 1, By.CLASS_NAME, "vacancy-serp-item__title").text
    vacancy_company = wait_element(vacancy_element, 1, By.CLASS_NAME, "vacancy-serp-item__meta-info").text
    vacancy_salary = wait_element(vacancy_element, 1, By.CLASS_NAME, "vacancy-serp-item__compensation").text
    vacancy_description = wait_element(vacancy_element, 1, By.XPATH, '//span[@data-qa="bloko-tag__text"]').text

    if "Django" in vacancy_description or "Flask" in vacancy_description:
        vacancy = {
            "link": vacancy_link,
            "title": vacancy_title,
            "company": vacancy_company,
            "salary": vacancy_salary,
        }
        vacancies.append(vacancy)

with open("vacancies.json", "w") as f:
    json.dump(vacancies, f, indent=4)


browser.close()
