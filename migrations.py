# -*- coding: utf-8 -*-
from pymongo import MongoClient
from utils import read_json_file
import sys
import settings

client = MongoClient(settings.DATABASE_HOST)
db = client['eurocham_cambodia']


def migrate(number):
    if number == '1':
        company_index = db['company_index']
        company_index_data = read_json_file('company_index.json')
        results = company_index.insert_many(company_index_data)
        print(results.inserted_ids)

    elif number == '2':
        company_profile = db['company_profile']
        company_profile_data = read_json_file('company_profile.json')
        results = company_profile.insert_many(company_profile_data)
        print(results.inserted_ids)

    else:
        print('no_migration_found')

if len(sys.argv) < 2:
    print('no_migration_number_provided')
    exit()

migration_number = sys.argv[1]
migrate(migration_number)
