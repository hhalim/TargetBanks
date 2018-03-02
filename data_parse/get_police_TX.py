# -*- coding: utf-8 -*-
from parse_police import parse_and_insert

#STATE = TX
url='https://www.policeone.com/law-enforcement-directory/Texas-Agencies/Police-Departments/'
page_start = 2
page_end = 27
parse_and_insert(url, page_start, page_end)

