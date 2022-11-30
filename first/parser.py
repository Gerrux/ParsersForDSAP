import csv
import json

import requests
from lxml import html

offset = 1
links = []
titles = []
authors = []
book_ratings = []
prices = []
variants = []
parser_is_run = True

while parser_is_run:

    url = f"https://www.bookvoed.ru/books?genre=2&offset={offset}&_part=books"
    response = requests.request("GET", url)
    tree = html.fromstring(response.text)
    x = 0
    for i in range(1, 60):
        start_xpath = "/html/body/div/div[1]/div/"
        # try:
        #     start_xpath = "/html/body/div/div[1]/div/"
        #     var = tree.xpath(f"{start_xpath}div[{i}]/div[1]/a")[0].attrib["href"]
        # except IndexError:
        #     start_xpath = "/html/body/div/div/div/"
        if offset == 960:
            x += 1
            if x == 40:
                parser_is_run = False
                break
        links.append(
            tree.xpath(f"{start_xpath}div[{i}]/div[1]/a")[0].attrib["href"]
        )
        titles.append(
            tree.xpath(f"{start_xpath}div[{i}]/div[2]/div[1]/a")[0].text.replace('\n', '')
        )
        authors.append(
            tree.xpath(f"{start_xpath}div[{i}]/div[2]/div[2]")[0].text.replace('\n', '')
        )
        try:
            book_ratings.append(
                tree.xpath(f"{start_xpath}div[{i}]/div[1]/div/span")[0].text + " "
            )
        except IndexError:
            book_ratings.append("нет рейтинга")
        additional_info = json.loads(
            tree.xpath(f"{start_xpath}div[{i}]")[0].attrib["data-retargeting_book"]
        )
        prices.append(additional_info["price"])
        try:
            info = json.loads(
                tree.xpath(f"{start_xpath}div[{i}]/div[4]/div[1]/a")[0].attrib["data-gtmoffer"]
            )["variant"]
            if info is None:
                variants.append("не указано")
            else:
                variants.append(info)
        except KeyError:
            variants.append("не указано")
        except json.decoder.JSONDecodeError:
            variants.append("не указано")
    if offset == 1:
        offset = 60

    elif x == 40:
        offset += 40
    else:
        offset += 60
    print(offset)

for i in range(len(links)):
    data = [links[i], titles[i], authors[i], book_ratings[i], prices[i], variants[i]]
    with open("harvest_data.csv", mode="a", encoding="windows-1251", newline="") as f:
        writer = csv.writer(f, delimiter=";", quotechar=" ")
        writer.writerow(data)
