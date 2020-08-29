import json

from app.dataset import Dataset


def pretty_print_json(obj):
    print(json.dumps(obj, indent=4, sort_keys=True))


if __name__ == "__main__":
    dataset = Dataset('data')

    print('Testing dataset...')

    print('Getting verb querer...')
    pretty_print_json(dataset.get_verb('querer'))

    print('Getting verb haber imperfect tenses...')
    pretty_print_json(dataset.get_verb_tense(verb='haber', tense='imperfect'))

    print('Getting verb pedir preterite ellos conjugation...')
    pretty_print_json(dataset.get_verb_conjugation(verb='pedir', tense='preterite', pronoun='ellos'))

    print('Getting 3 random verbs...')
    for _ in range(3):
        pretty_print_json(dataset.get_random_verb())

