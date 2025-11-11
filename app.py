from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ativo!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    print("🔔 Atualização recebida:", update, flush=True)
    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
