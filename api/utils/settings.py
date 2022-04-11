import json


__settings = json.load(open('../src/settings.json', 'r'))
locals().update(__settings)