from parsel import Selector
from requests import get
import re


def get_opponents_with_info(html):
    opponents = get_opponents(html)
    for opponent in opponents:
        if link := opponent.get('link'):
            res = get(link)
            # print(res.status_code)
            opponent['info'] = get_fighter_info(res.text)

    return opponents


def get_opponents(html):
    selector = Selector(text=html)

    # soup.find_all('table', attrs={'class': "wikitable"})

    matches = selector.xpath('//table[@class="wikitable"]')[0]
    # print(tables)
    trs = matches.xpath('.//tr')

    opponents = []

    for tr in trs[1:]:
        opponent = {
            'link': None,
            'name': None,
            'outcome': None
        }
        opponent_node = tr.xpath('./td[3]')
        outcome = tr.xpath('./td[1]/text()').get()
        anchors = opponent_node.xpath('a')

        # print(outcome)
        if len(anchors) == 1:
            a = anchors[0]
            href = a.xpath("@href").get()
            opponent['link'] = f"https://en.m.wikipedia.org{href}"
            opponent_name = a.xpath('text()').get()

        else:
            opponent_name = opponent_node.xpath("text()").get()

            # if opponent_name is None:

        opponent['name'] = opponent_name.strip('\n')
        opponent['outcome'] = outcome.strip('\n')

        opponents.append(opponent)

    return opponents


def get_fighter_info(html):
    selector = Selector(text=html)
    fighter_details = {
        'name': None,
        'image': None,
        'born': None,
        'native_name': None,
        'nick_name': None,
        'nationality': None,
        'height': None,
        'weight': None,
        'division': None,
        'reach': None,
        'style': None,
        'stance': None,
        'fight_out_of': None,
        'team': None,
        'trainer': None,
        'rank': None,
        'years_active': None,
        'total': None,
        'wins': None,
        'by_knockout': None,
        'by_submission': None,
        'by_decision': None,
        'losses': None,
        'website': None
    }

    trs = selector.xpath('.//table[@class="infobox vcard"]/tbody/tr')
    fighter_details['name'] = trs[0].xpath('./th/span/text()').get()
    fighter_details['image'] = f"https://en.m.wikipedia.org{trs[1].xpath('./td/a/@href').get()}"

    for tr in trs[2:]:
        key: str = tr.xpath('./th/text()').get()
        val = tr.xpath('./td/text()').get()

        if key is None or val is None:
            continue

        if key.startswith('Nickname'):
            fighter_details['nick_name'] = val

        elif key.startswith('Nationality'):
            fighter_details['nationality'] = val

        elif key.startswith('Height'):
            match = re.search(
                '(?P<imperic>\d.ft \d{1,2}.in) \((?P<metric>[\d.]+.c?m)\)', val)
            # parts = val.split('(')
            # imp = parts[0].strip(' ')
            # metric = parts[1].strip(')')
            # fighter_details['height'] = {
            #     'imperial': imp.replace('\u00a0', ' '),
            #     'metric': metric.replace('\u00a0', ' ')
            # }
            if match is None:
                print('Failed height match !!!', val)
                continue

            fighter_details['height'] = {
                'imperial': match.group('imperic').replace('\u00a0', ' '),
                'metric': match.group('metric').replace('\u00a0', ' '),
            }
        elif key.startswith('Weight'):
            match = re.search(
                '(?P<imperic>\d{1,3}.lb) \((?P<metric>\d{1,3}.kg); (?P<eng>[\d.]+.st(?: \d+.lb)?)+\)', val)

            if match is None:
                print('Failed weight match: ', val)
                continue

            fighter_details['weight'] = {
                'imperial': match.group('imperic').replace('\u00a0', ' '),
                'metric': match.group('metric').replace('\u00a0', ' '),
                'eng': match.group('eng').replace('\u00a0', ' '),
            }
        elif key.startswith('Born'):
            born_section = tr.xpath('./td').get()

            match = re.search(
                '<\/span>(?P<date>[\w ,]+)<span', born_section)
            if match is None:
                print('Failed born match: ', born_section)
                continue

            print('match: ', match.group('date'))

    # fighter_details['name'] = trs[0].xpath('./th/span/text()').get()
    # fighter_details['profile_pic'] = trs[1].xpath('./td/a/@href').get()
    # fighter_details['born'] = trs[2].xpath('./td/text()').get()
    # fighter_details['native_name'] = trs[3].xpath('./td/span/text()').get()
    # fighter_details['nick_name'] = trs[4].xpath('./td/text()').get()
    # fighter_details['nationality'] = trs[5].xpath('./td/text()').get()
    # fighter_details['height'] = trs[6].xpath('./td/text()').get().strip('\xa0')
    return fighter_details
