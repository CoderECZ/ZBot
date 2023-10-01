from flask import Flask, request, jsonify
from pyngrok import ngrok
import requests, json

# Receives the webhook from PayPal and then redirects it to the bot via a webhook

app = Flask(__name__)

with open('config.json', "r") as f:
    config = json.load(f)

webhookClient = 'https://discord.com/api/webhooks/id/token'
webhookClient = {
    'id': "id",
    'token': "token"
}
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get PayPal webhook data
    data = json.loads(request.get_data(as_text=True))

    # Extract specific data from the invoice payload
    if 'resource' in data and data['resource_type'] == 'invoices':
        
        invoice_no = data['resource']['number']
    
    print(invoice_no)
    return jsonify({'status': 'success'})

@app.route('/forward', methods=['POST'])
def forward_to_webhook():
    try:
        data = request.get_json()
        response = requests.post(WEBHOOK_URL, json=data)
        print(response.text)
        return jsonify({"message": "Request forwarded to webhook", "response": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    public_url = ngrok.connect(port=4040)
    print(' * ngrok tunnel "{}" -> "http://127.0.0.1:{}/"'.format(public_url, 4040))

    app.run(port=4040)