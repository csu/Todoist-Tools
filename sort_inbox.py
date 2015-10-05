import arrow
from datetime import datetime
from dateutil import tz
import requests
import todoist
from secrets import TODOIST_TOKEN, INBOX_PROJECT_ID

api = todoist.TodoistAPI(TODOIST_TOKEN)

request_url = 'https://api.todoist.com/API/getUncompletedItems?project_id=' + INBOX_PROJECT_ID
request_url += '&token=' + TODOIST_TOKEN
inbox_items = requests.get(request_url).json()

for inbox_item in inbox_items:
    if inbox_item['content'].startswith('CSE 333'):
        item = api.items.get_by_id(inbox_item['id'])
        date_string = inbox_item['date_string']
        date_string = date_string.split(' ')[1:-2]
        arw = arrow.get(datetime.strptime('Fri 9 Oct 2015', '%a %d %b %Y'), tz.gettz('US/Pacific'))
        arw = arw.replace(hour=11, minute=15)
        date_string = arw.format('MM/DD/YYYY @ HH:mm')
        # due_date_utc = arw.to('utc').format('YYYY-MM-DDTHH:mm')
        
        item.update(date_string=date_string)
        api.commit()