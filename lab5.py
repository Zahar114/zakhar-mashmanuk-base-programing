import matplotlib.pyplot as plt #графік
import emoji #смайлики
import requests #запит з сайту
import numpy as np #масиви
import pandas as pd #таблиця
import pillow #обробка зображень
import pygame #для ігор
import colorama #виведення кольорового тексту і фону
import termcolor #теж для тексту але легший
import pyfiglet #для ASCII артів

# Блок 1: matplotlib
try: #пробує виконати 
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.title("Графік")
    plt.savefig("grafik.png")
    plt.close()
    print("Графік збережено як grafik.png")
except Exception as e: #ловить помилку
    print("Matplotlib error:", e) #і прінтить 

# Блок 2: emoji
try:
    print(emoji.emojize("Привіт, Python :thumbs_up:"))
except Exception as e:
    print("Emoji error:", e)

# Блок 3: requests
try:
    r = requests.get("https://httpbin.org/get")
    print("Requests статус код:", r.status_code)
except Exception as e:
    print("Requests error:", e)

# Блок 4: numpy
try:
    arr = np.array([1, 2, 3, 4])
    print("Середнє значення масиву numpy:", np.mean(arr))
except Exception as e:
    print("Numpy error:", e)

# Блок 5: pandas
try:
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    print("DataFrame pandas:\n", df)
except Exception as e:
    print("Pandas error:", e)
