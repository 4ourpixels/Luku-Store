from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from .email import send_email_with_inline_logo
from .utils import cartData
from django.contrib import messages
from django.db.models import Q
from blog.models import BlogPost
import uuid
from django.views.decorators.csrf import csrf_exempt
from .mollie_integration import create_payment
blogs = BlogPost.objects.filter(is_published=True).order_by('-pk')

# ABOUT US


def about(request):
    data = cartData(request)
    cartItems = data['cartItems']
    object = AboutUs.objects.all()
    brands = Brand.objects.order_by('-pk')
    kendy = object[0]
    djg400 = object[1]
    fkinyash = object[2]
    tarela = object[3]
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        message = request.POST.get('message')
        contact = ContactForm(
            name=name,
            email=email,
            message=message,
        )
        contact.save()
        return redirect('about')
    context = {
        'title_tag': "Luku Fam | About Us",
        'fkinyash': fkinyash,
        'kendy': kendy,
        'tarela': tarela,
        'djg400': djg400,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands
    }

    return render(request, 'about.html', context)
# END OF ABOUT US

# HELP SECTION - DONE


def help(request):
    data = cartData(request)
    cartItems = data['cartItems']
    brands = Brand.objects.order_by('-pk')
    help = Help.objects.first()
    context = {
        'title_tag': "Help",
        'help': help,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'help.html', context)
# END OF HELP SECTION - DONE


def index(request):
    title_tag = "Home of Afro Streetwear Culture | Online Clothing Store"
    meta_description = "Immerse yourself in the rich tapestry of Kenyan culture with Luku Store.nl. Explore our latest blogs, diverse brands, new collections, and visually stunning images. Shop unique, handmade fashion that tells a story. Join our community of socially-conscious shoppers and experience the vibrancy of Kenyan style here in Amsterdam."
    meta_keywords = "Kenyan Culture, Fashion Blog, Unique Brands, New Collections, Vibrant Images, Streetwear, Handmade Clothing, Socially-conscious Shopping, Afro, Luku Store.nl, Cultural Fashion, Fashion Community, Online Clothing Store, Netherlands, Amsterdam, Young Men, Young Women, Local Designers, Unique Outfits, Colorful, Independent Clothing Designers, Reasonable Price, Stories Behind Designers."
    photos = Photo.objects.all()
    brands = Brand.objects.order_by('-pk')
    homepages = HomePage.objects.all()
    categories = Category.objects.all()
    mixes = Mix.objects.order_by('-pk')[:4]

    popular_items = Photo.objects.filter(popular=True)[:4]

    slide1 = homepages[0]
    slide2 = homepages[1]
    slide3 = homepages[2]

    collection = homepages[3]
    definition = homepages[4]
    new_release = homepages[5]
    jacket = homepages[6]
    sweater = homepages[7]
    trucker_hats = homepages[8]
    asorted_trucker_hats = homepages[9]
    green_trucker_hat = homepages[10]

    # Home page carousel slides
    slider_01 = homepages[11]
    slider_02 = homepages[12]
    slider_03 = homepages[13]

    # Lukubook image
    lukubookImage = get_object_or_404(Photo, pk=51)

    # Luku Inspo Images
    red_bucket_hat = homepages[14]
    kintsugi_top_blue = homepages[15]
    utility_jacket = homepages[16]
    kintsugi_flare = homepages[17]

    # Footer
    trucker_hat = homepages[18]

    video = Video.objects.first()
    videos = Video.objects.all()
    home_video_2 = videos[1]
    home_video_3 = videos[2]

    data = cartData(request)
    cartItems = data['cartItems']

    # Calculate remaining slots
    event = Event.objects.latest('date')
    remaining_slots = event.remaining_slots
    bonkerz_nairobi_products = Product.objects.filter(online=True)[:3]
    bonkerz_nairobi = Brand.objects.get(slug="bonkerz-nrb")
    bonkerz_nairobi_logo = bonkerz_nairobi.image.url

    context = {
        'photos': photos,
        'blogs': blogs,
        'brands': brands,
        'cartItems': cartItems,
        'title_tag': title_tag,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'homepages': homepages,
        'slide1': slide1,
        'slide2': slide2,
        'slide3': slide3,
        'collection': collection,
        'definition': definition,
        'new_release': new_release,
        'jacket': jacket,
        'jacket': jacket,
        'trucker_hats': trucker_hats,
        'sweater': sweater,
        'asorted_trucker_hats': asorted_trucker_hats,
        'green_trucker_hat': green_trucker_hat,
        'categories': categories,
        'popular_items': popular_items,
        'mixes': mixes,
        'slider_01': slider_01,
        'slider_02': slider_02,
        'slider_03': slider_03,
        'lukubookImage': lukubookImage,
        'red_bucket_hat': red_bucket_hat,
        'kintsugi_top_blue': kintsugi_top_blue,
        'utility_jacket': utility_jacket,
        'kintsugi_flare': kintsugi_flare,
        'trucker_hat': trucker_hat,
        'video': video,
        'home_video_2': home_video_2,
        'home_video_3': home_video_3,
        'remaining_slots': remaining_slots,
        'bonkerz_nairobi_products': bonkerz_nairobi_products,
        'bonkerz_nairobi_logo': bonkerz_nairobi_logo,
        'event': event,

    }
    return render(request, 'index.html', context)


def shop(request):
    brand = request.GET.get('brand')
    title_tag = "Shop Unique Kenyan Fashion at Luku Store.nl | Accessible and Stylish Clothing"
    meta_description = "Explore our collection of vibrant and accessible Kenyan fashion at Luku Store.nl. From handcrafted pieces to curated designs, discover the latest trends for unisex, men and women. Make a statement with our socially-conscious clothing. Shipping within Netherlands."
    meta_keywords = "Kenyan Fashion, Accessible Clothing, Stylish Outfits, Online Fashion Store, Handmade Clothes, Curated Designs, Socially-conscious Shopping, Men's Fashion, Women's Fashion, Unisex, Luku Store.nl, Netherlands Fashion, Shipping."
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('pk')
    products = Product.objects.all()
    # products = product.objects.filter(online=True).order_by('-priority')

    unique_product_codes = Photo.objects.filter(
        product_code__isnull=False).values_list('product_code', flat=True).distinct()
    unique_photos = []

    for product_code in unique_product_codes:
        latest_photo = Photo.objects.filter(
            product_code=product_code).order_by('pk').first()
        unique_photos.append(latest_photo)

    categories = Category.objects.all()

    data = cartData(request)
    cartItems = data['cartItems']

    if brand is not None:
        products = Product.objects.filter(brand__name=brand, online=True)
    else:
        products = Product.objects.filter(online=True)

    sorted_brands = Brand.get_brands_sorted_by_online_product()
    active_brand = request.GET.get('brand', None)

    for product in products:
        if any([
            product.size_xs > 0,
            product.size_small > 0,
            product.size_medium > 0,
            product.size_large > 0,
            product.size_xl > 0,
            product.size_xxl > 0,
        ]):
            product.has_size = True
        else:
            product.has_size = False

    context = {
        'title_tag': title_tag,
        'cartItems': cartItems,
        'latest_photo': latest_photo,
        'unique_photos': unique_photos,
        'categories': categories,
        'blogs': blogs,
        'brands': brands,
        "meta_description": meta_description,
        'meta_keywords': meta_keywords,
        'products': products,
        'sorted_brands': sorted_brands,
        'active_brand': active_brand,
    }

    return render(request, 'shop.html', context)


# CART


def error404(request):
    context = {
        'title_tag': "Error 404",
    }
    return render(request, '404.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    title_tag = f"Cart({cartItems})"
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'title_tag': title_tag,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'checkout/cart.html', context)

# END OF CART

# CHECKOUT


def checkout(request):
    title_tag = "Checkout"
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    # data = cartData(request)
    # cartItems = data['cartItems']
    # order = data['order']
    # items = data['items']
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        order_amount = order.get_cart_total
        order_description = f"Order for {order.customer}"
        # initiate_payment(request, order_amount, order_description)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {
        'title_tag': title_tag,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'checkout/checkout.html', context)

# END OF CHECKOUT
# Brands Start


def brand_list(request):
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    data = cartData(request)
    cartItems = data['cartItems']
    context = {
        'title_tag': "Brands",
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'brands/brand-list.html', context)


def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    brand_products = Product.objects.filter(brand=brand).order_by('-priority')
    products = []
    for product in brand_products:
        if product.online:
            products.append(product)

    filtered_blogs = BlogPost.objects.filter(
        Q(tag__name__icontains=brand.name) |
        Q(category__name__icontains=brand.name) |
        Q(author__username__icontains=brand.name) |
        Q(content__icontains=brand.name) |
        Q(title__icontains=brand.name)
    ).distinct()

    data = cartData(request)
    cartItems = data['cartItems']
    context = {
        'title_tag': brand.name,
        'cartItems': cartItems,
        'filtered_blogs': filtered_blogs,
        'brands': brands,
        'brand': brand,
        'products': products,
        'blogs': blogs,
    }
    return render(request, 'brands/brand-detail.html', context)


def music(request):
    title_tag = "DJ G400 Mixes"
    mixes = Mix.objects.order_by("-pk")
    latest_mix = mixes[2]
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    context = {
        'title_tag': title_tag,
        'mixes': mixes,
        'latest_mix': latest_mix,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'music.html', context)


def music_player(request, slug):
    mix = Mix.objects.get(slug=slug)
    title_tag = f"Playing {mix.title}"
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    context = {
        'title_tag': title_tag,
        'mix': mix,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'music_player.html', context)


# Amapiano Workshop Signup Logic Start
def amapiano_workshop_signup(request):
    title_tag = "Amapiano Workshop Signup"
    form = AmapianoSignUpForm()
    remaining_slots = 20 - AmapianoSignUp.objects.count()

    if request.method == 'POST':
        form = AmapianoSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Check if the email already exists in the database
            if AmapianoSignUp.objects.filter(email=email).exists():
                messages.error(
                    request, ('This email is already registered. Please use a different email.'))
                return redirect('index')

            if remaining_slots > 0:
                user_signup = form.save(commit=False)
                user_signup.consent = form.cleaned_data.get('consent')
                user_signup.ticket_number = str(uuid.uuid4())[:8]
                user_signup.save()

                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                consent = user_signup.consent
                ticket_number = user_signup.ticket_number
                short_ticket_number = ticket_number[:8]

                print(
                    f"\n\n++++++SIGNUP DETAILS START+++++\n\nTicket Number: {ticket_number}\n{first_name} {last_name} registered with {email}\nConsent: {consent}\nShort Ticket No: #{short_ticket_number}\n\n++++++SIGNUP DETAILS END+++++\n\n")

                # Send email with inline logo
                send_email_with_inline_logo(
                    email, first_name, short_ticket_number)

                messages.success(
                    request, (f"Hey {first_name}! Your Amapiano Workshop Registration Was Successful! Check your email for the ticket and event details."))
                return redirect('index')
            else:
                form.save()
                messages.error(
                    request, ('Sorry, all slots have been filled.'))
                return redirect('index')
        else:
            form = AmapianoSignUpForm()

    context = {
        'title_tag': title_tag,
        'form': form,
        'remaining_slots': remaining_slots,
    }

    return render(request, 'events/amapiano.html', context)
# Amapiano Workshop Signup Logic End

# ACCOUNT


# spectra Talks Signup Logic Start


def spectra_talks_signup(request):
    title_tag = "spectra Talks with Luku Store.nl & WhoWhatWhereKE Signup"
    spectra_talks_signup_form = SpectraTalksSignUpForm()
    remaining_slots = 43 - SpectraTalksSignUp.objects.count()

    if request.method == 'POST':
        spectra_talks_signup_form = SpectraTalksSignUpForm(request.POST)
        if spectra_talks_signup_form.is_valid():
            email = spectra_talks_signup_form.cleaned_data.get('email')

            if SpectraTalksSignUp.objects.filter(email=email).exists():
                messages.error(
                    request, ('Successfylly registered'))
                return redirect('index')

            if remaining_slots > 0:
                user_signup = spectra_talks_signup_form.save(commit=False)
                user_signup.consent = spectra_talks_signup_form.cleaned_data.get(
                    'consent')
                user_signup.ticket_number = str(uuid.uuid4())[:8]
                user_signup.save()

                first_name = spectra_talks_signup_form.cleaned_data.get(
                    'first_name')
                last_name = spectra_talks_signup_form.cleaned_data.get(
                    'last_name')
                email = spectra_talks_signup_form.cleaned_data.get('email')
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
                    print(f"{first_name} Unsibscribed :(")

                print(
                    f"\n\n++++++SIGNUP DETAILS START+++++\n\nTicket Number: {ticket_number}\n{first_name} {last_name} registered with {email}\nSubscription status: {consent_status}\nShort Ticket No: #{short_ticket_number}\n\n++++++SIGNUP DETAILS END+++++\n\n")

                send_email_with_inline_logo(
                    email, first_name, short_ticket_number)

                messages.success(
                    request, (f"Hey {first_name}! Your Registration to 'spectra Talks with Luku Store.nl & WhoWhatWhereKE' Was Successful! Check your email for the ticket and event details."))
                return redirect('index')
            else:
                spectra_talks_signup_form.save()
                messages.error(
                    request, ("We appreciate your interest! As we've reached full capacity, keep an eye on our announcements for details on the next event. Stay connected through our newsletter or social channels to be the first to know."))
                return redirect('index')
        else:
            spectra_talks_signup_form = SpectraTalksSignUpForm()

    context = {
        'title_tag': title_tag,
        'remaining_slots': remaining_slots,
        'spectra_talks_signup_form': spectra_talks_signup_form,
    }

    return render(request, 'events/spectra-talks.html', context)
# spectra Talks Signup Logic End


def search_result(request):
    title_tag = f'"{request.GET.get("q")}" results'
    brands = Brand.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    context = {
        "title_tag": title_tag,
        "brands": brands,
        "blogs": blogs,
        "cartItems": cartItems,
    }
    return render(request, "search.html", context)


# Mollie Utility Start

def initiate_payment(request, order_amount, order_description):
    redirect_url = "confirmed"
    payment = create_payment(
        amount=order_amount, description=order_description, redirect_url=redirect_url)
    return render(request, 'payment.html', {'payment_url': payment.checkout_url})
# Mollie Utility End
