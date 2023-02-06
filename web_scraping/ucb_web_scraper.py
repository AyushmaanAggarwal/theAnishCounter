import requests
import json
from bs4 import BeautifulSoup


def get_course_information(url_string):
    try:
        page = requests.get(url_string)
        soup = BeautifulSoup(page.content, 'html.parser')
        div1 = soup.find(class_="handlebarData theme_is_whitehot")
    except requests.ConnectionError:
        return None
    j = json.loads(div1['data-json'])
    unparsed_info = j['meetings'][0]
    return {'week_days': unparsed_info['meetsDays'], 'start': unparsed_info['startTime'],
            'end': unparsed_info['endTime'], 'location': unparsed_info['location']['description']}