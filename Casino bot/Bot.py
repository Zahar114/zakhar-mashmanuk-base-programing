import telebot
import random
import sqlite3
from datetime import datetime, timedelta
from telebot import types

TOKEN = "7672161454:AAHPnNbqwHU_EMmLIsnzw1bfJna9MalesX0"  # встав свій токен
bot = telebot.TeleBot(TOKEN)

# --- База ---
db = sqlite3.connect("casino.db", check_same_thread=False)
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    tg_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 500,
    last_bonus TEXT
)""")
sql.execute("""CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER,
    game TEXT,
    bet INTEGER,
    result TEXT,
    timestamp TEXT
)""")
db.commit()

# --- Функції ---
def get_user(user_id):
    sql.execute("SELECT balance, last_bonus FROM users WHERE tg_id=?", (user_id,))
    data = sql.fetchone()
    if not data:
        sql.execute("INSERT INTO users (tg_id, balance, last_bonus) VALUES (?, 1000, ?)",
                    (user_id, datetime.now().isoformat()))
        db.commit()
        return 1000, None
    return data

def update_balance(user_id, amount):
    sql.execute("UPDATE users SET balance = balance + ? WHERE tg_id=?", (amount, user_id))
    db.commit()

def add_history(user_id, game, bet, result):
    sql.execute("INSERT INTO history (tg_id, game, bet, result, timestamp) VALUES (?, ?, ?, ?, ?)",
                (user_id, game, bet, result, datetime.now().isoformat()))
    db.commit()

# --- Команди ---
@bot.message_handler(commands=["start"])
def start(msg):
    get_user(msg.from_user.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎲 Кості", callback_data="dice_info"))
    markup.add(types.InlineKeyboardButton("🎰 Слоти", callback_data="slots_info"))
    bot.send_message(msg.chat.id,
                     "🎰 Вітаю у *Casino Bot*! Вибери гру нижче або команди:\n"
                     "/balance - баланс\n"
                     "/bonus - щоденний бонус\n"
                     "/history - історія\n"
                     "/top - топ гравців",
                     reply_markup=markup,
                     parse_mode="Markdown")

@bot.message_handler(commands=["balance"])
def balance(msg):
    bal, _ = get_user(msg.from_user.id)
    bot.send_message(msg.chat.id, f"💰 Баланс: {bal}")

@bot.message_handler(commands=["bonus"])
def bonus(msg):
    user_id = msg.from_user.id
    bal, last_bonus = get_user(user_id)
    now = datetime.now()
    if last_bonus:
        last = datetime.fromisoformat(last_bonus)
        if now - last < timedelta(days=1):
            bot.send_message(msg.chat.id, "⏳ Бонус можна отримати лише 1 раз на добу!")
            return
    sql.execute("UPDATE users SET balance = balance + 100, last_bonus = ? WHERE tg_id=?",
                (now.isoformat(), user_id))
    db.commit()
    bot.send_message(msg.chat.id, "🎁 +100 кредитів! Приходь завтра!")

@bot.message_handler(commands=["history"])
def history(msg):
    sql.execute("SELECT game, bet, result, timestamp FROM history WHERE tg_id=? ORDER BY id DESC LIMIT 10", (msg.from_user.id,))
    rows = sql.fetchall()
    if not rows:
        bot.send_message(msg.chat.id, "Історія порожня 😢")
        return
    text = "📜 Історія останніх 10 ігор:\n"
    for row in rows:
        text += f"{row[3][:19]} | {row[0]} | ставка: {row[1]} | {row[2]}\n"
    bot.send_message(msg.chat.id, text)

@bot.message_handler(commands=["top"])
def top(msg):
    sql.execute("SELECT tg_id, balance FROM users ORDER BY balance DESC LIMIT 10")
    rows = sql.fetchall()
    text = "🏆 Топ гравців за балансом:\n"
    for i, row in enumerate(rows, 1):
        text += f"{i}. ID: {row[0]} | Баланс: {row[1]}\n"
    bot.send_message(msg.chat.id, text)

# --- Callback для кнопок ---
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.answer_callback_query(call.id)  # відповідаємо на callback
    if call.data.endswith("_info"):
        send_game_info(call)
    elif call.data.endswith("_play"):
        play_game(call)

# --- Інформація про гру ---
def send_game_info(call):
    text = ""
    markup = types.InlineKeyboardMarkup()
    if call.data == "dice_info":
        text = "🎲 *Кості*\nКидаєш два кубики (1-6). Сума ≥7 → виграш x2, інакше програш. Ставка: 50 кредитів."
        markup.add(types.InlineKeyboardButton("▶️ Грати", callback_data="dice_play"))
    elif call.data == "slots_info":
        text = "🎰 *Слоти*\nТри символи. 3 однакових → x5 ставки, 2 однакових → x2 ставки. Ставка: 50 кредитів."
        markup.add(types.InlineKeyboardButton("▶️ Грати", callback_data="slots_play"))
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# --- Ігри ---
def play_game(call):
    user_id = call.from_user.id
    bal, _ = get_user(user_id)
    bet = 50
    if bal < bet:
        bot.send_message(call.message.chat.id, "😢 У тебе замало грошей для ставки (50)")
        return

    if call.data == "dice_play":
        roll = random.randint(1,6) + random.randint(1,6)
        if roll >= 7:
            win = bet*2
            update_balance(user_id, win)
            outcome = f"🎉 Виграш! +{win}"
        else:
            update_balance(user_id, -bet)
            outcome = f"❌ Програш {bet}"
        add_history(user_id, "Кості", bet, outcome)
        bot.send_message(call.message.chat.id, f"{outcome}\n🎲 Сума кубиків: {roll}\n💰 Баланс: {get_user(user_id)[0]}")

    elif call.data == "slots_play":
        symbols = ["🍒","🍋","🍀","💎","🔔"]
        result = [random.choice(symbols) for _ in range(3)]
        if result[0]==result[1]==result[2]:
            win = bet*5
        elif result[0]==result[1] or result[1]==result[2] or result[0]==result[2]:
            win = bet*2
        else:
            win = 0
        update_balance(user_id, win-bet)
        outcome = f"Виграш {win}" if win>0 else f"Програш {bet}"
        add_history(user_id, "Слоти", bet, outcome + " " + " ".join(result))
        bot.send_message(call.message.chat.id, f"{' '.join(result)}\n{outcome}\n💰 Баланс: {get_user(user_id)[0]}")

# --- Запуск ---
bot.polling()
