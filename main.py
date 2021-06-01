from flask import Blueprint, render_template, request, redirect, send_file
from auth import token_required
import DB
import to_print
import logging


LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@token_required
def profile(username):
    return render_template('profile.html', name=username)


@main.route('/printers')
@token_required
def printers(username):
    api_key = DB.get_api(username, True)
    printers_list = None
    no_api_key = False
    if api_key:
        printers_list = DB.get_printers(api_key[0])
    else:
        no_api_key = True
    return render_template('printers.html', name=username, printers_list=printers_list, no_api=no_api_key)


@main.route('/printers', methods=['POST'])
@token_required
def edit_printer(username):
    printer_id = request.form['printer_id']
    nickname = request.form['nickname']
    active = request.form['active']
    logging.info(printer_id, nickname, active)
    DB.update_printers(printer_id, nickname, active)
    return redirect('/printers')


@main.route('/orders')
@token_required
def orders(username):
    orders = DB.get_orders(username)
    return render_template('orders.html', name=username, orders=orders)


@main.route('/print_page', methods=['POST'])
@token_required
def print_page(username):
    time = request.form['time']
    name = request.form['name']
    address = request.form['address']
    comments = request.form['comment']
    api_key = DB.get_api(username, True)
    if api_key:
        to_print.get_print_job(username, time, address, comments, name, api_key[0])
        return redirect('/orders')


@main.route('/orders', methods=['POST'])
@token_required
def post_orders(username):
    time = request.form['delivery_time']
    name = request.form['name']
    address = request.form['address']
    comments = request.form['comments']
    DB.insert_order(time, name, address, comments, username)
    orders = DB.get_orders(username)
    return render_template('orders.html', name=username, orders=orders)


@main.route('/settings')
@token_required
def settings(username):
    api_keys = DB.get_api(username)
    no_api_key = None
    if not api_keys:
        no_api_key = True
    return render_template('settings.html', name=username, api_key=api_keys, no_api=no_api_key)


@main.route('/settings', methods=['POST'])
@token_required
def post_settings(username):
    api_key = request.form['api_key']
    if api_key:
        DB.insert_api_key(username, api_key)
    api_keys = DB.get_api(username)
    return render_template('settings.html', name=username, api_key=api_keys)


@main.route('/print_jobs/<file_name>')
def print_job(file_name):
    try:
        return send_file(f'orders/{file_name}.pdf')
    except:
        return '', 404
