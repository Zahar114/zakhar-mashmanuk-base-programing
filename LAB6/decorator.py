import time

def delay(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Затримка виконання на {seconds} секунд...")
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator