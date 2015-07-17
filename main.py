import sys
import time
import requests

from requests.exceptions import HTTPError, ConnectionError

url = 'http://ws.audioscrobbler.com/2.0/'
apikey = '05502f0c412debc3ef7f850447f2761d'


def get_current(name):  # TODO: move function to separator file
    methods = {'method': 'user.getrecenttracks', 'user': name, 'api_key': apikey, 'format': 'json'}

    try:
        r = requests.get(url, params=methods)
    except (HTTPError, ConnectionError) as e:
        return 'Last.fm currently not available. %s' % e

    json = r.json()

    try:  # TODO: anything with that
        json = json['recenttracks']['track']
    except KeyError:
        print(json)
        return "Error"

    for tracks in json:
        if '@attr' in tracks:
            artist = tracks['artist']['#text']
            track = tracks['name']
            return artist + ' - ' + track
        else:
            return 'Nothing'


print('Starting... Enter your Last.fm name:')
user = input()

while True:
    current = get_current(user)

    f = open('current.txt', 'w')
    f.write(str(current))
    f.close()

    sys.stdout.write("\rCurrent track: %s" % current)
    sys.stdout.flush()

    time.sleep(5)
