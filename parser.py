import time

import requests
from bs4 import BeautifulSoup


def get_book(url):
    books = []

    headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
        }


    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)


    for page in range(1, pages_count + 1):
        url = f"https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={page}"

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")

        for bi in books_items:
            book_data = bi.find_all("td")

            try:
                book_title = book_data[0].find("a").text.strip()
            except:
                book_title = "[Error]:Books name nod found"

            try:
                book_author = book_data[1].text.strip()
            except:
                book_author = "[Error]:Author not found"

            try:
                book_publishing = book_data[2].find_all("a")
                book_publishing = ":".join([bp.text for bp in book_publishing])
            except:
                book_publishing = "[Error]:Publishing house not found"

            try:
                book_new_price = int(book_data[3].find("div", class_="price").find("span").find("span").text.strip().replace(" ", ""))
            except:
                book_new_price = "[Error]:New price not found"

            try:
                book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
            except:
                book_old_price = "[Error]:Old price not found"

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
            except:
                book_sale = "[Error]:Discount not found"

            try:
                book_status = book_data[-1].text.strip()
            except:
                book_status = "[Error]:Book not availably"

            # print(book_title)
            # print(book_author)
            # print(book_publishing)
            # print(book_new_price)
            # print(book_old_price)
            # print(book_sale)
            # print(book_status)
            # print('---' * 100)

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
    print('debug', type(books), '---' * 100)
    print(books)
    return books