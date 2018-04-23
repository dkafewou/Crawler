# -*- coding: utf-8 -*-
from models import CompanyIndex, CompanyProfile, Contact, Address
import requests
from bs4 import BeautifulSoup
from datetime import date
import json
from utils import save_json_file


def crawl_companies_indexes(url):
    source_code = None
    index = {}
    companies_indexes = []
    per_page = 25
    row = 1
    while True:
        try:
            # get source code
            source_code = requests.get(url)
            break
        except requests.RequestException as e:
            print(e)
            continue

    # get text
    text = source_code.text
    beautiful_soup = BeautifulSoup(text, 'html.parser')
    table = beautiful_soup.find('table', {'id': 'members'})
    list_body = table.find('tbody')
    items = list_body.find_all('tr')
    for item in items:
        index['url'] = item.select_one('a[href^="http://eurocham-cambodia.org/member/"]').get('href')
        index['title'] = item.find_all('td')[1].text.strip()
        index['crawled_at'] = date.today().isoformat()

        if row % per_page == 0:
            page_no = (row // per_page)
        else:
            page_no = (row // per_page) + 1
        index['page_no'] = page_no
        print(page_no)

        companies_indexes.append(json.loads(CompanyIndex(index).to_json()))
        row += 1

    return companies_indexes


def get_companies_indexes():
    url = 'http://eurocham-cambodia.org/members-directory'
    data = crawl_companies_indexes(url)
    filename = 'company_index'
    save_json_file(data, filename)
