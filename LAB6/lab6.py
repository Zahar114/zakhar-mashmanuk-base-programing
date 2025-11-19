from decorator import delay # type: ignore

@delay(2)   # Затримка 2 секунди
def divide(a, b):
    if b == 0:
        return "Ділити на нуль не можна"
    return a / b

print(divide(10, 2))