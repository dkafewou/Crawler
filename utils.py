# -*- coding: utf-8 -*-
import json
from selenium import webdriver
import re


def save_json_file(data, filename):
    # save data in json file
    with open(filename + '.json', 'w', encoding='utf8') as outfile:
        json.dump(data, outfile)


def read_json_file(filename):
    # read json file and return json object
    data = []
    with open(filename, 'r') as outfile:
        data = json.load(outfile)
    return data


def web_driver():
    # web driver for headless chrome
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('window-size=1200x600')

    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    return driver


def get_emails(source):
    # find email in source using regex match
    regex = re.compile('[\w\.-]+@[\w\.-]+\.\w+')
    return [email for email in re.findall(regex, source)]
