import requests

def main():
    city_name = "Moscow"
    api_key = "115f2f570d920e3f91af622d5e3e6c73"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&lang=ru&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()

        weather = result["weather"][0]["description"]
        print(f"Погода: {weather}")

        temp = result["main"]["temp"]
        print(f"Температура: {temp} C°")

        humidity = result["main"]["humidity"]
        print(f"Влажность: {humidity}%")

        pressure = result["main"]["pressure"]
        print(f"Давление: {pressure} гПа")
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")


if __name__ == '__main__':
    main()