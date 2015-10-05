import arrow
from datetime import datetime
from dateutil import tz
import requests
import todoist

from secrets import TODOIST_TOKEN, INBOX_PROJECT_ID, RULES

api = todoist.TodoistAPI(TODOIST_TOKEN)

request_url = 'https://api.todoist.com/API/getUncompletedItems?project_id=' + INBOX_PROJECT_ID
request_url += '&token=' + TODOIST_TOKEN
inbox_items = requests.get(request_url).json()

for inbox_item in inbox_items:
    for rule in RULES["due_time_by_prefix"]:
        prefix = rule[0]
        hour = rule[1]
        minute = rule[2]
        if inbox_item['content'].startswith(prefix):
            try:
                date_string = inbox_item['date_string']
                date_string = date_string.split(' ')[1:-2]
                arw = arrow.get(datetime.strptime(date_string, '%a %d %b %Y'), tz.gettz('US/Pacific'))
                arw = arw.replace(hour=hour, minute=minute)
                date_string = arw.format('MM/DD/YYYY @ HH:mm')
                
                item = api.items.get_by_id(inbox_item['id'])
                item.update(date_string=date_string)
                api.commit()
            except:
                print 'Failed on "%s"' % inbox_item['content']