from flask import Flask, request
import requests
import datetime

app = Flask(__name__)

# 🔹 COLOQUE AQUI O SEU TOKEN DO BOT
TOKEN = "TOKEN = "8003613789:AAE8GMU2LMuelsPTwd5hdVSaOdfc65LbR1w"
"

# 🔹 COLOQUE AQUI OS IDS DOS ADMINISTRADORES ENTRE COLCHETES
ADMIN_IDS = [8450036914, 5851719492, 7628586863, 5870846984]

@app.route('/')
def home():
    return "✅ Bot Liana ativo!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Verifica se é um novo membro entrando
    if "message" in data and "new_chat_members" in data["message"]:
        for member in data["message"]["new_chat_members"]:
            nome = member.get("first_name", "Desconhecido")
            user_id = member.get("id")
            horario = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            texto = (
                f"👋 <b>Novo membro no grupo!</b>\n\n"
                f"<b>Nome:</b> {nome}\n"
                f"<b>ID:</b> <code>{user_id}</code>\n"
                f"<b>Horário:</b> {horario}"
            )

            # Envia mensagem para todos os administradores
            for admin in ADMIN_IDS:
                requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    json={"chat_id": admin, "text": texto, "parse_mode": "HTML"}
                )

    return "ok", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
