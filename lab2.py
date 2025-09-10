a = [1, "age", 55, "height", "name", 43, 21, "is_student",
     111, "grades", 9, "coordinates", "person", 78,
     "unique_numbers", 34, 23, "b", "f", 90]

numbers = sorted([x for x in a if isinstance(x, int)])
words = sorted([x for x in a if isinstance(x, str)], key=str.lower)
sorted_list = numbers + words

b = [x for x in numbers if x % 2 == 0]

c= [x.upper() for x in words]

print("Оригінальний список:", a)
print("Відсортований список:", sorted_list)
print("Список чисел, кратних 2:",b)
print("Список рядків у капс:", c)
