from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from datetime import datetime
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'image'

conn = sqlite3.connect('database.db', check_same_thread=False)

product_list = [
    {
        'id': '1',
        'title': 'coca',
        'price': '0.5',
        'description': 'Some quick example text to build on the card title and make up the bulk of the cards content.',
        'image': 'product1.png',
    },
    {
        'id': '2',
        'title': 'Pepsi',
        'price': '0.5',
        'description': 'Some quick example text to build on the card title and make up the bulk of the cards content.',
        'image': 'product1.png',
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.get('/product')
def product():
    api_url = 'https://fakestoreapi.com/products'
    response = requests.get(api_url)
    if response.status_code == 200:
        product_list = response.json()
    else:
        product_list = []
    return render_template("product.html", product_list=product_list)


@app.get('/product_detail')
def product_detail():
    product_id = request.args.get('id')
    current_product = requests.get(f'https://fakestoreapi.com/products/{product_id}')
    current_product = current_product.json()
    return render_template('product_detail.html', current_product=current_product)


@app.get('/checkout')
def checkout():
    product_id = request.args.get('id')
    current_product = requests.get(f'https://fakestoreapi.com/products/{product_id}')
    current_product = current_product.json()
    return render_template('checkout.html', current_product=current_product)


TELEGRAM_BOT_TOKEN = '6866075986:AAEUC1yhzlZLA091oBXx2ZWjepsoG_GES1E'
TELEGRAM_CHAT_ID = '@Python_Channel_Bot'


def send_telegram_message(message):
    api_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    response = requests.post(api_url, data=data)
    return response


@app.route('/submit_order', methods=['POST'])
def submit_order():
    product_id = request.form.get('product_id')
    current_product = None

    if product_id:
        api_url = f'https://fakestoreapi.com/products/{product_id}'
        response = requests.get(api_url)

        if response.status_code == 200:
            current_product = response.json()
            product_name = current_product.get('title')  # Ensure correct key for product name
            price = current_product.get('price')
            product_image = current_product.get('image')  # Get the product image URL
        else:
            product_name = "Product Not Found"
            price = "N/A"
            video_file_path = "D:\Setec\Y3_S2\pp\dd.gif"

    name = request.form.get('fullname')
    phone = request.form.get('phone')
    email = request.form.get('email')

    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Create the message to send to Telegram
    message = (
        "*Order Successfully Placed☑✅️*\n\n"
        "*Product Details📄:*\n"
        "*Product:* {}\n"
        "*Price:* ${}\n\n"
        "+++++++++++++++++++++++++++\n\n"
        "*Customer Info🚺🚹:*\n"
        "*Name:* {}\n"
        "*Phone:* {}\n"
        "*Email:* {}\n\n"
        "*Order Time:* {}\n"
    ).format(product_name, price, name, phone, email, current_time)

    # Send the message to Telegram
    if product_image:
        send_telegram_photo_message(message, product_image)
    else:
        send_telegram_message(message)

    return render_template('submit_order.html', current_product=current_product, product_name=product_name, price=price,
                           name=name, phone=phone, email=email)


def send_telegram_photo_message(message, photo_url):
    api_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'photo': photo_url, 'caption': message, 'parse_mode': 'Markdown'}
    response = requests.post(api_url, data=data)
    return response


@app.get('/add_product')
def add_product():
    row = conn.execute("""SELECT * FROM product""")
    product = []
    for item in row:
        print(f"{item[0]}")
        product.append(
            {
                'id': item[0],
                'title': item[1],
                'cost': item[2],
                'price': item[3],
                'description': item[4],

            }
        )
    return render_template('add_product.html')


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/jingja')
def jingja():
    now = datetime.now()
    hour = 12.30
    return render_template("jingja.html", now=now, hour=hour)


@app.post('/submit_new_product')
def submit_new_product():
    product_id = request.form.get('title')
    file = request.form.get('file')
    title = request.form.get('title')
    price = request.form.get('price')
    catalog = request.form.get('catalog')
    description = request.form.get('description')
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/product', file.filename))

    return redirect(url_for('add_product'))


def is_even(value):
    return 'Yes' if value % 2 == 0 else 'No'


def is_odd(value):
    return 'Yes' if value % 2 != 0 else 'No'


if __name__ == '__main__':
    app.run(debug=True)
