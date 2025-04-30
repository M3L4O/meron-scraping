import json
import math
import random
import select
from io import StringIO
from os import makedirs, path
from time import sleep
from types import NoneType

from bs4 import BeautifulSoup
from numpy import info
from selenium.webdriver.chrome.options import Options
from seleniumbase import Driver
from tqdm import tqdm

base_url = "https://pcpartpicker.com"

components = {
    # "cpu": "/product/cpu/",
    # "gpu": "/product/video-card/",
    "motherboard": "/product/motherboard/",
    # "ram": "/product/memory/#Z=512001,1024001,2048001,4096001,8192001,16384001,24576001,32768001,49152001,65536001,131072001",
    # "storage": "/product/internal-hard-drive/",
    # "psu": "/product/power-supply/",
}


def get_max_page(soup: BeautifulSoup):
    return max(
        int(li.text) for li in soup.select(".pagination li") if li.text.isdigit()
    )


def get_shallow_specs(name: str, soup: BeautifulSoup):
    components_specs = soup.select("tr.tr__product")
    specs = []
    for component_specs in components_specs:
        entity = {
            spec.find("h6").text: spec.find("h6").next_sibling
            for spec in component_specs.select(".td__spec")
        }
        entity["model"] = component_specs.select_one(".td__name p").text
        entity["uri"] = component_specs.find("a")["href"]
        specs.append(entity)

    return specs


def scraping_component(driver: Driver, name: str, detail: bool = False):
    if detail:
        with open(f"data/{name}.json", "r") as file:
            components = json.load(file)

        specs = []
        for component in tqdm(components, desc=name):
            driver.sleep(random.uniform(3, 10))
            driver.get(base_url + component["uri"])
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            spec = {
                info.find("h3").text.strip(): (
                    info.find("p").text.strip()
                    if info.find("p")
                    else (
                        [li.text.strip() for li in info.find("ul").find_all("li")]
                        if info.find("ul")
                        else "0"
                    )
                )
                for info in soup.select(".group--spec")
            }
            specs.append(spec)
            with open(f"data/{name}_detail.json", "w", encoding="utf-8") as file:
                json.dump(specs, file, indent=4, ensure_ascii=False)

    else:
        page_str = "#page={}" if name != "ram" else "&page="
        url = base_url + components[name] + page_str
        driver.get(url.format(1))
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        pages = get_max_page(soup)
        specs = []
        for page in range(1, pages + 1):
            driver.sleep(random.uniform(3, 7))
            driver.get(url.format(page))
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            specs.extend(get_shallow_specs(name, soup))

            with open(f"data/{name}.json", "w", encoding="utf-8") as file:
                json.dump(specs, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    makedirs("data/", exist_ok=True)
    driver = Driver(uc=True )
    driver.uc_open(base_url)
    driver.uc_gui_click_captcha()
    driver.set_window_position(-10000, 0)  # Move a janela pra fora da tela
    driver.set_window_size(800, 600)       # Tamanho pequeno só pra constar
    for component in components.keys():
        specs = scraping_component(driver, component, True)

    driver.quit()
