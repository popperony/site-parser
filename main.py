import json
import time
import datetime
import csv

import parser_book


start_time = time.time()
# url = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table"  # NOQA E501
url = 'https://www.labirint.ru/genres/3079/?display=table'


def main():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    # создаем табличку
    with open(f"output/books_{cur_time}.csv", "w", encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название книги",
                "Автор",
                "Издательство",
                "Цена со скидкой",
                "Цена без скидки",
                "Процент скидки",
                "Наличие на складе"
            )
        )
    # запускаем парсер
    book_list = parser_book.get_book(url)
    # складываем в созданную табличку
    with open(f"output/books_{cur_time}.csv", "a", encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in book_list:
            writer.writerow(i.values())

    # создаем файл json и аккуратно складываем полученный список
    with open(f"output/books_{cur_time}.json", "w", encoding='utf-8') as file:
        json.dump(book_list, file, indent=4, ensure_ascii=False)

    finish_time = time.time() - start_time
    print(f"time: {finish_time}")


if __name__ == '__main__':
    main()
