# -*- coding: utf-8 -*-
import json
from tqdm import tqdm
from api import Sonarr

with open('config.json') as file:
    data = json.load(file)
    url = data['url']
    api_key = data['api_key']

print 'Searching series...'
sonarr = Sonarr(url, api_key)
for series in tqdm(sonarr.get_series()):
    tqdm.write('Searching ' + series['title'] + ' episodes')
    series_id = series['id']
    for episode in sonarr.get_episodes(series_id):
        if episode['hasFile']:
            if episode['episodeFile']['mediaInfo']['audioCodec'] == "AAC":
                episode_id = episode['id']
                tqdm.write('Searching ' + series['title'] + " " + str(episode['seasonNumber']) + 'x' + str(episode['episodeNumber'])  + ' releases')
                for releases in sonarr.get_release(episode_id):
                    if any(i in releases['title'].upper() for i in ['DD', '5.1', 'DTS']):
                        guid = releases['guid']
                        indexer_id = releases['indexerId']
                        rejected = False
                        for rejections in releases['rejections']:
                            if "blacklisted" in rejections:
                                rejected = True
                                break
                            elif "queue" in rejections:
                                rejected = True
                                break
                            elif "is not wanted in profile" in rejections:
                                rejected = True
                                break
                            else:
                                rejected = False
                        if(rejected):
                            continue
                        else:
                            tqdm.write('Grabbing ' + releases['title'])
                            sonarr.post_release(guid, indexer_id)
                            break

print "done"