import requests

class Sonarr(object):
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    def get_series(self):
        response = requests.get("{}/api/series?apikey={}".format(self.url, self.api_key))
        return response.json()

    def get_episodes(self, series_id):
        response = requests.get("{}/api/episode?seriesId={}&apikey={}".format(self.url, series_id, self.api_key))
        return response.json()

    def get_release(self, episode_id):
        response = requests.get("{}/api/release?episodeId={}&apikey={}".format(self.url, episode_id, self.api_key))
        return response.json()

    def post_release(self, guid, indexer_id):
        response = requests.post("{}/api/release?guid={}&indexerId={}&apikey={}".format(self.url, guid, indexer_id, self.api_key))
        return response.json()

    def get_profiles(self):
        response = requests.get("{}/api/profile?apikey={}".format(self.url, self.api_key))
        return response.json()