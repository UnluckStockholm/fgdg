from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

# Токен основного бота
TELEGRAM_BOT_TOKEN = "8360366118:AAF96StnUXzgyHYB-W0K_SBO7pK2DnUF2mo"

# Telegram ID администратора
ADMIN_CHAT_ID = 6685441594

# ID Telegram-группы (бот должен быть в ней и иметь права)
GROUP_CHAT_ID = -1002610049448

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "text": text,
        "parse_mode": "Markdown"
    }
    # Отправка админу
    requests.post(url, data={**payload, "chat_id": ADMIN_CHAT_ID})
    # Отправка в группу
    requests.post(url, data={**payload, "chat_id": GROUP_CHAT_ID})

@app.route("/payment/result", methods=["GET", "POST"])
def payment_result():
    if request.method == "POST":
        data = request.form or request.json or {}
        status = data.get("status", "-").lower()
        amount = data.get("amount", "-")
        transaction_id = data.get("transaction_id", "-")
        timestamp = get_timestamp()

        if status == "paid":
            message = (
                f"✅ *Оплата подтверждена*\n"
                f"💰 Сумма: `{amount}`\n"
                f"🆔 Транзакция: `{transaction_id}`\n"
                f"🕒 Время: `{timestamp}`"
            )
        else:
            message = (
                f"❌ *Оплата отклонена*\n"
                f"🆔 Транзакция: `{transaction_id}`\n"
                f"🕒 Время: `{timestamp}`"
            )

        send_message(message)
        return "OK", 200
    else:
        return "<h3>🔔 Этот маршрут предназначен для POST-запросов от платёжной системы.</h3>"

@app.route("/payment/success", methods=["GET", "POST"])
def payment_success():
    timestamp = get_timestamp()
    message = f"✅ *Платёж успешен*\n🕒 Время: `{timestamp}`"
    send_message(message)
    return "<h2>✅ Оплата прошла успешно. Спасибо за покупку!</h2>"

@app.route("/payment/fail", methods=["GET", "POST"])
def payment_fail():
    timestamp = get_timestamp()
    message = f"❌ *Ошибка оплаты*\n🕒 Время: `{timestamp}`"
    send_message(message)
    return "<h2>❌ Оплата не удалась. Попробуйте снова или свяжитесь с поддержкой.</h2>"

@app.route("/payment/refund", methods=["GET", "POST"])
def payment_refund():
    if request.method == "POST":
        data = request.form or request.json or {}
        reason = data.get("reason", "не указана")
        transaction_id = data.get("transaction_id", "-")
        timestamp = get_timestamp()

        message = (
            f"🔁 *Возврат платежа*\n"
            f"🆔 Транзакция: `{transaction_id}`\n"
            f"📝 Причина: `{reason}`\n"
            f"🕒 Время: `{timestamp}`"
        )
        send_message(message)
        return "OK", 200
    else:
        return "<h3>🔁 Этот маршрут предназначен для POST-запросов от платёжной системы.</h3>"

@app.route("/payment/chargeback", methods=["GET", "POST"])
def payment_chargeback():
    if request.method == "POST":
        data = request.form or request.json or {}
        reason = data.get("reason", "не указана")
        transaction_id = data.get("transaction_id", "-")
        timestamp = get_timestamp()

        message = (
            f"⚠️ *Чарджбэк!*\n"
            f"🆔 Транзакция: `{transaction_id}`\n"
            f"🚨 Причина: `{reason}`\n"
            f"🕒 Время: `{timestamp}`"
        )
        send_message(message)
        return "OK", 200
    else:
        return "<h3>🚨 Этот маршрут обрабатывает только POST-запросы от платёжной системы.</h3>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    @app.route("/")
    def home():
        return "<h2>🚀 Сервис работает! Используйте POST-запросы на /payment/*</h2>"