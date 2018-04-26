# -*- coding: utf-8 -*-
from models import CompanyIndex, CompanyProfile, Contact, Address
import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import json
import time
from utils import save_json_file, web_driver, get_emails
from selenium import common
from multiprocessing import Pool


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


def crawl_companies_profiles(index):
    profile = {'uid': index['url']}
    if profile['uid'] in ['http://eurocham-cambodia.org/member/413/', 'http://eurocham-cambodia.org/member/428/']:
        return None

    profile['company_name'] = index['title']
    if profile['uid'] == 'http://eurocham-cambodia.org/member/391/':
        profile['company_name'] = 'PPCBank'
    profile['created_at'] = index['crawled_at']
    driver = None
    while True:
        try:
            # set web driver
            driver = web_driver()
            # set up the url for chrome
            driver.get(profile['uid'])
            time.sleep(10)
            break
        except common.exceptions.WebDriverException as e:
            print(e)
            continue
    # get plain text
    text = driver.page_source
    driver.quit()
    # pulling data
    beautiful_soup = BeautifulSoup(text, 'html.parser')

    contact_list = []
    phone_list = []
    address = {}

    content = beautiful_soup.find('section', {'id': 'content'})
    if content is not None:
        post_content = content.find('div', {'class': 'postcontent nobottommargin clearfix'})
        if post_content is not None:
            media = post_content.find('div', {'class': 'col-sm-3 col-md-3'})
            if media is not None:
                logo_link = media.select_one('img[src^="http://eurocham-cambodia.org/images/members/logos/"]')
                if logo_link is not None:
                    profile['company_logo'] = logo_link.get('src')
            content_infos = post_content.find('div', {'class': 'col-sm-9 col-md-8'})
            if content_infos is not None:
                info_list = content_infos.find_all('div', {'class': 'col-sm-12 col-md-6'})
                for item in info_list:
                    if item.find('ul', {'class': 'iconlist'}) is not None:
                        icon_list = item.find('ul', {'class': 'iconlist'})
                        m_list = icon_list.find_all('li')
                        for li in m_list:
                            if li.find('i', {'class': 'icon-phone'}):
                                if li.text.strip() not in ['', '-']:
                                    phones = re.split(r'\([^0-9]+\) \/|\([^0-9]+\)|[^0-9]+:|\s[^0-9]+\s\/*',
                                                      li.text.strip())
                                    for phone in phones:
                                        if re.match(r'[\+\d+|\(\d+|\d+]+.?[\d+]*', phone.strip()):
                                            if len(phone.strip()) <= 7:
                                                limit = 2 * len(phone.strip()) + 3
                                                phone = li.text.strip()[:-limit] + phone.strip()
                                            phone_list.append(phone.strip())
                                    profile['company_phones'] = phone_list
                            elif li.find('i', {'class': 'icon-mail'}):
                                if li.text.strip() not in ['', '-']:
                                    if len(get_emails(li.text.strip())) > 0:
                                        emails = get_emails(li.text.strip())
                                        profile['company_emails'] = emails
                            elif li.find('i', {'class': 'icon-globe'}):
                                if li.text.strip() not in ['', '-']:
                                    profile['company_website'] = li.text.strip()

                    elif item.text.strip() not in ['', '-']:
                        address['full_name'] = item.text.strip()
                        profile['company_address'] = json.loads(Address(address).to_json())

            content_desc = beautiful_soup.find_all('div', {'class': 'col-sm-12'})
            for col in content_desc:
                if col.find('div', {'class': 'fancy-title title-double-border title-center'}) is not None:
                    if col.find('div',
                                {'class': 'fancy-title title-double-border title-center'}).text.strip() == 'People':
                        contact_blocs = col.find_all('div', {'class': 'col-sm-3 col-xs-6'})
                        for item in contact_blocs:
                            contact = {}
                            profile_picture = item.select_one('img[src^="http://eurocham-cambodia.org/images/pages/"]')
                            if profile_picture is not None:
                                contact['contact_profile_picture'] = profile_picture.get('src')
                            modal = item.find('div', {'class': 'modal-block mfp-hide container'})
                            if modal is not None:
                                item.find('div', {'class': 'modal-block mfp-hide container'}).extract()
                                if modal.find('h3').text.strip() != '':
                                    contact['contact_name'] = modal.find('h3').text.strip()
                                if modal.find('h5').text.strip() != '':
                                    contact['contact_designation'] = modal.find('h5').text.strip()
                            contact_emails = get_emails(item.text)
                            if len(contact_emails) > 0:
                                contact['contact_email'] = contact_emails[0]
                            if len(list(item.stripped_strings)) > 0:
                                for text in list(item.stripped_strings):
                                    if re.match(r'^[\+\d+|\(\d+|\d+]+.*[\d+]', text):
                                        contact['contact_phone'] = text.strip()
                                        break

                            contact_list.append(json.loads(Contact(contact).to_json()))
                        profile['company_contacts'] = contact_list
                elif col.text.strip() not in ['', '-']:
                    profile['company_description'] = col.text.strip()

    print(profile['uid'])
    return json.loads(CompanyProfile(profile).to_json())


def get_companies_data():
    # get companies indexes data and save to company_index.json
    url = 'http://eurocham-cambodia.org/members-directory'
    indexes = crawl_companies_indexes(url)
    filename = 'company_index'
    save_json_file(indexes, filename)

    with Pool(10) as p:  # Multiprocessing 10 in row
        profiles = [profile for profile in p.map(crawl_companies_profiles, indexes) if profile is not None]
    profile_filename = 'company_profile'
    save_json_file(profiles, profile_filename)
    print('Crawled European Chamber of Commerce in Cambodia successfully')

