import json
from api import Sonarr

with open('config.json') as file:
    data = json.load(file)
    url = data['url']
    api_key = data['api_key']

sonarr = Sonarr(url, api_key)

for series in sonarr.get_series():
    series_id = series['id']
    for episode in sonarr.get_episodes(series_id):
        if episode['hasFile']:
            if episode['episodeFile']['mediaInfo']['audioCodec'] == "AAC":
                episode_id = episode['id']
                for releases in sonarr.get_release(episode_id):
                    if any(i in releases['title'].upper() for i in ['DD', '5.1', 'DTS']):
                        guid = releases['guid']
                        indexer_id = releases['indexerId']
                        for rejections in releases['rejections']:
                            if "blacklisted" in rejections:
                                blacklisted = True
                                break
                            else:
                                blacklisted = False
                        if(blacklisted):
                            continue
                        else:
                            print releases['title'].encode('utf-8')
                            sonarr.post_release(guid, indexer_id)
                            break

print "done"