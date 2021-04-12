import ssl
import urllib.request
import urllib.parse

from prettytable import PrettyTable
from bs4 import BeautifulSoup
from random import choice

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

random_player = choice(list(open('players.txt', encoding='utf-8'))).replace('\n', '')

url = 'https://en.wikipedia.org/wiki/' + urllib.parse.quote(random_player)
html = urllib.request.urlopen(url, context=ctx)


def parse_html(page):
    soup = BeautifulSoup(page.read(), 'html.parser')
    table_wiki = soup.find('table', {'class': 'infobox vcard'})

    result = []
    for tr in table_wiki.find_all('tr'):
        if tr.find('th'):
            title = tr.find('th').text.replace('\n', '')
            info = [i.text.replace('\n', '') for i in tr.find_all('td')]

            if len(title) < 20:
                result.append((title, '|'.join(info)))

    return result


def process_data(res):
    table = PrettyTable()
    go_next, header = False, False

    for k, v in res:

        if 'National' in k or 'Honours' in k:
            go_next = False

        if go_next:
            if header:
                table_header = [k]
                for val in v.split('|'):
                    table_header.append(val)
                table.field_names = table_header
                header = False
            else:
                table_row = [k]
                for val in v.split('|'):
                    table_row.append(val)
                table.add_row(table_row)

        if 'Senior career' in k:
            go_next, header = True, True

    print(table)
    return table


def gen_player():
    if html.getcode() == 200:
        result = parse_html(html)
        player_stat = process_data(result)

        return player_stat

    elif html.getcode() == 404:
        print("Page not found!")
