import os
from dotenv import load_dotenv
import requests
import argparse


def get_course(currency, api_key):
    try:
        response = requests.get(f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}")
        response.raise_for_status()
        course = response.json()["conversion_rates"]
    except requests.HTTPError:
        print("HTTPError! Что-то не так с Api запросом!")
        exit()
    return course


def convert_amount(course, target_rate, amount):
    return course[target_rate] * amount


def main():
    load_dotenv()
    api_key = os.environ["EXCHANGERATE_API_KEY"]
    parser = argparse.ArgumentParser(description="Программа переводит указанную сумму из одной валюты в требуемую.")
    parser.add_argument("-b", "--base", help="Введите начальную валюту. (По умолчанию рубли)", required=False, default="RUB")
    parser.add_argument("-t", "--target", help="Введите целевую валюту. (По умолчанию иены)", required=False, default="JPY")
    parser.add_argument("-a", "--amount", help="Введите сумму. (По умолчанию 1000)", required=False, default="1000")
    args = parser.parse_args()
    course = get_course(args.base, api_key)
    target_rate = args.target
    print(f"Итоговая сумма: {convert_amount(course, target_rate, int(args.amount))} {target_rate}")


if __name__ == "__main__":
    main()
