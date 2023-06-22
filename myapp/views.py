from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
# Registration form import from the forms.py file
from .forms import OrderForm, RegisterUserForm, PhotoForm
from . utils import cookieCart, cartData, guestOrder, search_items
import http.client
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import random
import http.client


# ERROR - DONE


def error(request):
    print("Error 404")

    retry_link = ""
    error_message = ""

    context = {
        'retry_link': retry_link,
        'error_message': error_message,
    }

    return render(request, 'error.html', context)
# END OF ERROR - DONE

# ABOUT US


def about_us(request):
    page_name = f"| About Us"

    data = cartData(request)
    cartItems = data['cartItems']

    summary = AboutUs.objects.all()

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
        return redirect('about_us')

    context = {
        'summary': summary,
        'page_name': page_name,
        'cartItems': cartItems,
    }

    return render(request, 'about_us.html', context)
# END OF ABOUT US

# HELP SECTION - DONE


def help(request):
    page_name = f" | Help"

    data = cartData(request)
    cartItems = data['cartItems']

    help = Help.objects.first()
    context = {
        'help': help,
        'page_name': page_name,
        'cartItems': cartItems,
    }
    return render(request, 'help.html', context)
# END OF HELP SECTION - DONE


def index(request):
    page_name = "| Online Clothing Store | Affordable and Stylish Clothes from Kenya"

    photos = Photo.objects.all()
    blogs = Blog.objects.all()
    homepages = HomePage.objects.all()
    categories = Category.objects.all()

    hat_category_icon = categories[6].icon

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

    data = cartData(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        email = request.POST.get('email', '')
        newsletter_subscriber = Newsletter(email=email)
        newsletter_subscriber.save()
        print(f"{email} subscribed to our newsletter from the homepage!")
        return redirect('index')

    context = {
        'photos': photos,
        'blogs': blogs,
        'cartItems': cartItems,
        'page_name': page_name,
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
        'hat_category_icon': hat_category_icon,
    }
    return render(request, 'index.html', context)


def contact_us(request):
    page_name = f"| Contact Us"

    context = {'page_name': page_name}
    return render(request, 'contact_us.html', context)


def store(request):
    page_name = f"| Shop"

    data = cartData(request)
    cartItems = data['cartItems']

    blogs = Blog.objects.order_by('-pk')
    photos = Photo.objects.order_by('-pk')

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'page_name': page_name,
        'cartItems': cartItems,
        'blogs': blogs,
        'photos': photos,
    }

    return render(request, 'store.html', context)


def brand(request):
    page_name = f"| Brands"

    list_of_brand_products = Photo.objects.filter(brand=brand)
    list_of_brand_blogs = Blog.objects.filter(brand=brand)

    data = cartData(request)
    cartItems = data['cartItems']

    recent_products = Photo.objects.order_by('-pk')
    recent_blogs = Blog.objects.order_by('-pk')
    photos = Photo.objects.all()

    context = {
        'photos': photos,
        'page_name': page_name,
        'cartItems': cartItems,
        'recent_products': recent_products,
        'recent_blogs': recent_blogs,
        'list_of_brand_products': list_of_brand_products,
        'list_of_brand_blogs': list_of_brand_blogs,
    }
    return render(request, 'brand.html', context)
# CART


def cart(request):
    page_name = f"| Cart"

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    photos = Photo.objects.all()

    context = {
        'page_name': page_name,
        'items': items,
        'cartItems': cartItems,
        'order': order,
        'photos': photos,
    }

    return render(request, 'cart.html', context)

# END OF CART

# CHECKOUT


def checkout(request):

    page_name = f"| Checkout"

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'page_name': page_name,
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'checkout.html', context)

# END OF CHECKOUT


# PRODUCT DETAIL

def product_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    price_range = Photo.objects.filter(
        price__lte=photo.price + 25).exclude(pk=pk)

    rating = 0

    keywords = photo.keywords.split(',')
    similar_products = Photo.objects.filter(
        Q(keywords__icontains=keywords[0]) |
        Q(description__icontains=keywords[0]) |
        Q(name__icontains=keywords[0]) |
        Q(shop__icontains=keywords[0]) |
        Q(brand__icontains=keywords[0])
    ).exclude(pk=pk).distinct()

    page_name = f"| {photo.name}"

    data = cartData(request)
    cartItems = data['cartItems']
    shop = photo.shop

    colors = photo.colors.split(',')
    sizes = photo.sizes.split(',')

    context = {
        'photo': photo,
        'page_name': page_name,
        'shop': shop,
        'colors': colors,
        'cartItems': cartItems,
        'sizes': sizes,
        'keywords': keywords,
        'similar_products': similar_products,
        'price_range': price_range,
    }

    return render(request, 'product_detail.html', context)
# END OF PRODUCT DETAIL METHOD


def blog_list(request):
    blogs = Blog.objects.all()
    recent_blogs = Blog.objects.order_by('-pk')
    page_name = f"| Blogs"

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
        'blogs': blogs,
        'page_name': page_name,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'blog_list.html', context)


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    page_name = f"| {blog.title}"

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'blog': blog,
        'page_name': page_name,
        'cartItems': cartItems
    }
    return render(request, 'blog_detail.html', context)


def signup(request):
    page_name = f"| Log In/Sign Up"

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
        'page_name': page_name,
    }
    return render(request, 'signup.html', context)


@login_required(login_url='login')
def wishlist(request):
    photos = Photo.objects.all()
    page_name = f"| My Wishlist"

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'photos': photos,
        'page_name': page_name,
        'cartItems': cartItems,
    }
    return render(request, 'wishlist.html', context)
# END OF WISHLIST

# BRAND


def brands(request):
    page_name = f"| Brands"

    photos = Photo.objects.all()
    blogs = Blog.objects.all()

    brands_list = set(Photo.objects.values_list('shop', flat=True))
    categories = set(Photo.objects.values_list(
        'description', flat=True))  # add more categories as needed
    keywords = categories

    # print(keywords)
    # data = {'KINYOZI Salon Street', 'OX Sheep bucket', 'Red stylish bucket hat by akiba studios', 'Stylish bucket hat', 'Cool vibes, Akiba Studio with a new Tropical, Hawaii theme', 'Black pants with RED AK embroidery', 'Blue Top, Ladies', 'White trucker hat from Akiba Studios', 'Farm boyz blue shirt', 'Stay cozy with our “World Wide Web” knit pullover Featuring our “spider web” embroidery', 'Stylish akiba asorted hats', 'Black Akiba Pants with AK embroidery', 'NFT wallpaper playing playstation', 'Akiba front side trucker hat', 'Yellow stylish bucket hat for summer with cartoon embroidery on front side.', 'Introducing our latest print Kintsungi graphic print and a scattered poem inspired by the Kintsungi philosophy', 'Black half jacket by Akiba Studios, Street Fashion', 'FARM BOYZ 1 - Pink Blue Jersey', 'Black pants with ORANGE AK embroidery', 'Green lukustore.nl limiteed edition of the bucket hat', 'Blue Akiba Studios Bucket Hat for summer'}
    akiba_studios_products = search_items(keywords)
    # Products from akiba studios printed on the terminal

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'brands_list': brands_list,
        'page_name': page_name,
        'cartItems': cartItems,
        'categories': categories,
        'keywords': keywords,
        'akiba_studios_products': akiba_studios_products,
        'blogs': blogs,
        'photos': photos,
    }
    return render(request, 'brands.html', context)
# END OF BRAND


def newsletter(request):
    page_name = f" | Newsletter Subscription"

    data = cartData(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        email = request.POST.get('email', '')
        newsletter_subscriber = Customer.objects.filter(email=email).first()
        if newsletter_subscriber:
            return redirect('/')
        else:
            # Subscribe the email to the newsletter
            print(f"{email} Subscribed to our newsletter!")
            newsletter_subscriber = Newsletter(email=email)
            newsletter_subscriber.save()
        return redirect('/')

    context = {
        'page_name': page_name,
        'cartItems': cartItems,
    }

    return render(request, 'newsletter.html', context)

# cart update item view


def updateItem(request):
    data = json.loads(request.body)
    photoId = data['photoId']
    action = data['action']

    print(f'{action}ed the product {photoId}')

    customer = request.user.customer
    photo = Photo.objects.get(pk=photoId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, photo=photo)

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
    return JsonResponse('Payment Complete', safe=False)


def loginPage(request):

    page_name = f" | Log In"

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
                    return redirect('dashboard')
                else:
                    return redirect('register')
            else:
                messages.info(request, 'Username Or Password is incorrect')

    context = {
        'page_name': page_name,
        'cartItems': cartItems,
    }

    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):

    page_name = f" | Sign Up"

    form = RegisterUserForm()

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
        'page_name': page_name,
        'cartItems': cartItems,
        'form': form,
    }

    return render(request, 'register.html', context)
# customer


def confirmed(request):
    page_name = f"| Order Complete!"

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'page_name': page_name,
        'cartItems': cartItems,
    }

    return render(request, 'confirmed.html', context)


@login_required(login_url='login')
def add(request):
    page_name = '| New Luku!'

    photos = Photo.objects.order_by('-pk')
    total_products = Photo.objects.count()

    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        name = request.POST.get('name')

        if data['category'] != 'none':
            category = Category.objects.get(pk=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                name=data['category_name'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
                name=data['name'],
                keywords=data['keywords'],
                shop=data['shop'],
                size=data['size'],
                price=data['price'],
                type=data['type'],
                rating=data['rating'],
                color=data['color'],
            )
        messages.success(request, ('Succesfully added new product!'))
        return redirect('gallery')

    context = {
        'categories': categories,
        'page_name': page_name,
        'photos': photos,
        'total_products': total_products,

    }
    return render(request, 'add.html', context)


@login_required(login_url='login')
def delete(request, pk):
    photo = get_object_or_404(Photo, id=pk)

    if request.method == 'POST':
        photo.delete()
        return redirect('dashboard')
    return render(request, 'delete.html', {'photo': photo})

# Trials ===========================


def gallery(request):
    category = request.GET.get('category')

    data = cartData(request)
    cartItems = data['cartItems']

    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)

    categories = Category.objects.all()

    context = {
        'categories': categories,
        'photos': photos,
        'cartItems': cartItems,
    }
    return render(request, 'gallery.html', context)


def viewPhoto(request, pk):
    photo = Photo.objects.get(pk=pk)
    data = cartData(request)
    cartItems = data['cartItems']

    name_link = photo.name_link.split(',')

    similar_images = Photo.objects.filter(
        Q(name_link__icontains=name_link[0]) |
        Q(name__icontains=name_link[0])
    ).exclude(pk=pk).distinct()

    similar_products = photo.similar_products.split(',')

    similar_products = Photo.objects.filter(
        Q(similar_products__icontains=similar_products[0]) |
        Q(name__icontains=similar_products[0])
    ).exclude(pk=pk).distinct()

    context = {
        'photo': photo,
        'cartItems': cartItems,
        'similar_images': similar_images,
        'similar_products': similar_products
    }

    return render(request, 'photo.html', context)


@login_required(login_url='login')
def addPhoto(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        name = request.POST.get('name')

        if data['category'] != 'none':
            category = Category.objects.get(pk=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                name=data['category_name'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
                name=name,
            )

        return redirect('gallery')

    context = {
        'categories': categories,
    }
    return render(request, 'addphoto.html', context)


# DASHBOARD
@login_required(login_url='login')
def dashboard(request):
    photos = Photo.objects.all()
    categories = Category.objects.all()
    newsletters = Newsletter.objects.all()
    shippings = ShippingAddress.objects.all()
    orders = Order.objects.order_by('-pk')
    order_lists = OrderItem.objects.all()
    page_name = f" | Dashboard"

    blogs = Blog.objects.all()
    username = User.objects.all()
    customers = Customer.objects.all()
    helps = Help.objects.all()
    order_item_list = OrderItem.objects.all()
    about_us = AboutUs.objects.all()

    data = cartData(request)
    cartItems = data['cartItems']

    total_products = Photo.objects.count()

    category_list = [category.name for category in categories]
    category_json = json.dumps(category_list)

    popular_list = [photo.popular for photo in photos]
    popular_number = popular_list.count(True)

    regular_products = total_products - popular_number

    context = {
        'blogs': blogs,
        'customers': customers,
        'helps': helps,
        'order_item_list': order_item_list,
        'about_us': about_us,
        'total_products': total_products,
        'shippings': shippings,
        'cartItems': cartItems,
        'page_name': page_name,
        'photos': photos,
        'categories': categories,
        'orders': orders,
        'newsletters': newsletters,
        'order_lists': order_lists,
        'category_json': category_json,
        'popular_number': popular_number,
        'regular_products': regular_products,
    }

    return render(request, 'dashboard.html', context)
# END OF DASHBOARD


@login_required(login_url='login')
def update(request, pk):

    print("Debugging Update view...")
    print("Getting photo object using the Primary key")
    photo = Photo.objects.get(pk=pk)
    print("Getting a few methods from the request and using the Photo as an instance")
    form = PhotoForm(request.POST or None, instance=photo)
    print("Page name variable")
    page_name = f"| Edit"

    print("If condition starts here")
    if form.is_valid():
        print("Form is saved")
        form.save()
        print("Redirecting to dashboard")
        return redirect('dashboard')

    print("Context dictionary starts here")
    context = {
        'page_name': page_name,
        'form': form,
        'photo': photo,
    }
    print("Returning a copy of edit html with the context")

    return render(request, 'edit.html', context)


def music(request):
    page_name = "| DJ G400 Mixes"

    mix_albums = MixAlbum.objects.all()
    mixes = Mix.objects.all()
    playlists = ['Hip Hop', 'RnB', 'Trap', 'Afrobeats', 'Dancehall']

    context = {
        'page_name': page_name,
        'mixes': mixes,
        'mix_albums': mix_albums,
        'playlists': playlists,
    }
    return render(request, 'music.html', context)


def music_player(request, id):

    mix = Mix.objects.get(pk=id)
    mix_albums = MixAlbum.objects.all()
    mixes = Mix.objects.all()

    page_name = f"| Playing {mix.title}"

    context = {
        'page_name': page_name,
        'mix': mix,
        'mixes': mixes,
        'mix_albums': mix_albums,
    }
    return render(request, 'music_player.html', context)
