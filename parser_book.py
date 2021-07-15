import time

import requests
from bs4 import BeautifulSoup
import colorama


colorama.init()
GREEN = colorama.Fore.GREEN
BLUE = colorama.Fore.BLUE
RED = colorama.Fore.RED
RESET = colorama.Fore.RESET


def get_book(url):
    books = []

    headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",  # NOQA E501
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"  # NOQA E501
        }

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)  # NOQA E501

    for page in range(1, pages_count + 1):
        url = f"https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={page}"  # NOQA E501

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")  # NOQA E501

        for bi in books_items:
            book_data = bi.find_all("td")

            try:
                book_title = book_data[0].find("a").text.strip()
            except Exception as exc:
                print(f'{RED} {exc} {RESET}')
                book_title = f'{RED}[Error]:Books name nod found{RESET}'

            try:
                book_author = book_data[1].text.strip()
            except Exception as exc:
                print(f'{RED} {exc} {RESET}')
                book_author = f'{RED}[Error]:Author not found{RESET}'

            try:
                book_publishing = book_data[2].find_all("a")
                book_publishing = ":".join([bp.text for bp in book_publishing])
            except Exception as exc:
                print(f'{RED} {exc} {RESET}')
                book_publishing = f'{RED}[Error]:Publishing house not found{RESET}'  # NOQA E501

            try:
                book_new_price = int(book_data[3].find("div", class_="price").find("span").find("span").text.strip().replace(" ", ""))  # NOQA E501
            except Exception as exc:
                print(f'{RED} {exc} {RESET}')
                book_new_price = f'{RED}[Error]:New price not found{RESET}'

            try:
                book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))  # NOQA E501
            except Exception as exc:
                print(f'{RED} {exc} {RESET}')
                book_old_price = f'{RED}[Error]:Old price not found{RESET}'

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)  # NOQA E501
            except Exception as exc:
                print(f'{RED} {exc} {RESET}')
                book_sale = f'{RED}[Error]:Discount not found{RESET}'

            try:
                book_status = book_data[-1].text.strip()
            except Exception as exc:
                print(f'{RED} {exc} {RESET}')
                book_status = f'{RED}[Error]:Book not availably{RESET}'

            print(f'{GREEN}{book_title}')
            print(f'{book_author}')
            print(f'{book_publishing}{RESET}')
            print(f'{BLUE}{book_new_price}')
            print(f'{BLUE}{book_old_price}')
            print(f'{BLUE}{book_sale}')
            print(f'{GREEN}{book_status}')

            books.append(
                {
                    "book_title": book_title,
                    "book_author": book_author,
                    "book_publishing": book_publishing,
                    "book_new_price": book_new_price,
                    "book_old_price": book_old_price,
                    "book_sale": book_sale,
                    "book_status": book_status
                }
            )
        print(f'Continue {page} of {pages_count}')
        time.sleep(0.5)
    return books
