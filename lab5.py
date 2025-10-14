import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw
from faker import Faker
from dateutil import parser
import pytest
from rich.console import Console

console = Console()

# 5 блоків try/except з використанням різних бібліотек

# 1. requests
try:
    response = requests.get('https://api.github.com')
    console.print(f"[green]Requests response status:[/green] {response.status_code}")
except Exception as e:
    console.print(f"[red]Requests error:[/red] {e}")

# 2. numpy
try:
    arr = np.array([1, 2, 3, 4, 5])
    console.print(f"[green]Numpy array sum:[/green] {np.sum(arr)}")
except Exception as e:
    console.print(f"[red]Numpy error:[/red] {e}")

# 3. pandas
try:
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    console.print(f"[green]Pandas DataFrame head:[/green]\n{df.head()}")
except Exception as e:
    console.print(f"[red]Pandas error:[/red] {e}")

# 4. Pillow
try:
    img = Image.new('RGB', (100, 100), color='blue')
    draw = ImageDraw.Draw(img)
    draw.text((10, 40), "Hello", fill='white')
    img.save("test_image.png")
    console.print(f"[green]Image created and saved[/green]")
except Exception as e:
    console.print(f"[red]Pillow error:[/red] {e}")

# 5. Faker
try:
    fake = Faker()
    console.print(f"[green]Fake name:[/green] {fake.name()}")
except Exception as e:
    console.print(f"[red]Faker error:[/red] {e}")
