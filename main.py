import json

import requests
from fake_useragent import UserAgent

ua = UserAgent()


def collect_data():
    page = max_page = 1
    count = total_count = 0
    flag = True
    result = {}

    while True:
        try:
            url = f'https://market.dota2.net/ajax/price/Arcana/Обычная/all/{page}/56/0;500000/all/all?sd=asc'
            response = requests.get(
                url=url,
                headers={'user-agent': f'{ua.random}'}
            )

            data = response.json()
            if flag:
                max_page = data[1]
                flag = False

            for item in data[0]:
                item_to_url = item[8].replace(' ', '%20')
                condition = True
                if len(result) != 0:
                    for product in result.values():
                        if item[8] == product['full_name']:
                            condition = False
                if condition and \
                        all(part_str not in item[8].lower() for part_str in ('call', 'rune', 'voice', 'bundle')):
                    item_price = item[3]
                    item_image_url = f'https://cdn.dota2.net//item/{item_to_url}/100.png'
                    item_url = f'https://market.dota2.net/item/{item[0]}-{item[1]}-{item_to_url}/'
                    result[total_count + count] = {
                        'full_name': item[8],
                        'price': item_price,
                        'image_url': item_image_url,
                        'url': item_url
                    }
                    count += 1
            total_count += count
            print(
                f'Page#{page} / #{max_page} - Items = {count} - Total = {total_count} - Completed')
            if total_count >= 30:
                break
            count = 0
            page += 1
            if page <= max_page:
                continue
            else:
                print('===END===')
                break
        except Exception as err:
            print('===END===')
            print(f"Unexpected {err=}, {type(err)=}")
            break

    with open('result.json', 'w') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    return total_count


def main():
    total_count = collect_data()
    if total_count == 0:
        print('Предметов на данный момент нет!')


if __name__ == '__main__':
    main()
