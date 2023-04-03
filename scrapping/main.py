# from bs_opponents import get_opponents
# from bs_select_opponents import get_opponents
from requests import get
import json
from scrapping.wiki_fighters import get_fighter_info, get_opponents, get_opponents_with_info
import sys


def default():
    if len(sys.argv) == 1:
        raise Exception('missing argument ...')

    target = sys.argv[1]
    url = sys.argv[2]
    output = sys.argv[3]

    handler = None
    if target == 'ops':
        handler = get_opponents
    elif target == 'ops+info':
        handler = get_opponents_with_info
    elif target == 'info':
        handler = get_fighter_info

    response = get(url)
    results = handler(response.text)

    # print(opponents)

    # json_payload = json.dumps(results, ensure_ascii=False, indent=2)
    json_payload = json.dumps(results, indent=2)
    # print(opponents_json)

    with open(f"{output}.json", 'w', encoding='utf-8') as f:
        # f.write(json_payload.encode('ascii', 'ignore').decode('utf-8'))
        f.write(json_payload)
