students = {}

print("Введіть ім'я студента та його оцінку (для завершення введення напишіть 'stop').")

while True:
    name = input("Ім'я студента: ").strip()
    if name.lower() == "stop":
        break

    try:
        grade = int(input("Оцінка (1-12): "))
        if 1 <= grade <= 12:
            students[name] = grade
        else:
            print(" Оцінка має бути від 1 до 12!")
    except ValueError:
        print(" Потрібно вводити число!")

# Виведення результатів
print("\n Результати:")
for name, grade in students.items():
    print(f"{name}: {grade}")

# Обчислення статистики
if students:
    average = sum(students.values()) / len(students)
    excellent = {name: grade for name, grade in students.items() if 10 <= grade <= 12}
    good = {name: grade for name, grade in students.items() if 7 <= grade <= 9}
    bad = {name: grade for name, grade in students.items() if 4 <= grade <= 6}
    failed = {name: grade for name, grade in students.items() if 1 <= grade <= 3}

    print(f"\n Середній бал групи: {average:.2f}")
    print(f" Відмінники (10-12): {len(excellent)} — {', '.join(excellent.keys()) if excellent else 'немає'}")
    print(f" Хорошисти (7-9): {len(good)} — {', '.join(good.keys()) if good else 'немає'}")
    print(f" Відстаючі (4-6): {len(bad)} — {', '.join(bad.keys()) if bad else 'немає'}")
    print(f" Не здали (1-3): {len(failed)} — {', '.join(failed.keys()) if failed else 'немає'}")
else:
    print("Немає введених студентів.")