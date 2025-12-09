import telebot
import random
import sqlite3
import threading
from datetime import datetime, timedelta
from telebot import types

TOKEN = "7672161454:AAHPnNbqwHU_EMmLIsnzw1bfJna9MalesX0"
bot = telebot.TeleBot(TOKEN)

# --- База і lock ---
conn = sqlite3.connect("casino.db", check_same_thread=False)
sql = conn.cursor()
sql_lock = threading.Lock()

with sql_lock:
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
    conn.commit()

# --- Функції для роботи з БД ---
def get_user(user_id):
    with sql_lock:
        sql.execute("SELECT balance, last_bonus FROM users WHERE tg_id=?", (user_id,))
        row = sql.fetchone()
        if row is None:
            starting_balance = 1000
            now_iso = datetime.now().isoformat()
            sql.execute("INSERT INTO users (tg_id, balance, last_bonus) VALUES (?, ?, ?)",
                        (user_id, starting_balance, now_iso))
            conn.commit()
            return starting_balance, now_iso
        return row[0], row[1]

def update_balance(user_id, amount):
    with sql_lock:
        sql.execute("UPDATE users SET balance = balance + ? WHERE tg_id=?", (amount, user_id))
        conn.commit()

def add_history(user_id, game, bet, result):
    with sql_lock:
        sql.execute("INSERT INTO history (tg_id, game, bet, result, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (user_id, game, bet, result, datetime.now().isoformat()))
        conn.commit()

def fetch_history(user_id, limit=10):
    with sql_lock:
        sql.execute("SELECT game, bet, result, timestamp FROM history WHERE tg_id=? ORDER BY id DESC LIMIT ?", (user_id, limit))
        rows = sql.fetchall()
    return rows

def fetch_top(limit=10):
    with sql_lock:
        sql.execute("SELECT tg_id, balance FROM users ORDER BY balance DESC LIMIT ?", (limit,))
        rows = sql.fetchall()
    return rows

# --- Команди ---
@bot.message_handler(commands=["start"])
def start(msg):
    get_user(msg.from_user.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎲 Кості", callback_data="dice_info"))
    markup.add(types.InlineKeyboardButton("🎰 Слоти", callback_data="slots_info"))
    bot.send_message(msg.chat.id,
                     "🎰 Вітаю у *Casino Bot*! Вибери гру нижче або використай команди:\n"
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
        try:
            last = datetime.fromisoformat(last_bonus)
            if now - last < timedelta(days=1):
                bot.send_message(msg.chat.id, "⏳ Бонус можна отримати тільки раз на добу!")
                return
        except:
            pass
    with sql_lock:
        sql.execute("UPDATE users SET balance = balance + 100, last_bonus = ? WHERE tg_id=?",
                    (now.isoformat(), user_id))
        conn.commit()
    add_history(user_id, "bonus", 0, "+100 бонус")
    bot.send_message(msg.chat.id, "🎁 Бонус отримано! +100 кредитів")

@bot.message_handler(commands=["history"])
def history(msg):
    rows = fetch_history(msg.from_user.id)
    if not rows:
        bot.send_message(msg.chat.id, "Історія порожня 😢")
        return
    text = "📜 Історія останніх ігор:\n"
    for row in rows:
        game, bet, result, timestamp = row
        text += f"{timestamp[:19]} | {game} | ставка: {bet} | {result}\n"
    bot.send_message(msg.chat.id, text)

@bot.message_handler(commands=["top"])
def top(msg):
    rows = fetch_top()
    if not rows:
        bot.send_message(msg.chat.id, "Поки що немає гравців.")
        return
    text = "🏆 Топ гравців за балансом:\n"
    for i, row in enumerate(rows, 1):
        text += f"{i}. ID: {row[0]} — {row[1]} кредитів\n"
    bot.send_message(msg.chat.id, text)

# --- Callback ---
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    if call.data.endswith("_info"):
        send_game_info(call)
    elif call.data.endswith("_play"):
        play_game(call)

# --- Інформація про гру ---
def send_game_info(call):
    text = ""
    markup = types.InlineKeyboardMarkup()
    if call.data == "dice_info":
        text = "🎲 *Кості*\nКидаєш два кубики. Сума ≥7 → виграш x2, інакше програш. Ставка: 50 кредитів."
        markup.add(types.InlineKeyboardButton("▶️ Грати (50)", callback_data="dice_play"))
    elif call.data == "slots_info":
        text = "🎰 *Слоти*\nТри символи. 3 однакових → x5 ставки, 2 однакових → x2 ставки. Ставка: 50 кредитів."
        markup.add(types.InlineKeyboardButton("▶️ Грати (50)", callback_data="slots_play"))
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# --- Ігри ---
def play_game(call):
    user_id = call.from_user.id
    bal, _ = get_user(user_id)
    bet = 50
    if bal < bet:
        bot.send_message(call.message.chat.id, "😢 У тебе замало грошей для ставки (мінімум 50).")
        return

    # Кості
    if call.data == "dice_play":
        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        total = d1 + d2
        if total >= 7:
            win = bet * 2
            update_balance(user_id, win)
            outcome = f"🎉 Виграш! +{win}"
        else:
            update_balance(user_id, -bet)
            outcome = f"❌ Програш {bet}"
        add_history(user_id, "Кості", bet, f"{outcome} | {d1}+{d2}={total}")
        bal_after, _ = get_user(user_id)
        bot.send_message(call.message.chat.id, f"{outcome}\n🎲 Результат: {d1} + {d2} = {total}\n💰 Баланс: {bal_after}")

    # Слоти
    elif call.data == "slots_play":
        symbols = ["🍒","🍋","🍀","💎","🔔"]
        result = [random.choice(symbols) for _ in range(3)]
        if result[0]==result[1]==result[2]:
            win = bet*5
        elif result[0]==result[1] or result[1]==result[2] or result[0]==result[2]:
            win = bet*2
        else:
            win = 0
        update_balance(user_id, win - bet)
        outcome = f"Виграш {win}" if win>0 else f"Програш {bet}"
        add_history(user_id, "Слоти", bet, f"{outcome} | {' '.join(result)}")
        bal_after, _ = get_user(user_id)
        bot.send_message(call.message.chat.id, f"{' '.join(result)}\n{outcome}\n💰 Баланс: {bal_after}")

# --- Запуск ---
if __name__ == "__main__":
    print("Bot started...")
    bot.infinity_polling(timeout=60, long_polling_timeout=5)
