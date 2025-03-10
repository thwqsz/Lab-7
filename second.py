import requests


def fetch_data(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Вызывает ошибку, если статус не 200
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None


def display_character_info(character_id):
    url = f"https://rickandmortyapi.com/api/character/{character_id}"
    data = fetch_data(url)

    if not data:
        print("Не удалось получить данные.")
        return

    print("\nИнформация о персонаже:")
    print(f"ID: {data['id']}")
    print(f"Имя: {data['name']}")
    print(f"Вид: {data['species']}")
    print(f"Родная планета: {data['origin']['name']}")
    print(f"Местоположение: {data['location']['name']}")
    print(f"Статус: {data['status']}")
    print(f"Пол: {data['gender']}")

    if data["type"]:
        print(f"Тип: {data['type']}")

    print(f"Дата создания: {data['created']}")
    print("-" * 40)


def display_character_list(character_list):
    print("\nНайденные персонажи:")
    for character in character_list:
        print(f"{character['id']} - {character['name']}")


def main():
    print("Программа для поиска персонажей \"Rick and Morty\"")
    print("Введите имя персонажа или оставьте пустым для поиска всех.")
    print("Введите \"quit\", чтобы выйти.\n")

    while True:
        search_query = input("Введите имя персонажа: ").strip()
        if search_query.lower() == "quit":
            break

        url = f"https://rickandmortyapi.com/api/character/?name={search_query}"
        data = fetch_data(url)

        if not data or "results" not in data:
            print("Персонаж не найден. Попробуйте ещё раз.")
            continue

        total_characters = data["info"]["count"]
        print(f"\nНайдено {total_characters} персонажей.")

        pages = data["info"]["pages"]

        for page in range(1, pages + 1):
            print(f"\nСтраница {page} из {pages}:")
            display_character_list(data["results"])

            id_input = input("Введите ID персонажа (или Enter для следующей страницы): ").strip()

            if id_input.lower() == "quit":
                return

            if id_input.isdigit():
                display_character_info(int(id_input))
                break

            if page < pages:
                next_url = data["info"]["next"]
                data = fetch_data(next_url)
                if not data:
                    print("Ошибка при загрузке следующей страницы.")
                    break



if __name__ == '__main__':
    main()
