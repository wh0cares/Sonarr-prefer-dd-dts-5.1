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
    profile_id = series['profileId']
    quality_rank = []
    for profile in sonarr.get_profiles():
        if str(profile_id) in str(profile['id']):
            for item in profile['items']:
                if item['allowed']:
                   quality_rank.append(item['quality']['id'])
    for episode in sonarr.get_episodes(series_id):
        if episode['hasFile']:
            if episode['episodeFile']['mediaInfo']['audioCodec'] == "AAC":
                episode_id = episode['id']
                quality = episode['episodeFile']['quality']['quality']['id']
                try:
                    episode_rank = quality_rank.index(quality)
                except ValueError:
                    episode_rank = 0
                name = episode['episodeFile']['quality']['quality']['name']
                tqdm.write('Searching ' + series['title'] + " " + str(episode['seasonNumber']) + 'x' + str(episode['episodeNumber'])  + ' releases')
                for releases in sonarr.get_release(episode_id):
                    if any(i in releases['title'].upper() for i in ['DD', '5.1', 'DTS']):
                        guid = releases['guid']
                        indexer_id = releases['indexerId']
                        release_quality = releases['quality']['quality']['id']
                        rejected = False
                        try:
                            release_rank = quality_rank.index(release_quality)
                        except ValueError:
                            release_rank = 0
                        if release_rank >= episode_rank:
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
                                elif "requested" in rejections:
                                    rejected = True
                                    break
                                else:
                                    rejected = False
                            if(rejected):
                                tqdm.write('Rejected ' + releases['title'])
                                continue
                            else:
                                tqdm.write('Grabbing ' + releases['title'])
                                sonarr.post_release(guid, indexer_id)
                                break
                        else:
                            break

print "done"