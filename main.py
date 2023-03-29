import json

import requests
from fake_useragent import UserAgent


def collect_data():
    ua = UserAgent()
    page = max_page = 1
    total_count = 0
    result = {}

    print('===START===')
    while True:
        try:
            url = f'https://market.dota2.net/ajax/price/Arcana/Обычная/all/{page}/56/0;500000/all/all?sd=asc'
            response = requests.get(url, headers={'User-Agent': ua.random})
            response.raise_for_status()

            data = response.json()
            if page == 1:
                max_page = data[1]

            count = 0
            for item in data[0]:
                item_name = item[8]
                
                if any(part_str in item_name.lower() for part_str in ('call', 'rune', 'voice', 'bundle')):
                    continue

                if any(item_name == product['full_name'] for product in result.values()):
                    continue

                item_price = item[3]
                item_image_url = f'https://cdn.dota2.net//item/{item_name.replace(" ", "%20")}/100.png'
                item_url = f'https://market.dota2.net/item/{item[0]}-{item[1]}-{item_name.replace(" ", "%20")}/'
                result[total_count + count] = {
                    'full_name': item_name,
                    'price': item_price,
                    'image_url': item_image_url,
                    'url': item_url,
                }
                count += 1
            total_count += count

            print(f'Page#{page} / #{max_page} - Items = {count} - Total = {total_count} - Completed')
            if total_count >= 30 or page >= max_page:
                print('====END====')
                break
            page += 1

        except requests.exceptions.RequestException as err:
            print('====END====')
            print(f"Unexpected {err=}, {type(err)=}")
            break

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    return total_count


def main():
    total_count = collect_data()
    if total_count == 0:
        print('Предметов на данный момент нет!')


if __name__ == '__main__':
    main()
