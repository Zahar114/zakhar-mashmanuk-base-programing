def format_price(price):
    "'Ціна: xxx.xx грн'"
    return f"Ціна: {price:.2f} грн"


def check_availability(*items):
    "Перевіряє, які товари є в наявності"
    store_items = {
        "хліб": True,
        "молоко": True,
        "сир": False,
        "яблуко": True,
        "цукор": False
    }

    result = {}
    for item in items:
        result[item] = store_items.get(item, False)
    return result


def make_order(order):
    "Створює замовлення, якщо всі товари є в наявності"
    prices = {
        "хліб": 20.50,
        "молоко": 35.75,
        "сир": 100.00,
        "яблуко": 15.30,
        "цукор": 28.00
    }

    availability = check_availability(*order)

    if not all(availability.values()):
        print(" Не всі товари є в наявності. Замовлення неможливе.")
        print("Стан товарів:", availability)
        return

    total = sum(prices[item] for item in order)
    print(" Усі товари в наявності!")
    print("Загальна сума:", format_price(total))


def shop():
    "Основне меню користувача"
    prices = {
        "хліб": 20.50,
        "молоко": 35.75,
        "сир": 100.00,
        "яблуко": 15.30,
        "цукор": 28.00
    }

    while True:
        print("\nОберіть дію:")
        print("1 — Переглянути ціну товару")
        print("2 — Купити товари")
        print("3 — Вихід")

        choice = input("Ваш вибір: ")

        if choice == "1":
            item = input("Введіть назву товару: ").strip().lower()
            if item in prices:
                print(format_price(prices[item]))
            else:
                print(" Такого товару немає у прайсі.")

        elif choice == "2":
            order = input("Введіть товари через кому: ").split(",")
            order = [x.strip().lower() for x in order]
            make_order(order)

        elif choice == "3":
            print("Дякуємо за відвідування магазину! ")
            break

        else:
            print(" Невірний вибір. Спробуйте ще раз.")


#  Запуск програми
shop()
