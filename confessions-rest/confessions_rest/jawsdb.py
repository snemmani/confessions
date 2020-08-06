"""This file will provide the necessary databse settings"""

import os
import re


class JawsDBConnection:
    def __init__(self):
        url = os.environ['DATABASE_URL']
        match = re.search('mysql://(.*):(.*)@(.*):(.*)/(.*)', url)
        self.username = match.group(1)
        self.password = match.group(1)
        self.host = match.group(1)
        self.port = match.group(1)
        self.database = match.group(1)
