import pdf_maker
import printnode_connection
import DB
import logging


LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


files = dict()


def make_file_name(username):
    if username not in files:
        files[username] = [f'{username}-0']
    else:
        file_num = len(files[username])
        files[username].append(f'{username}-{file_num}')
    logging.info(f'file {files[username][-1]} created at orders directory')


def get_print_job(username, deliver_time, address, comments, client_name, api_key):
    make_file_name(username)
    order_name = files[username][-1]
    pdf_maker.make_order_pdf(order_name, deliver_time, address, comments, client_name)
    printers_id = DB.get_active_printers(api_key)
    for printer_id in printers_id:
        printnode_connection.make_print(api_key, order_name, printer_id)
        logging.info(f'print {order_name} send to printer {printer_id}')
