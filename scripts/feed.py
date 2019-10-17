from google.cloud import storage
import requests
import json
import os
# import utils


# def parametized(dec):
#     def layer(*args, **kwargs):
#         def repl(f):
#             return dec(f, *args, **kwargs)
#         return repl
#     return layer


# @parametized
# def add_n(f,n):
#     def do_function(*args,**kwargs):
#         return f(*args,**kwargs) + n
#     return do_function

# @add_n(10)
# def do_something(x):
#     return x

# print function(3)


def run():
    # https: // docs.opendota.com/  # tag/feed
    api_path = 'https://api.opendota.com/api/feed'

    file_path = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(file_path, 'feed.txt')
    api_key = ''
    bucket = 'kaodim-ml'
    params = {'seq_number': 5072768284, 'game_mode': 2, 'api_key':api_key}
    res = requests.get(api_path,params=params)
    data = json.loads(res.text)
    client = storage.Client()
    

    


if __name__ == "__main__":
    run()
