from django.core.mail import EmailMessage
import os
from django.conf import settings
from .models import Event
from .event_ticket_pdf import generate_pdf_ticket

event = Event.objects.latest('date')


def send_email_with_inline_logo(email, first_name, last_name, short_ticket_number, ticket_number, event_name, event_date):
    subject = event.confirmation_email_subject
    admin_message = event.confirmation_email_message
    message = f"Hi {first_name},\n\n{admin_message}\n\n\nYour Ticket: {ticket_number}\n\n\n\nLuku Store.nl\ninfo@lukustore.nl"
    from_email = settings.EMAIL_HOST_USER
    cc_email = settings.EMAIL_HOST_CC
    recipient_list = [email, cc_email]
    pdf_output = generate_pdf_ticket(
        first_name, last_name, ticket_number, event_name, event_date)

    email_message = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list,
    )
    generate_pdf_ticket(first_name, last_name,
                        ticket_number, event_name, event_date)
    email_message.attach(
        f'ticket_{short_ticket_number}.pdf', pdf_output, 'application/pdf')
    email_message.send()
