import requests

def currency(bot, message):
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        usd_data = next((item for item in data if item["cc"] == "USD"), None)
        eur_data = next((item for item in data if item["cc"] == "EUR"), None)
        gbp_data = next((item for item in data if item["cc"] == "GBP"), None)
        bot.send_message(
            message.chat.id,
            "Ось поточний курс валют:\n"
            f"💵 USD: {usd_data['rate']}\n"
            f"💶 EUR: {eur_data['rate']}\n"
            f"💷 GBP: {gbp_data['rate']}\n"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Не вдалося отримати дані про курси валют. Спробуйте пізніше."
        )
