import random
import string

# --- Етап 1: Створення текстового файлу ---
def create_text_file(filename="text.txt", lines=100, chars_per_line=100):
    """Створює текстовий файл з випадковим текстом"""
    with open(filename, "w", encoding="utf-8") as f:
        for _ in range(lines):
            # Генеруємо рядок з літер і пробілів
            line = ''.join(random.choices(string.ascii_lowercase + " ", k=chars_per_line))
            f.write(line + "\n")

create_text_file()


# --- Етап 2: Генератор пар букв ---
def letter_pairs_generator(filename="text.txt"):
    """Генератор, який повертає по 3 унікальні пари букв з кожного рядка"""
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            pairs = set()  # для зберігання унікальних пар

            # Рахуємо пари всередині слів
            words = line.split()
            for word in words:
                for i in range(len(word) - 1):
                    pair = word[i:i+2]
                    pairs.add(pair)

            # Беремо 3 випадкові пари
            pairs_list = list(pairs)
            if len(pairs_list) <= 3:
                selected_pairs = pairs_list
            else:
                selected_pairs = random.sample(pairs_list, 3)

            yield selected_pairs


# --- Приклад використання ---
for i, pairs in enumerate(letter_pairs_generator(), 1):
    print(f"Рядок {i}: {pairs}")

