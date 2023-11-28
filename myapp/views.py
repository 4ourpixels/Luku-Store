from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
import datetime
from .models import *
from .forms import *
from . utils import cartData, guestOrder
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Email Logic
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

# Amapiano Slots Logic
from django.db.models import Count
from django.http import JsonResponse
import uuid
import os

# History Logic Start
from django.contrib.admin.models import LogEntry
# History Logic End
# ABOUT US


def lukufam(request):
    title_tag = f"- About Us"

    data = cartData(request)
    cartItems = data['cartItems']

    object = AboutUs.objects.all()
    blogs = Blog.objects.order_by('-pk')
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
        return redirect('lukufam')

    context = {
        'kendy': kendy,
        'djg400': djg400,
        'fkinyash': fkinyash,
        'tarela': tarela,
        'title_tag': title_tag,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands
    }

    return render(request, 'lukufam.html', context)
# END OF ABOUT US

# HELP SECTION - DONE


def help(request):
    title_tag = f"- Help"

    data = cartData(request)
    cartItems = data['cartItems']
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    help = Help.objects.first()
    context = {
        'help': help,
        'title_tag': title_tag,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'help.html', context)
# END OF HELP SECTION - DONE


def index(request):
    title_tag = "- Home of Afro Streetwear Culture | Online Clothing Store"
    meta_description = "Immerse yourself in the rich tapestry of Kenyan culture with Luku Store.nl. Explore our latest blogs, diverse brands, new collections, and visually stunning images. Shop unique, handmade fashion that tells a story. Join our community of socially-conscious shoppers and experience the vibrancy of Kenyan style here in Amsterdam."
    meta_keywords = "Kenyan Culture, Fashion Blog, Unique Brands, New Collections, Vibrant Images, Streetwear, Handmade Clothing, Socially-conscious Shopping, Afro, Luku Store.nl, Cultural Fashion, Fashion Community, Online Clothing Store, Netherlands, Amsterdam, Young Men, Young Women, Local Designers, Unique Outfits, Colorful, Independent Clothing Designers, Reasonable Price, Stories Behind Designers."
    photos = Photo.objects.all()
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    homepages = HomePage.objects.all()
    categories = Category.objects.all()
    mixes = Mix.objects.all()

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
    remaining_slots = 20 - AmapianoSignUp.objects.count()

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

    }
    return render(request, 'index.html', context)


def shop(request):
    title_tag = f"- Shop Unique Kenyan Fashion at Luku Store.nl | Accessible and Stylish Clothing"
    meta_description = "Explore our collection of vibrant and accessible Kenyan fashion at Luku Store.nl. From handcrafted pieces to curated designs, discover the latest trends for unisex, men and women. Make a statement with our socially-conscious clothing. Shipping within Netherlands."
    meta_keywords = "Kenyan Fashion, Accessible Clothing, Stylish Outfits, Online Fashion Store, Handmade Clothes, Curated Designs, Socially-conscious Shopping, Men's Fashion, Women's Fashion, Unisex, Luku Store.nl, Netherlands Fashion, Shipping."
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    products = Product.objects.order_by('-pk')

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

    context = {
        'title_tag': title_tag,
        'cartItems': cartItems,
        'latest_photo': latest_photo,
        'unique_photos': unique_photos,
        'categories': categories,
        'blogs': blogs,
        'brands': brands,
        'products': products,
        "meta_description": meta_description,
        'meta_keywords': meta_keywords,
    }

    return render(request, 'shop.html', context)


def view_product(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
        photos = Photo.objects.filter(product_code=product.product_code)

        similar_products_codes = product.similar_products_codes.split(',')
        similar_products = Product.objects.filter(
            Q(product_code__in=similar_products_codes) | Q(
                name__in=similar_products_codes)
        )

        data = cartData(request)
        cartItems = data['cartItems']
        blogs = Blog.objects.order_by('-pk')
        brands = Brand.objects.order_by('-pk')

        title_tag = f"- {product.name}"

        context = {
            'product': product,
            'cartItems': cartItems,
            'photos': photos,
            'title_tag': title_tag,
            'blogs': blogs,
            'brands': brands,
            'similar_products': similar_products,
        }

        return render(request, 'product.html', context)
    except Product.DoesNotExist:
        # Handle the case when the product doesn't exist
        # You can render a specific template or return an appropriate response
        return render(request, 'product_not_found.html')

    except Exception as e:
        # Handle other exceptions
        title_tag = f'- Error {product.name} was not found'
        print("Error :", str(e))
        context = {
            'error': str(e),
            'title_tag': title_tag
        }
        return render(request, '404.html', context)
# CART


def error404(request):
    page = "- Error"

    context = {
        'page': page,
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

    title_tag = f"- Cart({cartItems})"
    blogs = Blog.objects.order_by('-pk')
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

    return render(request, 'cart.html', context)

# END OF CART

# CHECKOUT


def checkout(request):
    title_tag = f"- Checkout"
    blogs = Blog.objects.order_by('-pk')
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

    return render(request, 'checkout.html', context)

# END OF CHECKOUT


def blog_list(request):
    title_tag = f"- Blogs"
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
        'title_tag': title_tag,
    }
    return render(request, 'blog_list.html', context)


def blog_detail(request, slug):
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    blog = get_object_or_404(Blog, slug=slug)
    title_tag = f"- {blog.title}"
    meta_description = f"- {blog.title}"
    meta_keywords = f"- {blog.keywords}"
    keywords = [
        item.strip()
        for item in blog.keywords.split(',')
        if item.strip()
    ]

    data = cartData(request)
    cartItems = data['cartItems']

    # Retrieve photos from the category named "SS23"
    category_ss23 = Category.objects.get(name='SS23')
    photos_in_ss23_category = Photo.objects.filter(category=category_ss23)

    context = {
        'blog': blog,
        'title_tag': title_tag,
        'blogs': blogs,
        'cartItems': cartItems,
        'photos_in_ss23_category': photos_in_ss23_category,
        'keywords': keywords,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'brands': brands,
    }
    return render(request, 'blog_detail.html', context)

# Brands Start


def brand_list(request):
    title_tag = "- Brands"
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
        'blogs': blogs,
        'title_tag': title_tag,
        'brands': brands,
    }
    return render(request, 'brand_list.html', context)


def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.order_by('-pk')
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    title_tag = f"- {brand.name}"

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
        'blogs': blogs,
        'title_tag': title_tag,
        'brands': brands,
        'brand': brand,
        'products': products,
    }
    return render(request, 'brand_detail.html', context)


def newsletter(request):
    title_tag = "- Newsletter"
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    data = cartData(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data.get('email')
            if Newsletter.objects.filter(email=email).exists():
                messages.info(
                    request, "Hey superstar, you're already one of our favorites! Keep an eye on your inbox for more amazing content. You're officially ahead of the curve!")
            else:
                newsletter_form.save()
                print(f"{email} subscribed to our newsletter from the homepage!")
                messages.success(
                    request, "You just unlocked VIP access to our exclusive updates! Stay tuned for the hottest news and insider tips we've got lined up just for you.")
            # Get the referring page's URL
            referer = request.META.get('HTTP_REFERER')
            return redirect(referer or 'index')
    else:
        newsletter_form = NewsletterForm()

    context = {
        'title_tag': title_tag,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
        'newsletter_form': newsletter_form,
    }

    return render(request, 'newsletter.html', context)

# cart update item view


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(pk=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
# end of cart update item view


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        customer, order = guestOrder(request, data)

    total = data['form']['total']
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    messages.success(request, ("Payment Complete!"))
    return JsonResponse('Payment Complete!', safe=False)

# Trial cart update item view


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print(f'{action}ed the product {productId}')

    customer = request.user.customer
    product = Product.objects.get(product_code=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
# end of cart update item view


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    print("TRANSACTION ID: ==>> ", transaction_id)
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        customer, order = guestOrder(request, data)

    total = data['form']['total']
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    messages.success(request, ("Payment Complete!"))
    return JsonResponse('Payment Complete!', safe=False)


def loginPage(request):
    title_tag = f"- Log In"
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    data = cartData(request)
    cartItems = data['cartItems']

    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_staff:
                    messages.info(request, f'Welcome back {user.first_name}')
                    return redirect('index')
                else:
                    messages.info(
                        request, 'Register an account with us today.')
                    return redirect('register')
            else:
                messages.info(request, 'Username Or Password is incorrect')

    context = {
        'title_tag': title_tag,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    title_tag = f"- Create Your Luku Account - Sign Up for Exclusive Offers and Fashion Updates"
    meta_description = "Join the Lukustore.nl community! Sign up for an account to access exclusive offers, stay updated on the latest Kenyan fashion trends, and be part of our socially-conscious shopping experience. Register now for a personalized shopping journey that celebrates diversity and style."
    meta_keywords = "Luku Store.nl Signup, Account Registration, Exclusive Offers, Fashion Updates, Socially-conscious Shopping, Personalized Account, Kenyan Fashion, Streetwear, Community Membership, Stay Connected, Diverse Style."
    form = RegisterUserForm()
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    data = cartData(request)
    cartItems = data['cartItems']

    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, ('Registration Successful'))
                return redirect('index')
        else:
            form = RegisterUserForm()
    context = {
        'title_tag': title_tag,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'cartItems': cartItems,
        'form': form,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'register.html', context)
# customer


def confirmed(request):
    title_tag = f"- Order Complete!"
    data = cartData(request)
    cartItems = data['cartItems']
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    context = {
        'title_tag': title_tag,
        'cartItems': cartItems,
        'success': True,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'confirmed.html', context)


def gallery(request):
    category = request.GET.get('category')
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    data = cartData(request)
    cartItems = data['cartItems']

    if category == None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__name=category)

    categories = Category.objects.all()

    unique_product_codes = Product.objects.filter(
        product_code__isnull=False).values_list('product_code', flat=True).distinct()
    unique_photos = []

    for product_code in unique_product_codes:
        latest_photo = Product.objects.filter(
            product_code=product_code).order_by('-id').first()
        unique_photos.append(latest_photo)

    active_category = request.GET.get('category', None)

    context = {
        'categories': categories,
        'products': products,
        'cartItems': cartItems,
        'active_category': active_category,
        'unique_photos': unique_photos,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'gallery.html', context)


def viewPhoto(request, pk):
    try:
        photo = get_object_or_404(Photo, pk=pk)
        product = get_object_or_404(Product, product_code=photo.product_code)
        data = cartData(request)
        cartItems = data['cartItems']
        blogs = Blog.objects.order_by('-pk')
        brands = Brand.objects.order_by('-pk')
        photos = Photo.objects.filter(product_code=product.product_code)

        similar_products = Product.objects.filter(
            product_code=photo.product_code)

        similar_products_codes = photo.similar_products_codes.split(',')
        similar_products = Product.objects.filter(
            Q(product_code__in=similar_products_codes) | Q(
                name__in=similar_products_codes)
        )

        title_tag = f"- {photo.name}"

        context = {
            'photo': photo,
            'cartItems': cartItems,
            'similar_products': similar_products,
            'title_tag': title_tag,
            'blogs': blogs,
            'brands': brands,
            'product': product,
            'photos': photos,
        }

        return render(request, 'photo.html', context)

    except Exception as e:
        # Handle other exceptions
        title_tag = f'- Error {photo.name} was not found'
        print("Error :", str(e))
        context = {
            'error': str(e),
            'title_tag': title_tag
        }
        return render(request, '404.html', context)


# ACCOUNT
@login_required(login_url='login')
def account(request):
    photos = Photo.objects.all()
    products = Product.objects.all()
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    shippings = ShippingAddress.objects.all()
    orders = Order.objects.order_by('-pk')
    order_item_list = OrderItem.objects.all()
    # title Tag
    title_tag = f"Account Settings | Manage Your Luku Profile and Preferences"
    meta_description = "Customize your Lukustore.nl experience with our account settings. Update your profile, manage preferences, and stay connected with the latest Kenyan fashion. Shop consciously with Lukustore.nl."
    meta_keywords = "Lukustore, Account Settings, Profile Management, Preferences, Kenyan Fashion, Online Clothing Store, Socially-conscious Shopping, Vibrant Outfits, Handmade Clothes, Free Shipping Netherlands."
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'order_item_list': order_item_list,
        'shippings': shippings,
        'cartItems': cartItems,
        'title_tag': title_tag,
        'photos': photos,
        'products': products,
        'orders': orders,
        'order': order,
        'items': items,
        'blogs': blogs,
        'brands': brands,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,

    }

    return render(request, 'account.html', context)
# END OF ACCOUNT


def music(request):
    title_tag = "- DJ G400 Mixes"
    mixes = Mix.objects.all()
    latest_mix = mixes[2]
    blogs = Blog.objects.order_by('-pk')
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
    mixes = Mix.objects.all()
    title_tag = f"- Playing {mix.title}"
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    context = {
        'title_tag': title_tag,
        'mix': mix,
        'mixes': mixes,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'music_player.html', context)


@login_required(login_url='index')
def dashboard(request):
    stocks = Stock.objects.all()
    total_pieces = Stock.objects.first().total_pieces()
    total_consigment = Stock.objects.first().total_consigment()
    grand_total_cost = Stock.objects.first().grand_total_cost()
    total_amount_T = Stock.objects.first().total_amount_T()

    euro_exchange_rate = int(155)
    euro_converted_total_consigment = round(
        int(grand_total_cost) / euro_exchange_rate)

    title_tag = "Dashboard"
    admin_actions = LogEntry.objects.order_by('-action_time')[:10]

    context = {
        'title_tag': title_tag,
        'stocks': stocks,
        'total_pieces': total_pieces,
        'total_consigment': total_consigment,
        'grand_total_cost': grand_total_cost,
        'total_amount_T': total_amount_T,
        'euro_converted_total_consigment': euro_converted_total_consigment,
        'admin_actions': admin_actions,
    }

    return render(request, 'dashboard.html', context)


# Amapiano Workshop Signup Logic Start


def send_email_with_inline_logo(email, first_name, ticket_number):
    subject = 'Your Amapiano Workshop Confirmation 🎉'
    message = f"Hi {first_name},\n\nGreat news! You're officially registered for the Amapiano Workshop 🎶\n\n📅 Date: 18th Nov 2023\n🕒 Time: 3:00 PM - 5:00 PM\n📍 Venue: Amsterdam Dance Center\n\n\nYour Ticket: {ticket_number}\n\nGet ready for a fantastic time of music and dance!\nSee you there,\n\nLuku Store.nl\ninfo@lukustore.nl"

    from_email = 'lukustore.nl@gmail.com'
    lukustore_info_email = 'info@lukustore.nl'
    recipient_list = [email, lukustore_info_email]

    # Create an EmailMessage instance
    email_message = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list,
    )

    # Attach the logo inline
    logo_path = os.path.join(os.path.dirname(
        __file__), 'static/Amapiano-Workshop.jpg')
    with open(logo_path, 'rb') as logo_file:
        # Adjust content type if needed
        email_message.attach(logo_file.name, logo_file.read(), 'image/png')

    # Send the email
    email_message.send()


def amapiano_workshop_signup(request):
    title_tag = "- Amapiano Workshop Signup"
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

    return render(request, 'amapiano.html', context)
# Amapiano Workshop Signup Logic End

# ACCOUNT


@login_required(login_url='login')
def account_settings(request):
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    shippings = ShippingAddress.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # Edit account
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    title_tag = f"- Account Settings"
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            print(f"Succesfully updated {first_name}'s account.")
            messages.success(
                request, ('Succesfully updated account settings.'))
            return redirect('account_settings')
        else:
            form = CustomerForm(instance=customer)

    context = {
        'shippings': shippings,
        'cartItems': cartItems,
        'title_tag': title_tag,
        'blogs': blogs,
        'brands': brands,
        'form': form,
    }

    return render(request, 'account_settings.html', context)


# Stock Logic Start
def view_stock(request, slug):
    stock = Stock.objects.get(slug=slug)
    return HttpResponseRedirect(reverse('dashboard'))


def edit_stock(request, slug):
    stock = get_object_or_404(Stock, slug=slug)

    if request.method == 'POST':
        form = StockForm(request.POST, request.FILES, instance=stock)
        if form.is_valid():
            form.save()
            return render(request, 'edit_stock.html', {
                'form': form,
                'success': True
            })
        else:
            print("Errors occurred while uploading: ", form.errors)
    else:
        form = StockForm(instance=stock)

    return render(request, 'edit_stock.html', {
        'form': form,
    })


def delete_stock(request, slug):
    if request.method == 'POST':
        stock = Stock.objects.get(slug=slug)
        stock.delete()
    return HttpResponseRedirect(reverse('dashboard'))


def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            # new_title = form.cleaned_data['title']
            new_stock = Stock(
                # title=new_title,

            )

            new_stock.save()
            return render(request, 'add_stock.html', {
                'form': StockForm(),
                'success': True
            })
    else:
        form = StockForm()
    return render(request, 'add_stock.html', {
        'form': StockForm()
    })

# Stock Logic End
