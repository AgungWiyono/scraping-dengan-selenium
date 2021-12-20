import os
import sys
import json
import time
import random
from urllib.parse import urlencode

from requests_html import HTMLSession


def get_data(url):
    print(f"Hitting {url}")

    session = HTMLSession()
    resp = session.get(url)
    if resp.status_code != 200:
        return None

    jsondata = resp.json()["data"]

    time.sleep(random.randint(1, 4))
    return jsondata


def main_process(keyword):
    if not os.path.isdir("user_ids"):
        os.mkdir("user_ids")

    parameters = {
        "facet_limit": 100,
        "location": 1000001,
        "location_facet_limit": 40,
        "query": keyword,
        "spellcheck": True,
    }
    qs = urlencode(parameters)
    url = "https://www.olx.co.id/api/relevance/v2/search?" + qs
    user_ids = []
    iteration = 0
    while True:
        if iteration % 5 == 0 and iteration != 0:
            filename = f"user_ids/users_{iteration//5}.json"
            print(user_ids)
            with open(filename, "w") as f:
                json.dump({"data": user_ids}, f)
            user_ids = []

        if iteration < 1:
            tempdata = get_data(url)
        else:
            tempdata = get_data(url + f"&page={iteration}")

        for item in tempdata:
            user_ids.append(item["user_id"])

        if tempdata is None:
            filename = f"user_ids/users_{iteration//5+1}.json"
            with open(filename, "w") as f:
                json.dump({"data": user_ids}, f)
            user_ids = []
        iteration += 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Butuh kata kunci")
        sys.exit()

    main_process(sys.argv[1])
