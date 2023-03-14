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
            {
                "Продукт",
                "Скидка",
                "Цена",
                "Ссылка"
            }
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
    # soup = BeautifulSoup(src,"lxml")     

    pages_count = int(
        soup.find('nav', attrs={"aria-label": "Pagination Navigation"}).find_all('div')[-1].find_all('span')[-1].text)

    products_data = []
    for page in range(1, pages_count + 1):
        # for page in range(5, 6):
        url = f"https://ultra.md/ru/promo/products?page={page}"

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        products_items = soup.find('div', class_="products-list").find_all('div', class_="product-block-card-container")

        for pi in products_items:

            product_data = pi.find_all('div')
            try:
                product_data_sale = pi.parent.find("span", {"class": "text-lg text-red-500 font-bold"}).text
            except:
                product_data_sale = None

            if product_data_sale is None:
                try:
                    product_title = product_data[0].find_all('a')[-1].text.strip().replace("ö", "o").replace("Wi‑Fi", "WiFi")
                except:
                    product_title = "No data available!"

                try:
                    if len(product_data) == 23:
                        product_discount = product_data[14].find('div', class_="relative w-full").find_all('span')[
                            1].text.replace("лей", "No discount!")
                    elif len(product_data) == 25:
                        product_discount = product_data[16].find('div', class_="relative w-full").find_all('span')[
                            1].text.replace("лей", "No discount!")
                    else:
                        product_discount = product_data[12].find('div', class_="relative w-full").find_all('span')[
                            1].text.replace("лей", "No discount!")
                except:
                    product_discount = "No discount!"

                try:
                    if len(product_data) == 23:
                        product_price = product_data[14].find('div', class_="relative mt-1 w-full").find('span',
                                                                                                         class_="text-xl").text.strip().replace(
                            " ", "").replace("\n", " ")
                        # product_price_re = re.split(r'\s+', product_price)
                        # product_price = " ".join(product_price_re)
                    elif len(product_data) == 25:
                        product_price = product_data[16].find('div', class_="relative mt-1 w-full").find('span',
                                                                                                         class_="text-xl").text.strip().replace(
                            " ", "").replace("\n", " ")
                        # product_price_re = re.split(r'\s+', product_price)
                        # product_price = " ".join(product_price_re)
                    else:
                        product_price = product_data[12].find('div', class_="relative mt-1 w-full").find('span',
                                                                                                         class_="text-xl").text.strip().replace(
                            " ", "").replace("\n", " ")
                        # product_price_re = re.split(r'\s+', product_price)
                        # product_price = "".join(product_price_re)
                except:
                    product_price = "No data available!"

                try:
                    product_link = product_data[0].find_all('a')[-1].get('href')
                except:
                    product_link = "No data available!"

                products_data.append(
                    {
                        "Title": product_title,
                        "Discount": product_discount,
                        "Price": product_price,
                        "URL-LINK": product_link
                    }
                )
                try:
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
                except Exception as err:
                    print(err)
            else:
                products_data.append(
                    {
                        "Title": product_data_sale,
                        "Discount": product_data_sale,
                        "Price": product_price,
                        "URL-LINK": product_link
                    }
                )
                try:
                    with open(f"Товары по Акции_{cur_time}.csv", "a", encoding="cp1251", newline="") as file:
                        writer = csv.writer(file, delimiter=";")

                        writer.writerow(
                            (
                                product_title,
                                product_data_sale,
                                product_price,
                                product_link
                            )
                        )
                except Exception as err:
                    print(err)

        print(f"Обработана {page} / {pages_count}")
        time.sleep(2)

    with open(f"Товары по Акции_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"Затраченно на работу скрипта времени: {finish_time}")


if __name__ == "__main__":
    main()
