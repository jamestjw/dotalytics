import requests
import json

class MatchGenerator(object):
    def __init__(self,list_of_match_id,**kwargs):
        self.list_of_match_id = list_of_match_id
        self.index = 0
        # self.__dict__ = kwargs

    def __len__(self): return len(self.match_ids)

    def api_request(self,match_id):
        api_path = 'https://api.opendota.com/api/matches/{}'.format(match_ids)
        results = requests.get(api_path)

    def __iter__(self):
        for index, match_id in enumerate(self.list_of_match_id):
            results = self.api_request(match_id)
            self.index = index
            yield results





