import json
import urllib.parse
import pyperclip

SERVER_HOST = 'localhost:8080'
SEED = 123123
LENGTH = 121
PLAYERS = [
    {
        'name': 'Baratheon',
        'address': '127.0.0.1:8080',
    },
    {
        'name': 'Greyjoy',
        'address': '127.0.0.1:8080',
    },
    {
        'name': 'Martell',
        'address': '127.0.0.1:8080',
    },
    {
        'name': 'Stark',
        'address': '127.0.0.1:8080',
    },
    {
        'name': 'Tully',
        'address': '127.0.0.1:8080',
    },
    {
        'name': 'Tyrell',
        'address': '127.0.0.1:8080',
    },
    {
        'name': 'Lannister',
        'address': '127.0.0.1:8080',
    },
    {
        'name': 'Frey',
        'address': '127.0.0.1:8080',
    },
]

PLAYERS = [
    {
        'name': 'RADKA DANE',
        'address': '127.0.0.1:8081',
    },
    {
        'name': 'TOMKA DANE',
        'address': '127.0.0.1:8080',
    }
]


def make_competition_url():
    data = {}

    if SEED:
        data['seed'] = SEED
    if LENGTH:
        data['length'] = LENGTH

    data['players'] = urllib.parse.quote(json.dumps(PLAYERS))
    qs = urllib.parse.urlencode(data)

    return urllib.parse.urlunparse(('http', SERVER_HOST, '', '', qs, ''))


def main():
    url = make_competition_url()
    pyperclip.copy(url)
    print(url)


if __name__ == '__main__':
    main()
