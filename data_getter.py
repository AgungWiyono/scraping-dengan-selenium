import sys
import time
import random
import json
from datetime import datetime

from selenium import webdriver


def get_data(browser, url):
    browser.get(url)
    jsontext = browser.find_element("tag name", "pre").text
    time.sleep(random.randint(1, 4))
    return json.loads(jsontext)["data"]


def main_process(browser, user_ids):
    user_data = []
    base_url = "view-source:https://www.olx.co.id/api/users/"
    for idx, user_id in enumerate(user_ids):
        if idx == 3:
            break
        url = base_url + user_id
        data = get_data(browser, url)
        user_data.append(
            {
                "name": data["name"],
                "phone": data["phone"],
                "verified": data["verification_status"],
                "about": data["about"],
                "url": url,
            }
        )
    browser.close()

    filename = f"result_{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}.json"
    with open(filename, "w") as f:
        json.dump(user_data, f)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Butuh file berisi user id")
        sys.exit()

    browser = webdriver.Firefox()
    browser.get("https://www.olx.co.id")
    yes = input("Apakah berhasil login (y/n)? ")
    if yes != "y":
        print("Membatalkan....")
        sys.exit()

    with open(sys.argv[1], "r") as f:
        user_ids = json.load(f)["data"]

    main_process(browser, user_ids)
