import sqlite3
import codecs


def main():
    con = sqlite3.connect('./DM_DATE_NEW.db')
    cur = con.cursor()
    sql = "select * from dm_card"
    cur.execute(sql)

    card_list = []

    for row in cur:  # レコードを出力する
        card_name = row[0] + " "

        race = row[1]
        if race is not "":
            race = row[1] + " "

        power = row[2]
        if power is not "":
            power = "パワー" + row[2] + " "

        civ = row[3] + "文明 "
        # civ = row[3] + " "

        cost = "コスト" + row[4] + " "
        # cost = row[4] + "マナ "

        ability = row[5].replace(",", "")

        card_list.append(card_name + race + power + civ + cost + ability)

    con.close()

    [print(text) for text in card_list]

    write_txt(card_list, "DM_CARD_NEW")


def write_txt(contents, file_name):
    try:
        if len(contents) > 0:
            fileName = file_name + ".txt"

            f = codecs.open(fileName, 'w+', 'utf-8')
            for one_card in contents:
                f.write(one_card + "\n")
            f.close()
        print(str(len(contents)) + "行を書き込み")

    except Exception as e:
        print("テキストへの書き込みに失敗")
        print(e)


if __name__ == '__main__':
    main()
