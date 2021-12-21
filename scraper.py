import json
import time
import random

from csv import DictWriter
from typing import Any, Dict, List, Union
from urllib.parse import urlencode

from selenium import webdriver
from requests_html import HTMLSession


def get_page_data(url: str) -> Union[Dict[str, Any], None]:
    print(f"Hitting {url}")

    session = HTMLSession()
    resp = session.get(url)
    if resp.status_code != 200:
        return None

    jsondata = resp.json()

    if not jsondata.get("data"):
        return None

    time.sleep(random.randint(1, 3))
    return jsondata["data"]


def id_getter(keyword: str, page=0) -> List[str]:
    parameters = {
        "facet_limit": 100,
        "location": 1000001,
        "location_facet_limit": 40,
        "query": keyword,
        "spellcheck": True,
    }
    if page:
        parameters["page"] = page
    qs = urlencode(parameters)
    url = "https://www.olx.co.id/api/relevance/v2/search?" + qs

    user_ids = []

    tempdata = get_page_data(url)
    if not tempdata:
        raise Exception("Tidak berhasil mengambil data")

    for item in tempdata:
        user_ids.append(item["user_id"])

    return user_ids


def browser_get_data(
    browser: webdriver.Firefox, url: str
) -> Union[Dict[str, Any], None]:
    browser.get(url)
    elements = browser.find_elements("tag name", "pre")
    if not elements:
        return None

    jsontext = elements[0].text
    jsondata = json.loads(jsontext)

    if not jsondata.get("data"):
        return None

    time.sleep(random.randint(1, 3))
    return jsondata["data"]


def userdata_getter(
    browser: webdriver.Firefox, userid_list: List[str]
) -> List[Dict[str, str]]:
    tempdata = []
    base_url = "view-source:https://www.olx.co.id/api/users/"

    for userid in userid_list:
        url = base_url + userid
        userdata = browser_get_data(browser, url)
        if not userdata:
            raise Exception(f"Gagal mendapatkan data user id {userid}")

        tempdata.append(
            {
                "name": userdata["name"],
                "phone": userdata["phone"],
                "verified": userdata["verification_status"],
                "about": userdata["about"],
                "url": url,
            }
        )
    return tempdata


def scrape_data():
    keyword = input("Masukkan kata kunci: ")
    startpage = int(input("Masukkan halaman mulai (minimal 0): "))
    endpage = int(
        input(
            (
                "Masukkan batas halaman yang akan discrape "
                "(0 berrati tanpa batas): "
            )
        )
    )

    print("Browser akan terbuka.")
    print("Silakan login di browser kemudian kembali ke console")
    browser = webdriver.Firefox()
    browser.get("https://www.olx.co.id")
    is_login = input("Apakah berhasil login (y/n)? ")
    if is_login != "y":
        print("Membatalkan....")
        return

    page = startpage
    userdata = []
    while True:
        if endpage > 0:
            if page > endpage:
                break

        try:
            userids = id_getter(keyword, page)
        except Exception as e:
            print(f"Gagal mengambil data untuk halaman {page}")
            print(e)
            browser.close()
            return

        try:
            usertempdata = userdata_getter(browser, userids)
        except Exception as e:
            print(f"Gagal mengambil data untuk user pada halaman {page}")
            print(e)
            browser.close()
            return

        userdata.extend(usertempdata)
        page += 1

    filename = f"result_page_{startpage}_to_{page-1}.csv"
    with open(filename, "w") as f:
        writer = DictWriter(f, userdata[0].keys())
        writer.writeheader()
        writer.writerows(userdata)
    browser.close()


if __name__ == "__main__":
    scrape_data()
