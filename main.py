import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook


def get_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    # Списки для столбцов
    page_names = []
    page_prices_live = []
    page_prices = []

    hotels_cards = soup.find_all("div", class_="catalog_list")

    for good_info in hotels_cards:
        prices_lives = good_info.find_all("div", class_="cli_price_live")
        names = good_info.find_all('a', class_='cli_title')
        prices = good_info.find_all('div', class_="cli_price")

        for name in names:
            page_names.append(name.text.strip().replace('"', ''))
        for price_live in prices_lives:
            page_prices_live.append(price_live.text.strip().replace('.', ''))
        for price in prices:
            page_prices.append(price.text.strip().replace('.', ''))

    return page_names, page_prices_live, page_prices


def main():
    fn = "file_path.xlsx" # вставьте сюда путь к файлу
    wb = load_workbook(fn)
    ws = wb['Тест']
    ws.append(['Название', 'Розничная цена', 'Оптовая цена'])
    for i in range(1, 837):
        print(f"Парсинг страницы {i}...")
        page_names, page_prices_live, page_prices = get_data(f"https://doka-baza.ru/catalog/?PAGEN_1={i}")

        for name, price_live, price in zip(page_names, page_prices_live, page_prices):
            ws.append([name, price_live, price])

    # Сохраняем
    wb.save(fn)
    wb.close()

print("Данные успешно сохранены")


if __name__ == '__main__':
    main()