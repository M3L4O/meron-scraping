import json
import math
import random
from io import StringIO
from time import sleep

import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
from tqdm import tqdm


base_url = "https://www.ldlc.com"
components_path = "/en/computing/components/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": base_url
}

page_components = [
    #"processor/c4300/",
    "graphics-card/c4684/",
    #"motherboard/c4293/",
    #"pc-ram/c4703/",
    #"internal-hard-drive/c4697/",
    #"ssd/c4698/",
    #"pc-power-supply/c4289/",
]

components = [
    #"cpu",
    "gpu",
    #"motherboard",
    #"ram",
    #"hdd",
    #"ssd",
    #"psu",
]


def get_components_links(soup, selector: str):
    return [base_url + a["href"] for a in soup.select(selector)]


for page_component, component in zip(page_components, components):
    component_url = base_url + components_path + page_component
    html = rq.get(component_url, headers=headers).content
    soup = BeautifulSoup(html, "html.parser")

    num_pages = max(
        [int(a.text) for a in soup.select("ul.pagination li a") if a.text.isdigit()]
    )

    component_links = get_components_links(soup, ".title-3 a")

    for page in range(1, num_pages):
        page_url = component_url + f"page{page}/"
        html = rq.get(page_url, headers=headers).content
        soup = BeautifulSoup(html, "html.parser")
        component_links.extend(get_components_links(soup, ".title-3 a"))

    components_info = []

    for link in tqdm(component_links, desc=component):
        sleep(random.uniform(2, 5))
        html = rq.get(link, headers=headers).content
        soup = BeautifulSoup(html, "html.parser")

        tables = soup.select("table")
        try:
            if tables:
                entity = {}
                features = tables[0]
                html_str = str(features)
                table = pd.read_html(StringIO(html_str))
                keys = [key for key in table[0][1]]
                values = [value for value in table[0][2]]

                for key, value in zip(keys, values):
                    if type(value) is float and math.isnan(value):
                        value = ""
                    if key in entity.keys():
                        if type(entity[key]) is list:
                            entity[key].append(value)
                        else:
                            entity[key] = [entity[key], value]
                    else:
                        entity[key] = value
                components_info.append(entity)

        except:
            print("Nenhuma tabela encontrada na página.")
            continue

    with open(f"data_ldlc/{component}.json", "w") as f:
        json.dump(components_info, f, indent=4)
    sleep(50)