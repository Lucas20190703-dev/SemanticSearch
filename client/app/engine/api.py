
import requests


API_FETCH_DIRECTORY = "http://127.0.0.1:3000/api/directories"

API_FILE_CAPTION = "http://127.0.0.1:3000/api/caption"

def get_caption(file):
    params = {"file": file}
    res = requests.get(API_FILE_CAPTION, params=params)
    return res.json()


def search():
    pass