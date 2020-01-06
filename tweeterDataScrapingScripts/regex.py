# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 19:47:37 2019

@author: ravik
"""

import re
import sys

regex = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
with open(r"C:\Users\ravik\OneDrive\Desktop\usa1.json") as file:
    con = file.read()
    regex.sub(r'', con)