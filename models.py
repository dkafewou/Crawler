# -*- coding: utf-8 -*-
import json
from datetime import date


class CompanyIndex:
    """
    Class CompanyIndex to manipulate company index data
    """

    def __init__(self, row):
        self.page_no = row.get('page_no')
        self.url = row.get('url')
        self.title = row.get('title')
        # set crawled_at to today if date is not passing as parameter
        self.crawled_at = row.get('crawled_at') if (row.get('crawled_at') is not None) else date.today().isoformat()

    def to_json(self):
        """
        CompanyIndex serializing method
        :return: json object of the instance
        """
        return json.dumps(self, default=lambda c: c.__dict__, indent=4)


class CompanyProfile:
    """
    Class CompanyProfile to manipulate company profile data
    """

    def __init__(self, row):
        self.uid = row.get('uid')
        self.created_at = row.get('created_at')
        self.company_name = row.get('company_name')
        self.company_logo = row.get('company_logo')
        self.company_address = row.get('company_address')
        self.company_phones = row.get('company_phones')
        self.company_emails = row.get('company_emails')
        self.company_website = row.get('company_website')
        self.company_description = row.get('company_description')
        self.company_contacts = row.get('company_contacts')

    def to_json(self):
        """
        CompanyProfile serializing method
        :return: json object of the instance
        """
        return json.dumps(self, default=lambda c: c.__dict__, indent=4)


class Address:
    """
    Class Address to manipulate Address data
    """

    def __init__(self, row):
        self.full_name = row.get('full_name')
        self.street = row.get('street')
        self.city = row.get('city')
        self.state = row.get('state')

    def to_json(self):
        """
        Address serializing method
        :return: json object of the instance
        """
        return json.dumps(self, default=lambda a: a.__dict__, indent=4)


class Contact:
    """
    Class Contact to manipulate Contact data
    """
    def __init__(self, row):
        self.name = row.get('contact_name')
        self.designation = row.get('contact_designation')
        self.email = row.get('contact_email')
        self.phone = row.get('contact_phone')
        self.profile_picture = row.get('contact_profile_picture')

    def to_json(self):
        """
        Contact serializing method
        :return: json object of the instance
        """
        return json.dumps(self, default=lambda c: c.__dict__)
