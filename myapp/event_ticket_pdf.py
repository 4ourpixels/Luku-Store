from fpdf import FPDF
import qrcode
from django.templatetags.static import static
from .models import LukuRadioSignup, SpectraTalksSignUp, Event
import os
from django.conf import settings
from datetime import datetime

event = Event.objects.latest('date')
qr_filename = ''


class PDF(FPDF):
    def set_ticket_number(self, ticket_number):
        self.ticket_number = ticket_number

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def header(self):
        # Adding QR code and poster images to the header
        self.image(qr_filename, 3, 10, 66)
        self.image(event.poster, 70, 0, 140)

        # Setting up font and displaying event details
        self.set_y(80)
        self.set_font('helvetica', "", 12)
        self.multi_cell(0, 10, f"{self.first_name} {self.last_name}", ln=True)
        self.set_font('helvetica', "B", 14)
        self.multi_cell(0, 10, self.ticket_number, ln=True)
        self.ln(4)
        self.set_font('helvetica', "B", 18)
        self.multi_cell(50, 7, str(event.name), ln=True)
        self.ln(4)

        # Additional event details
        self.set_font('helvetica', "", 10)
        self.set_text_color(80, 80, 80)
        self.multi_cell(
            50, 5, "This ticket admits one person. Minimum age of 21 years.", ln=True)
        self.ln(6)
        self.set_font('helvetica', "", 9)
        self.set_text_color(80, 80, 80)

        # Displaying event start, end, location, and address
        start_datetime = datetime.combine(
            event.date, event.start_time)
        end_datetime = datetime.combine(
            event.date, event.end_time)

        self.cell(10, 5, "Start:")
        self.set_x(30)
        self.cell(
            10, 5, start_datetime.strftime("%Y-%m-%d %I:%M %p"), ln=True)
        self.cell(10, 5, "End:")
        self.set_x(30)
        self.cell(
            10, 5, end_datetime.strftime("%Y-%m-%d %I:%M %p"), ln=True)
        self.cell(10, 5, "Location:")
        self.set_x(30)
        self.cell(10, 5, str(event.location), ln=True)
        self.cell(10, 5, "Venue:")
        self.set_x(30)
        self.cell(10, 5, str(event.venue), ln=True)
        self.ln(10)

        # Additional information about the event
        self.set_font('helvetica', "", 9)
        self.set_text_color(180, 180, 180)
        self.multi_cell(
            50, 5, "Your ID and ticket will be checked at the door.", ln=True)
        self.multi_cell(
            50, 5, "If your energy or ticket is not correct entrance will be denied.", ln=True)
        self.multi_cell(50, 5, "No ticket refunds, entrance on own risk.")

    def footer(self):
        # Adding disclaimer text from an external file and displaying page number
        self.set_y(-45)
        self.set_font("helvetica", "", 5)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 5, event.event_disclaimer, ln=True)
        self.set_font("helvetica", "", 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def generate_pdf_ticket(first_name, last_name, ticket_number, event_name, event_date):
    global qr_filename
    # Create a QR code with participant and event details
    qr_data = f"Name: {first_name} {last_name}\nTicket Number: {ticket_number}\nEvent: {event_name}\nDate: {event_date}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Specify the directory for saving the QR code image
    qr_directory = os.path.join(settings.BASE_DIR, 'qrcodes')

    # Create the directory if it doesn't exist
    os.makedirs(qr_directory, exist_ok=True)

    # Save the QR code image
    qr_filename = os.path.join(qr_directory, f'qr_{ticket_number}.png')

    img.save(qr_filename)

    # Creating PDF instance, setting properties, and generating the PDF
    pdf = PDF("P", "mm", "A4")
    pdf.set_first_name(first_name)
    pdf.set_last_name(last_name)
    pdf.set_ticket_number(ticket_number)
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.image(qr_filename, x=3, y=10, w=66)

    # Save the PDF content to a variable
    pdf_output = pdf.output()
    return pdf_output
