import csv
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

wd = webdriver.Chrome("chromedriver", options=chrome_options)
wd.get("https://www.news29.ru/novosti/")
wd.implicitly_wait(10)
wd.fullscreen_window()


def scrap_block_news(block):
    data = []
    link = (
        "https://www.news29.ru"
        + block.find("div", {"class": "title"}).find("a")["href"]
    )  # Ссылка

    title = block.find("div", {"class": "title"}).text  # заголовок
    # дата публикации
    publ_date = block.find("div", {"class": "date"}).text
    view_count = (
        block.find("div", {"class": "viewscount"})
        .text.replace("\n", "")
        .replace("\t", "")
        .replace(publ_date, "")
        .lstrip(" ")
        .split(" ")[0]
    )
    publ_date = publ_date.replace(
        "вчера", (datetime.today() - timedelta(days=1)).strftime("%d.%m.%y")
    ).replace("сегодня", datetime.today().strftime("%d.%m.%y"))
    # количество просмотров
    tags = block.find("div", {"class": "issue"}).text
    data.append(title)
    data.append(link)
    data.append(publ_date)
    data.append(view_count)
    data.append(tags)
    return data


def parse(start):
    soup = BeautifulSoup(wd.page_source, features="html.parser")
    location_blocks = soup.findAll("div", {"class": "newItemContainer"})
    for i in range(start, len(location_blocks)):
        block = location_blocks[i]
        try:
            data = scrap_block_news(block)
        except:
            time.sleep(2)

            data = scrap_block_news(block)

        with open(
            "harvest_data.csv", mode="a", encoding="windows-1251", newline=""
        ) as f:
            writer = csv.writer(f, delimiter=";", quotechar=" ")
            writer.writerow(data)
    return len(location_blocks)


time.sleep(0.5)
x = 0
while x < 2000:
    x = parse(x)
    print(x)
    wait = WebDriverWait(wd, 30)
    wait.until(ec.element_to_be_clickable((By.ID, "moreNews")))
    wd.execute_script('document.querySelector("#moreNews").click()')


wd.quit()
