import os
import json
import random

from app.scraper import Scraper

DATASET_FILENAME = 'conjugations.json'
DEFUALT_VERBS_PAGE = 'https://www.linguasorb.com/spanish/verbs/most-common-verbs/'
DEFUALT_VERBS_PAGE_COUNT = 10

class Dataset(object):
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.scraper = Scraper()

        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)

        full_path = self.get_dataset_path()

        print('Initialising dataset...')
        if os.path.exists(full_path):
            print('Dataset exitsts, attempting to load...')
            self.conjugations = self.load_from_json(self.get_dataset_path())
        else:
            print('Dataset does not exits, creating a new one...')
            self.conjugations = self.create_dataset(DEFUALT_VERBS_PAGE)

        print('Initialising dataset complete')


    def create_dataset(self, verb_url):
        print('Creating new verb dataset...')
        verbs = self.scraper.get_verb_list(verb_url, page_count=DEFUALT_VERBS_PAGE_COUNT)

        conj = []
        for v in verbs:
            c = self.scraper.get_conjugation(v)

            if c:
                conj.append(c)

        print(f'New verb dataset created with {len(conj)} verbs!')

        self.save_to_json(conj, self.get_dataset_path())

        return conj


    def get_dataset_path(self):
        return os.path.join(self.dataset_path, DATASET_FILENAME)


    def save_to_json(self, collection, path):
        print(f'Saving dataset to {path}', end='...')
        try:
            with open(path, 'w') as f:
                json.dump(collection, f, indent=4)
            print('complete!')
        except:
            raise 'There was a problem saving the dataset'


    def load_from_json(self, path):
        print(f'Loading dataset from {path}', end='...')
        try:
            with open(path) as f:
                collection = json.load(f)
                print('complete!')
                return(collection)
        except:
            raise 'There was a problem loading the dataset'


    def get_verb(self, verb):
        return next((f for f in self.conjugations if f['verb'] == verb), None)


    def get_random_verb(self):
        return self.conjugations[random.randint(0, len(self.conjugations) - 1)]


    def get_verb_tense(self, verb, tense):
        conj = self.get_verb(verb)
        return [t for t in conj['tenses'] if t['tense'] == tense]


    def get_verb_conjugation(self, verb, tense, pronoun):
        tenses = self.get_verb_tense(verb, tense)
        return next(c for c in tenses if c['pronoun'] == pronoun)