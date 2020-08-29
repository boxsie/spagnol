import requests
import json

from lxml import html
from urllib.parse import urlparse

CONJUGATION_BASE_URL = 'https://www.linguasorb.com/spanish/verbs/conjugation/'

class Scraper(object):
    def get_verb_list(self, verb_url, page_count=None):
        print('Preparing to get verbs...')
        print(f'Connecting to {verb_url}')

        verbs = []
        loop_count = page_count if page_count else 1

        for page_number in range(loop_count):
            full_url = verb_url if not page_count else f'{verb_url}{page_number}'

            print('Downloading page', end='...')
            page_as_text = requests.get(full_url)
            html_page = html.fromstring(page_as_text.content)
            page_verb_elements = html_page.xpath('//span[@class="vIrreg"]')

            for verb_element in page_verb_elements:
                verb = verb_element.text.strip()
                if verb != 'Irregular verbs':
                    verbs.append(verb)
            print('complete!')

        print(f'Found {len(verbs)} verbs')
        return verbs


    def get_conjugation(self, verb):
        print(f'Preparing to get conjugation of the verb \'{verb}\'...')
        url = f'{CONJUGATION_BASE_URL}{verb}'
        print(f'Connecting to {url}')

        print('Downloading page', end='...')
        page = requests.get(url)
        html_page = html.fromstring(page.content)
        section = html_page.xpath('//section[@class="verb-tense-section"]')

        conj = {
            'verb': verb,
            'tenses': []
        }

        for s in section:
            tense_title = s.xpath('h3')

            if not tense_title:
                break

            tense = tense_title[0].text.lower()
            conj_span = s.xpath('div[@class="vPos"]/ul/li')

            for c in conj_span:
                pron = c[0][0].text
                irreg = c[0][1].text

                if pron and irreg:
                    conj['tenses'].append({
                        'tense': tense,
                        'pronoun': pron,
                        'conjugation': irreg
                    })

        print('complete!')
        return conj if conj['tenses'] else None