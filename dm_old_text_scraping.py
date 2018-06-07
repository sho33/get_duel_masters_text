import urllib.request
from bs4 import BeautifulSoup
from time import sleep
from model import DM_CARD
import re
import sqlite3
import codecs

http_list = [
    'http://dm.takaratomy.co.jp/archive/product/dmr17/',
    'http://dm.takaratomy.co.jp/archive/product/dmr18/',
    'http://dm.takaratomy.co.jp/archive/product/dmr19/',
    'http://dm.takaratomy.co.jp/archive/product/dmr20/',
    'http://dm.takaratomy.co.jp/archive/product/dmr21/',
    'http://dm.takaratomy.co.jp/archive/product/dmr22/',
    'http://dm.takaratomy.co.jp/archive/product/dmr23/',
]

root = "http://dm.takaratomy.co.jp"


def main():
    card_detail_list = get_card_detail_list(http_list)

    all_card_list = []

    for detail_url in card_detail_list:
        all_card_list.append(get_one_card_detail(detail_url))

    write_contents = []

    for one_card_both in all_card_list:
        for card in one_card_both:
            write_contents.append(card)

    # write_txt(write_contents, "dmr23")
    write_sqlite(write_contents, "dm_card")

    """
    one_card_both = get_one_card_detail("http://dm.takaratomy.co.jp/archive/card/detail/?id=dmr23-ffl01")
    # http://dm.takaratomy.co.jp/archive/card/detail/?id=dmr23-ffl01
    # http://dm.takaratomy.co.jp/archive/card/detail/?id=dmr23-l02
    # http://dm.takaratomy.co.jp/archive/card/detail/?id=dmr23-014

    write_contents = [card for card in one_card_both]

    write_txt(write_contents, "DM_CARD_TEST")
    # write_sqlite(write_contents, "dm_card_test")
    """


def get_card_detail_list(url_list):
    detail_list = []
    for url in url_list:
        print(url)
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser").find("div", class_="cardbox")
        # print(soup.prettify())
        results = soup.find_all("div", class_=re.compile("^card-thumbnail"))
        for result in results:
            data_href = root + result.find("a", class_="ajax").get("href")
            detail_list.append(data_href)
        sleep(1)
    return detail_list


def get_one_card_detail(url):
    dm_card_both = []
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find_all("table", class_=re.compile("^cardPopupDetail"))

    for one_table in table:
        dm_card = DM_CARD()
        card_name = one_table.find("img").get("alt")
        dm_card.card_name = card_name

        race = one_table.find("td", class_="racetxt").get_text()
        dm_card.race = race

        power = one_table.find("td", class_="powertxt").get_text()
        dm_card.power = power

        civ = one_table.find("td", class_="civtxt").get_text()
        dm_card.civ = civ

        cost = one_table.find("td", class_="costtxt").get_text().replace(" マナ", "")
        dm_card.cost = cost

        abilitytxt = one_table.find_all("td", class_="abilitytxt")
        ability_list = []
        for txt in abilitytxt:
            ability_list.append(format_text(txt.get_text()))
        dm_card.ability = ",".join(ability_list)

        print(dm_card.card_name)
        dm_card_both.append(dm_card)

    sleep(1)
    return dm_card_both


def write_txt(contents, file_name):
    try:
        if len(contents) > 0:
            fileName = file_name + ".txt"

            f = codecs.open(fileName, 'w+', 'utf-8')
            for one_card in contents:
                card_name = one_card.card_name + " "
                race = one_card.race
                if race is not "":
                    race = one_card.race + " "
                power = one_card.power
                if power is not "":
                    power = "パワー" + power + " "
                civ = one_card.civ + "文明 "
                cost = "コスト" + one_card.cost + " "
                ability = one_card.ability.replace(",", "")
                row = card_name + race + power + civ + cost + ability
                f.write(format_text(row) + "\n")
            f.close()
        print(str(len(contents)) + "行を書き込み")

    except Exception as e:
        print("テキストへの書き込みに失敗")
        print(e)


def write_sqlite(contents, file_name):
    con = sqlite3.connect('./DM_DATE_Rev.db')  # データベースに接続する
    cur = con.cursor()
    sql = "create table " + file_name + "(card_name text, race text, power text, civ text, cost text ,ability text); "
    cur.execute(sql)

    try:
        dm_card_tuple_list = []
        if len(contents) > 0:
            for one_card in contents:
                dm_card_tuple_list.append((one_card.card_name, one_card.race, one_card.power, one_card.civ,
                                           one_card.cost, one_card.ability))
        # レコードを一括挿入
        cur.executemany("insert into " + file_name + ' values(?, ?, ?, ?, ?, ?)', dm_card_tuple_list)
        print(str(len(contents)) + "行を書き込み")

    except Exception as e:
        print("テキストへの書き込みに失敗")
        print(e)

    con.commit()  # コミットする
    con.close()  # 接続を閉じる


def format_text(text):
    text = re.sub(r'\n', "", text)
    text = text.strip()
    return text


if __name__ == "__main__":
    main()
