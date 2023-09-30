import discord
import discord.ext
from flask import Flask, request, jsonify
import sqlite3
import json
from reference_number_converter import ReferenceNumberConverter as rnc
import requests
from main import createProjectDB as cpDB

app = Flask(__name__)

# SQLite database connection and cursor
conn = sqlite3.connect("data/invoices.db")
cursor = conn.cursor()

# Create a table to store webhook data
cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        invoice_id INTEGER PRIMARY KEY,
        email TEXT,
        discord_id INTEGER,
        invoice_amount REAL,
        desc TEXT,
        game TEXT,
        category TEXT,
        deadline TEXT,
        status TEXT
    )
""")
conn.commit()

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get PayPal webhook data
    data = json.loads(request.get_data(as_text=True))

    # Extract specific data from the invoice payload
    if 'resource' in data and data['resource_type'] == 'invoices':
        
        invoice_no = data['resource']['number']
    
    try: api(invoice=invoice_no) 
    except Exception as e: print("Failed to call upon API.")
    
    return jsonify({'status': 'success'})

def api(invoice):
    with open("config.json", "r") as f:
        config = json.load(f)
    
    headers = {
        'Authorization': f"Bearer {config['paypalapi']}",
        'Content-Type': 'application/json',
    }

    response = requests.get(f'https://api-m.sandbox.paypal.com/v2/invoicing/invoices/{invoice}', headers=headers)
    
    data = response.json()

    # Extracting data from the JSON response
    invoice_id = data.get('id')
    status = data.get('status')
    
    detail = data.get('detail', {})
    invoice_number = detail.get('invoice_number')
    reference = detail.get('reference')
    note = detail.get('note')
    
    invoicer = data.get('invoicer', {})
    invoicer_email = invoicer.get('email_address')
    
    amounts = data.get('due_amount', {})
    total = amounts.get('value')
     
    decodedReference = rnc.decode(reference)
    
    try:
        cursor.execute('''
            INSERT INTO invoices (invoice_id, email, discord_id, invoice_amount, desc, game, category, deadline, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (int(invoice_number), invoicer_email, decodedReference['Discord ID'], float(total), note, decodedReference['Game'], decodedReference['Service Type'], decodedReference['Deadline'], status))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving invoice to database: {e}")
    finally:
        discord(id=int(invoice_number))

def discord(invoiceID):
    cursor.execute('SELECT discord_id, invoice_amount, desc, game, category, deadline FROM invoices WHERE invoice_id = ?', (invoiceID,))
    project_data = cursor.fetchone()
    
    if project_data:
        discord_id, invoice_amount, desc, game, category, deadline = project_data
    
    if invoice_amount:
        developerPay = float(invoice_amount) * 0.4
        if developerPay:
            devPayReal = "${:,.2f}".format(developerPay)
    
    cpDB(ctx='ctx', project_details=desc, game=game, category=category, deadline=deadline, developer_payment=devPayReal, clientID=discord_id)
    
if __name__ == '__main__':
    app.run(debug=True)