from .forms import EventParticipantForm
from .models import EventParticipant, SpectraTalksSignUp, Event
from django.contrib import messages
from django.shortcuts import render, redirect
from .email import send_email_with_inline_logo
import uuid
from django.core.exceptions import ObjectDoesNotExist


def event_signup(request):
    # Fetch the latest event
    event = Event.objects.latest('date')

    # Set metadata for the page
    title_tag = event.name
    meta_description = event.event_description
    meta_keywords = event.event_keywords

    # Initialize the form with or without POST data
    event_signup_form = EventParticipantForm(request.POST or None)

    # Calculate remaining slots
    remaining_slots = event.event_capacity - EventParticipant.objects.count()

    if request.method == 'POST':
        if event_signup_form.is_valid():
            # Assigning the event signup instance with a ticket number and the latest event
            user_signup = event_signup_form.save(commit=False)
            user_signup.event = event
            user_signup.ticket_number = str(uuid.uuid4())[:10]

            # Check if the email exists in a previous event
            email = event_signup_form.cleaned_data.get('email')
            try:
                spectra_signup = SpectraTalksSignUp.objects.get(email=email)
                messages.error(
                    request, f'Your email is already in our system. See you at {event.venue}. Doors open at {event.start_time}.')
                return redirect('index')
            except ObjectDoesNotExist:
                pass

            # Check if the email exists in the current event
            if EventParticipant.objects.filter(email=email).exists():
                messages.error(request, 'Successfully registered')
                return redirect('index')

            if remaining_slots > 0:
                # Additional processing for successful registration
                user_signup.consent = event_signup_form.cleaned_data.get(
                    'consent')
                user_signup.save()

                # Extract information for logging and email
                first_name = user_signup.first_name
                last_name = user_signup.last_name
                consent_status = "Subscribed" if user_signup.consent else "Unsubscribed"

                # Log signup details
                print(
                    f"\n\n++++++SIGNUP DETAILS START+++++\n\nTicket Number: {user_signup.ticket_number}\n{first_name} {last_name} registered with {email}\nSubscription status: {consent_status}\nShort Ticket No: #{user_signup.ticket_number[:4]}\n\n++++++SIGNUP DETAILS END+++++\n\n")

                # Send confirmation email
                send_email_with_inline_logo(
                    email, first_name, last_name, user_signup.ticket_number[:4], user_signup.ticket_number, event.name, event.date)

                # Display success message
                messages.success(
                    request, f"Hey {first_name}! Your Registration to '{event.name}' Was Successful! Check your email for the ticket and event details.")
                return redirect('index')
            else:
                # Handle case where event is at full capacity
                messages.error(request, "We appreciate your interest! As we've reached full capacity, keep an eye on our announcements for details on the next event. Stay connected through our newsletter or social channels to be the first to know.")
                return redirect('index')

    # Prepare context for rendering the template
    context = {
        'title_tag': title_tag,
        'remaining_slots': remaining_slots,
        'event_signup_form': event_signup_form,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'event': event,
    }

    # Render the template
    return render(request, 'events/event.html', context)
