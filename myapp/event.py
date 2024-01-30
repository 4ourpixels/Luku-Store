from .forms import LukuRadioSignupForm
from .models import LukuRadioSignup, SpectraTalksSignUp
from django.contrib import messages
from django.shortcuts import render, redirect
from .email import send_email_with_inline_logo
import uuid
from django.core.exceptions import ObjectDoesNotExist


def event_signup(request):
    title_tag = "Luku Radio Vol 2 Kenyan Edition | MR. LU*"
    meta_description = "MR. LU* is a Kenyan producer, composer, deejay and artist who creates music that spans the sonic spectrum. Not one to be restricted by genre, this musical shapeshifter transcends the boundaries of bouncy hip-hop, cosmic trap and celestial R&B. Having worked with industry icons like Karun, Blinky Bill and Tai Tripper, @mistaalu future as the leader of Nairobi’s alternative soundscape is undeniable."
    meta_keywords = "MR. LU*, Kenyan producer, Composer, Deejay, Artist, Music, Sonic spectrum, Genre-spanning, Bouncy hip-hop, Cosmic trap, Celestial R&B, Musical shapeshifter, Boundaries, Industry icons, Karun, Blinky Bill, Tai Tripper, @mistaalu, Future leader, Nairobi, Alternative soundscape"
    event_signup_form = LukuRadioSignupForm()
    remaining_slots = 30 - LukuRadioSignup.objects.count()
    if request.method == 'POST':
        event_signup_form = LukuRadioSignupForm(request.POST)
        if event_signup_form.is_valid():
            email = event_signup_form.cleaned_data.get('email')
            try:
                spectra_signup = SpectraTalksSignUp.objects.get(email=email)
                messages.error(
                    request, ('Your email is already in our system. See you at Santuri. Doors open at 6pm.'))
                return redirect('index')
            except ObjectDoesNotExist:
                pass
            if LukuRadioSignup.objects.filter(email=email).exists():
                messages.error(
                    request, ('Successfylly registered'))
                return redirect('index')
            if remaining_slots > 0:
                user_signup = event_signup_form.save(commit=False)
                user_signup.consent = event_signup_form.cleaned_data.get(
                    'consent')
                user_signup.ticket_number = str(uuid.uuid4())[:6]
                user_signup.save()
                first_name = event_signup_form.cleaned_data.get(
                    'first_name')
                last_name = event_signup_form.cleaned_data.get(
                    'last_name')
                email = event_signup_form.cleaned_data.get('email')
                consent = user_signup.consent
                ticket_number = user_signup.ticket_number
                short_ticket_number = ticket_number[:8]
                consent = user_signup.consent
                if consent:
                    print("New subscriber!")
                    consent_status = "Subscribed"
                elif consent == "Unknown":
                    print("Consent Unknown")
                    consent_status = "Unknown"
                else:
                    consent_status = "Unsbscribed"
                    print(f"{first_name} Unsbscribed :(")

                print(
                    f"\n\n++++++SIGNUP DETAILS START+++++\n\nTicket Number: {ticket_number}\n{first_name} {last_name} registered with {email}\nSubscription status: {consent_status}\nShort Ticket No: #{short_ticket_number}\n\n++++++SIGNUP DETAILS END+++++\n\n")

                send_email_with_inline_logo(
                    email, first_name, short_ticket_number)

                messages.success(
                    request, (f"Hey {first_name}! Your Registration to 'Luku Radio Vol 2 Kenyan Edition' Was Successful! Check your email for the ticket and event details."))
                return redirect('index')
            else:
                event_signup_form.save()
                messages.error(
                    request, ("We appreciate your interest! As we've reached full capacity, keep an eye on our announcements for details on the next event. Stay connected through our newsletter or social channels to be the first to know."))
                return redirect('index')
        else:
            event_signup_form = LukuRadioSignupForm()

    context = {
        'title_tag': title_tag,
        'remaining_slots': remaining_slots,
        'event_signup_form': event_signup_form,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    }

    return render(request, 'events/event.html', context)
