import fpdf


def make_order_pdf(order_name, deliver_time, address, comments, client_name):
    pdf = fpdf.FPDF(format='letter')
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Order:", ln=1, align="L")
    time_line = f'Delivery time:   \t\t{deliver_time}'
    pdf.cell(200, 10, time_line, 0, 1, 'L')
    address_line  = f'Address:         \t\t\t\t{address}'
    pdf.cell(200, 10, address_line, 0, 2, 'L')
    comments_line = f'Comments:      \t\t\t{comments}'
    pdf.cell(200, 10, comments_line, 0, 3, 'L')
    client_name_line = f'Client name:    \t\t\t{client_name}'
    pdf.cell(200, 10, client_name_line, 0, 4, 'L')
    pdf.output(f"orders/{order_name}.pdf")


