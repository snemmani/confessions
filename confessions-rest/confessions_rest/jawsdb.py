"""This file will provide the necessary databse settings"""

import os
import re


class JawsDBConnection:
    def __init__(self):
        url = os.environ['JAWSDB_MARIA_URL']
        match = re.search('mysql://(.*):(.*)@(.*):(.*)/(.*)', url)
        self.username = match.group(1)
        self.password = match.group(2)
        self.host = match.group(3)
        self.port = match.group(4)
        self.database = match.group(5)
