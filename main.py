import json
import time
import datetime
import csv

import parser


start_time = time.time()
# url = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table"
url = 'https://www.labirint.ru/genres/3079/?display=table'

def main():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    # создаем табличку
    with open(f"output/books_{cur_time}.csv", "w") as file:
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
    book_list = parser.get_book(url)
    # складываем в созданную табличку
    with open(f"output/books_{cur_time}.csv", "a") as file:
        writer = csv.writer(file)
        for i in book_list:
            writer.writerow(i.values())


    # создаем файл json и аккуратно складываем полученный список
    with open(f"output/books_{cur_time}.json", "w") as file:
        json.dump(book_list, file, indent=4, ensure_ascii=False)



    finish_time = time.time() - start_time
    print(f"time: {finish_time}")


if __name__ == '__main__':
    main()