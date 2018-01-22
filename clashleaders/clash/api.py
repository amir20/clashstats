import asyncio
import logging
import os
from urllib.parse import quote

import aiohttp
import requests

API_TOKEN = os.getenv('API_TOKEN')
HEADERS = {'authorization': 'Bearer ' + API_TOKEN}
logger = logging.getLogger(__name__)


class ClanNotFound(Exception):
    pass


async def __fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            return await response.json()


def __get_all(urls):
    loop = asyncio.get_event_loop()
    futures = [__fetch(url) for url in urls]
    responses = loop.run_until_complete(asyncio.gather(*futures))
    return responses


def find_clan_by_tag(tag):
    if not tag.startswith('#'):
        tag = '#' + tag
    logger.info(f"Fetching clan from API {tag}.")
    r = requests.get('https://api.clashofclans.com/v1/clans/' + quote(tag), headers=HEADERS)

    if r.status_code != 200:
        raise ClanNotFound('Clan not found')

    return r.json()


def search_by_name(name, limit=10):
    logger.info(f"Searching for clan name '{name}'.")
    r = requests.get('https://api.clashofclans.com/v1/clans', headers=HEADERS, params={'name': name, 'limit': limit})

    if r.status_code != 200:
        return []
    else:
        return r.json()['items']


def clan_warlog(tag):
    if not tag.startswith('#'):
        tag = '#' + tag
    logger.info(f"Fetching clan warlog from API {tag}.")
    r = requests.get(f"https://api.clashofclans.com/v1/clans/{quote(tag)}/warlog", headers=HEADERS)

    if r.status_code != 200:
        raise ClanNotFound('Clan not found')

    return r.json()


def fetch_all_players(clan):
    logger.info(f"Fetching all player stats for {clan['tag']}.")
    tags = [member['tag'] for member in clan['memberList']]
    urls = ['https://api.clashofclans.com/v1/players/' + quote(tag) for tag in tags]
    return __get_all(urls)
