from printnodeapi import Gateway
import logging


LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# apikey2 = 'FEGj7XvW5hWAiU44d6qN7wxdNdrxNpO6WOxPZsvxsoU'


def make_print(api_key, order_name, printer_id):
    gateway = Gateway(url='https://api.printnode.com', apikey=api_key)
    gateway.PrintJob(printer=printer_id,
                     options={"copies": 1},
                     uri=f'http://127.0.0.1:5000/print_jobs/{order_name}')


def get_printers(api_key):
    gateway = Gateway(url='https://api.printnode.com', apikey=api_key)
    printers_list = []
    for printer in gateway.printers():
        printers_list.append((printer.id, printer.name, api_key))
    logging.info(f'got all printers from Printnode for the api key')
    return printers_list


