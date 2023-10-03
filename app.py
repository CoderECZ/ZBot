from flask import Flask, request, jsonify
from pyngrok import ngrok
import requests, json

from cogs.invoice import Invoice
from cogs.utilities import Utilites

# Receives the webhook from PayPal and then redirects it to the bot via a webhook

app = Flask(__name__)

with open('config.json', "r") as f:
    config = json.load(f)

headers = {
    'Authorization': f'Bearer {config["paypalapi"]}',
    'Content-Type': 'application/json',
}

ngrok_url = ngrok.connect(5000)
paypal_webhook_url = str(ngrok_url).replace('http', 'https') + "/webhook"

@app.route('/webhook', methods=['POST'])
def webhook():
    '''Receives webhooks from PayPal.'''
    # Get PayPal webhook data
    data = json.loads(request.get_data(as_text=True))

    # Extract specific data from the invoice payload
    if 'resource' in data and data['resource_type'] == 'invoices':
        invoice_no = data['resource']['number']
        print(invoice_no)
        api(invoice_no)

    return '', 200  # Return a 200 OK response to PayPal

def api(invoice_no: int):
    '''Processes the invoice number and fetches the full invoice details from PayPal, processes the JSON payload for use in further functions.'''
    response = requests.get(f'https://api-m.sandbox.paypal.com/v2/invoicing/invoices/{invoice_no}', headers=headers)

    data = response.json()
    
    status = data.get('status')
    detail = data.get('detail', {}) # Inside data container
    invoice_number = detail.get('invoice_number')
    reference = detail.get('memo')
    invoicer = data.get('invoicer', {}) # Inside the invoicer container
    invoicer_email = invoicer.get('email_address')
    items = data.get('items', [])
    for index, item in enumerate(items):
        item_name = item.get('name')
        item_description = item.get('description')
        item_quantity = item.get('quantity')
        item_unit_amount = item.get('unit_amount', {}).get('value')
        item_tax = item.get('tax', {}).get('amount', {}).get('value')
        item_discount = item.get('discount', {}).get('amount', {}).get('value')

        # Generate a unique project number for each item
        project_number = Utilites.generate_project_number(int(invoice_number), index)
        
        ProjectDetails: {
            "Status": status,
            "Invoice Number": project_number,
            "Reference Number": reference,
            "Email Address": invoicer_email,
            "Items": [item_name, item_description, item_unit_amount],
        }

        Invoice.saveInvoice(data=ProjectDetails)
        
print(paypal_webhook_url)
        
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        print("Shutting down ngrok...")
        ngrok.kill()
