import AccountCredentials
import requests

token = AccountCredentials.TODOIST_API_TOKEN

fname = raw_input('Enter file name: ')
project_id = raw_input('Project ID: ')
priority = raw_input('Priority (1 to 4, 4 highest): ')
indent = raw_input('Indent (1 to 4, 1 top-level): ')
date_string = raw_input('Date (string) (e.g. friday at 11pm): ')

with open(fname) as f:
    content = f.readlines()

for item in content:
    request = 'https://api.todoist.com/API/addItem?content=' + item + '&token=' + token
    if project_id:
        request += '&project_id=' + project_id
    if priority:
        request += '&priority=' + priority
    if indent:
        request += '&indent=' + indent
    if date_string:
        request += '&date_string=' + date_string
    r = requests.get(request)