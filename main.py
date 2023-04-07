import json
import time
import requests
from bs4 import BeautifulSoup
import re
import datetime
import csv

start_time = time.time()


def get_data():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y %H_%M")

    with open(f"Товары по Акции_{cur_time}.csv", "w", encoding="cp1251", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            (
                "Продукт",
                "Скидка",
                "Цена",
                "Ссылка"
            )
        )

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }

    url = "https://ultra.md/ru/promo/products"

    response = requests.get(url=url, headers=headers)

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    soup = BeautifulSoup(response.text, "lxml")

    # with open("index.html", encoding="utf-8") as file:
    #     src = file.read()
    # soup = BeautifulSoup(src, "lxml")

    pages_count = int(
        soup.find('nav', attrs={"aria-label": "Pagination Navigation"}).find_all('div')[-1].find_all('span')[-1].text)

    # products_data = []
    for page in range(1, pages_count + 1):
        # for page in range(1, 2):
        url = f"https://ultra.md/ru/promo/products?page={page}"

        response = requests.get(url=url, headers=headers)

        # with open(f"index{page}.html", "w", encoding="utf-8") as file:
        #     file.write(response.text)
        soup = BeautifulSoup(response.text, "lxml")

        # with open(f"index.html", encoding="utf-8") as file:
        #     src = file.read()
        # soup = BeautifulSoup(src, "lxml")

        products_items = soup.find('div', class_="products-list").find_all('div', class_="product-block-card-container")

        for pi in products_items:
            product_data = pi.find('div').find_next_sibling("div")

            # ---------------Product title
            try:
                product_title = pi.find("div").find_all('a')[-1].text.strip().replace("ö", "o").replace("Wi‑Fi",
                                                                                                         "WiFi")
            except:
                product_title = "No data available!"            

            # ---------------Product price
            try:
                product_price = int(product_data.find('span', class_="text-xl").text.strip().replace(" ", "").replace("\nлей", " "))
            except:
                product_price = "No data!"

            # ---------------Product discount
            product_sold_out = pi.parent.find("span", string="Распродано")  
            if product_sold_out:
                product_discount = product_sold_out.text
            else:
                try:
                    product_old_price = int(product_data.find("span", class_="line-through").text.strip().replace(" ", "").replace("\nлей", " "))
                    product_discount = f"{round(((product_old_price-product_price)/product_old_price)*100)} %"
                except:
                    product_discount = "No discount!"

            # ---------------Product link
            try:
                product_link = pi.find("div").find_all('a')[-1].get('href')
            except:
                product_link = "No data available!"

            # products_data.append(
            #     {
            #         "Title": product_title,
            #         "Discount": product_discount,
            #         "Price": product_price,
            #         "URL-LINK": product_link
            #     }
            # )
            # print(len(product_data))
            # print(product_price)
            # print(product_old_price)
            # print(product_discount)
            # print("*"*10)
           
            with open(f"Товары по Акции_{cur_time}.csv", "a", encoding="cp1251", newline="") as file:
                writer = csv.writer(file, delimiter=";")

                writer.writerow(
                    (
                        product_title,
                        product_discount,
                        product_price,
                        product_link
                    )
                )

        print(f"Обработана {page} / {pages_count}")
        time.sleep(2)

    # with open(f"Товары по Акции_{cur_time}.json", "w", encoding="utf-8") as file:
    #     json.dump(products_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"Затраченно на работу скрипта времени: {finish_time}")


if __name__ == "__main__":
    main()
