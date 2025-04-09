import requests

async def weather(message,token):
    city = message.text.strip()

    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={token}&units=metric&lang=ua"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"]
                await message.answer(
                    f"Погода у місті <b>{city}</b>:\n"
                    f"Температура: {temp}°C\n"
                    f"Опис: {description}", parse_mode="HTML"
                )
            else:
                await message.answer(
                    "Не вдалося отримати дані про погоду. Перевірте назву міста."
                )