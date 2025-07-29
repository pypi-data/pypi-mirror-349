import re
from typing import Dict, List

import requests
from lxml import html

from ipo_premium_client.exceptions import ElementNotFound


def parse_tables_from_url(url: str, xpaths: List[str]) -> List[Dict[str, Dict[str, str]]]:
    response = requests.get(url=url)
    response.raise_for_status()
    tables = []
    for xpath in xpaths:
        table = html.fromstring(response.text).xpath(xpath)
        if len(table) != 1:
            raise Exception('Failed to parse table')
        tables.append(parse_table(table[0]))
    return tables


def parse_table_from_url(url: str, xpath: str) -> Dict[str, Dict[str, str]]:
    response = requests.get(url=url)
    response.raise_for_status()
    table = html.fromstring(response.text).xpath(xpath)
    if len(table) != 1:
        raise Exception('Failed to parse table')
    return parse_table(table[0])


def parse_table(html_table) -> Dict[str, Dict[str, str]]:
    table = {}
    headers = [header.text_content() for header in html_table.findall('thead')[0].findall('tr')[-1].findall('th')][1:]

    html_rows = html_table.findall('tbody')[0].findall('tr')
    for html_row in html_rows:
        children = html_row.getchildren()
        row = {}

        if len(children) == 1:
            continue

        key = children[0].text_content()
        for grandchild in children[0].getchildren():
            if grandchild.tag == 'a':
                row['url'] = grandchild.attrib['href'].strip()
                key = grandchild.xpath('text()')
                key = key[0] if len(key) > 0 else grandchild.text_content()
                break

        for index, td in enumerate(children[1:]):
            if len(headers) <= index:
                continue
            k = remove_non_ascii(headers[index].strip())
            row[k] = remove_non_ascii(td.text_content().strip())

        table[remove_non_ascii(key)] = row

    return table


def parse_row_based_table_from_url(url: str, xpath: str) -> dict[str, str]:
    response = requests.get(url=url)
    response.raise_for_status()
    table = html.fromstring(response.text).xpath(xpath)
    if not len(table):
        raise ElementNotFound('Failed to parse table')
    return parse_row_based_table(table[0])


def parse_row_based_table(html_table) -> Dict[str, str]:
    table = {}
    table_body = html_table.findall('tbody')
    if len(table_body) != 1:
        raise ElementNotFound('Failed to parse table')
    rows = table_body[0].findall('tr')
    for row in rows:
        try:
            key, value = [td.text_content().strip() for td in row.findall('td')]
            table[key] = value
        except ValueError as e:
            print('Failed to parse row', e)
    return table


def is_blank(s: str) -> bool:
    return s is None \
        or s == '' \
        or s.casefold() == 'na'.casefold() \
        or s == '--'


def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]', "", text).strip()


def get_number_or_input(x):
    try:
        return float(x)
    except ValueError:
        return x


def parse_float(text):
    keep_list = '0123456789.'
    num_list = ''.join([x for x in text if x in keep_list])
    return float(num_list)
