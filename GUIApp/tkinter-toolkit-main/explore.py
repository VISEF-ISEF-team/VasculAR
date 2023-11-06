import os
import json

DIRPATH = os.path.join(os.path.dirname(__file__))
print(DIRPATH)

database = os.path.join(DIRPATH, "assets", "database.json")
if os.path.exists(database):
    with open(database) as f:
        data = json.load(f)
        for i in data.keys():
            print(f'{i} \n')