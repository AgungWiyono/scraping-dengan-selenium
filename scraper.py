import sys
import os
import json
import time
import random
import logging

from typing import Any, Dict, List, Union
from urllib.parse import urlencode
from logging.handlers import RotatingFileHandler

import tablib

from selenium import webdriver
from requests_html import HTMLSession

if not os.path.exists("logs"):
    os.mkdir("logs")
logger = logging.getLogger(__name__)
file_handler = RotatingFileHandler(
    "./logs/scraper.log",
    maxBytes=1024 * 5,
    backupCount=10,
)
logging.basicConfig(level=logging.INFO)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(message)s")
)
logger.addHandler(file_handler)


def get_page_data(url: str) -> Union[Dict[str, Any], None]:
    print(f"Hitting {url}")
    logger.info(f"Hitting {url}")

    session = HTMLSession()
    resp = session.get(url)
    if resp.status_code == 404:
        logger.info("Proses Scraping telah sampai pada halaman akhir.")
        return None
    if resp.status_code != 200:
        logger.info(json.dumps(resp.json()))
        return None

    jsondata = resp.json()

    if not jsondata.get("data"):
        logger.info("Elemen Data tidak ditemukan")
        return None

    time.sleep(random.randint(1, 3))
    return jsondata["data"]


def id_getter(keyword: str, page=0, location=None) -> List[str]:
    parameters = {
        "facet_limit": 100,
        "location": location if location else 1000001,
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
        logger.info("Elemen pre tidak ditemukan.")
        return None

    jsontext = elements[0].text
    jsondata = json.loads(jsontext)

    if not jsondata.get("data"):
        logger.info("Elemen data pada data user tidak ditemukan.")
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
                "url": url[12:],
            }
        )
    return tempdata


def find_location(keyword) -> str:
    parameters = {
        "input": keyword,
        "limit": 50,
    }
    url = "https://www.olx.co.id/api/locations/autocomplete?"
    querystring = urlencode(parameters)
    browser = HTMLSession()
    resp = browser.get(f"{url}{querystring}")
    data = resp.json()["data"]["suggestions"]

    suggested_location = []
    valid_location = []
    for item in data:
        choice = {
            "nama": item["name"],
            "jenis": item["type"],
            "id": item["id"],
        }
        valid_location.append(choice["id"])
        suggested_location.append(choice)
    print(f"Pilihan lokasi yang tersedia berdasarkan keyword {keyword}")
    for item in suggested_location:
        print(
            f"ID: {item['id']}, Nama: {item['nama']}, Jenis: {item['jenis']}"
        )
    location_id = input("Masukkan id dari lokasi yang diinginkan: ")
    print(valid_location)
    if int(location_id) not in valid_location:
        print("Lokasi yang dipilih tidak valid.")
        print("Menghentikan program...")
        sys.exit()
    return location_id


def scrape_data():
    keyword = input("Masukkan kata kunci: ")
    startpage = int(input("Masukkan halaman mulai (minimal 0): ") or 0)
    endpage = int(
        input(
            (
                "Masukkan batas halaman yang akan discrape "
                "(0 berrati tanpa batas): "
            )
        )
        or 0
    )

    location_keyword = input(
        "Masukkan lokasi yang diinginkan (default kosong): "
    )
    location_id = None
    if location_keyword:
        location_id = find_location(location_keyword)

    print("Browser akan terbuka.")
    print("Silakan login di browser kemudian kembali ke console")
    browser = webdriver.Firefox()
    browser.get("https://www.olx.co.id")
    is_login = input("Apakah berhasil login (y/n)? ")
    if is_login != "y":
        print("Membatalkan....")
        return

    page = startpage
    headers = ["name", "phone", "verified", "about", "url"]
    userdata = tablib.Dataset()
    userdata.headers = headers
    userphone_exists = []

    state = True
    while state:
        if endpage > 0:
            if page > endpage:
                logger.info("Ending Scraping Process")
                break

        try:
            userids = id_getter(keyword, page, location_id)
        except Exception as e:
            print(f"Gagal mengambil data untuk halaman {page}")
            print(e)
            browser.close()
            state = False

        if not state:
            break

        try:
            usertempdata = userdata_getter(browser, userids)
        except KeyboardInterrupt:
            print("Proses dihentikan")
        except Exception as e:
            print(f"Gagal mengambil data untuk user pada halaman {page}")
            print(e)
            browser.close()
            state = False

        for row in usertempdata:
            if row["phone"] not in userphone_exists:
                userphone_exists.append(row["phone"])
                userdata.append(row.values())
        page += 1

    filename = f"result_page_{startpage}_to_{page-1}.xlsx"
    with open(filename, "wb") as f:
        f.write(userdata.export("xlsx"))
    browser.close()


if __name__ == "__main__":
    scrape_data()
