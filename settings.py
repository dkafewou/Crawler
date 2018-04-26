# -*- coding: utf-8 -*-
import os

# setting up mongodb host
DEFAULT_DATABASE_HOST = 'mongodb://localhost:27017/'
DATABASE_HOST = os.environ['DATABASE_HOST'] if (os.environ.get('DATABASE_HOST') is not None) else DEFAULT_DATABASE_HOST
