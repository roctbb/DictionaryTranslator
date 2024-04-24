import json

import requests
import pandas as pd
from config import *


def run_translation_job(texts, target):
    task = {
        "folderId": FOLDER_ID,
        "texts": texts,
        "targetLanguageCode": target
    }

    headers = {
        "Authorization": f"Api-Key {KEY}"
    }

    answer = requests.post("https://translate.api.cloud.yandex.net/translate/v2/translate", json=task,
                           headers=headers).json()

    return list(map(lambda t: t["text"], answer["translations"]))


def translate_texts(texts, target):
    texts = texts.copy()
    result = []
    while texts:
        current_job = []
        while sum(map(len, current_job)) < 9000 and texts:
            current_job.append(texts[0])
            del texts[0]
        result += run_translation_job(current_job, target)
    return result







def translate_dict(data, target):
    keys = list(data.keys())
    return dict(zip(keys, translate_texts(keys, target)))


def export_to_excel(data, filename):
    frame = pd.DataFrame(data.items())
    frame.to_excel(filename, index=False)


def export_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


jobs = ["requests.json"]
# jobs = ["test.json"]

for job in jobs:
    data = read_json("jobs/" + job)
    data = translate_dict(data, "kk")
    export_to_json(data, "results/" + job)
    export_to_excel(data, "results/" + job + ".xlsx")
