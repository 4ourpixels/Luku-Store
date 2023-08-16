from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
# Registration form import from the forms.py file
from .forms import *
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
from django.db.models import F


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


def lukufam(request):
    page_name = f"- About Us"

    data = cartData(request)
    cartItems = data['cartItems']

    object = AboutUs.objects.all()

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
        'page_name': page_name,
        'cartItems': cartItems,
    }

    return render(request, 'lukufam.html', context)
# END OF ABOUT US

# HELP SECTION - DONE


def help(request):
    page_name = f"- Help"

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
    page_name = "- Home of African Streetwear | Online Clothing Store"

    photos = Photo.objects.all()
    blogs = Blog.objects.all()
    homepages = HomePage.objects.all()
    categories = Category.objects.all()
    mixes = Mix.objects.all()

    popular_items = Photo.objects.filter(popular=True)[:4]

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

    # Home page carousel slides
    slider_01 = homepages[11]
    slider_02 = homepages[12]
    slider_03 = homepages[13]

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
        'popular_items': popular_items,
        'mixes': mixes,

        'slider_01': slider_01,
        'slider_02': slider_02,
        'slider_03': slider_03,
    }
    return render(request, 'index.html', context)


def shop(request):
    page_name = f"- Shop"
    photos = Photo.objects.order_by('-pk')

    data = cartData(request)
    cartItems = data['cartItems']
    blogs = Blog.objects.order_by('-pk')
    category = request.GET.get('category')
    categories = Category.objects.all()

    total_products = Photo.objects.count()

    unique_product_codes = Photo.objects.filter(
        product_code__isnull=False).values_list('product_code', flat=True).distinct()
    unique_photos = []

    for product_code in unique_product_codes:
        latest_photo = Photo.objects.filter(
            product_code=product_code).order_by('-id').first()
        unique_photos.append(latest_photo)

    active_category = request.GET.get('category', None)

    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)

    context = {
        'page_name': page_name,
        'cartItems': cartItems,
        'blogs': blogs,
        'photos': photos,
        'categories': categories,
        'total_products': total_products,
        'unique_photos': unique_photos,
        'active_category': active_category,
    }

    return render(request, 'shop.html', context)

# CART


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    discount = 0
    page_name = f"- Cart({cartItems})"

    photos = Photo.objects.all()

    context = {
        'page_name': page_name,
        'items': items,
        'cartItems': cartItems,
        'order': order,
        'photos': photos,
        'discount': discount,
    }

    return render(request, 'cart.html', context)

# END OF CART

# CHECKOUT


def checkout(request):

    page_name = f"- Checkout"

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


def blog_list(request):
    blogs = Blog.objects.all()
    recent_blogs = Blog.objects.order_by('-pk')
    page_name = f"- Blogs"

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
    page_name = f"- {blog.title}"
    recent_blogs = Blog.objects.order_by('-pk')

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'blog': blog,
        'page_name': page_name,
        'recent_blogs': recent_blogs,
        'cartItems': cartItems,
    }
    return render(request, 'blog_detail.html', context)


def newsletter(request):
    page_name = f"- Newsletter"

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
    return JsonResponse('Payment Complete!', safe=False)


def loginPage(request):

    page_name = f"- Log In"

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
                    return redirect('account')
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

    page_name = f"- Sign Up"

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
    page_name = f"- Order Complete!"

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'page_name': page_name,
        'cartItems': cartItems,
        'success': True
    }

    return render(request, 'confirmed.html', context)


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

    unique_product_codes = Photo.objects.filter(
        product_code__isnull=False).values_list('product_code', flat=True).distinct()
    unique_photos = []

    for product_code in unique_product_codes:
        latest_photo = Photo.objects.filter(
            product_code=product_code).order_by('-id').first()
        unique_photos.append(latest_photo)

    active_category = request.GET.get('category', None)

    context = {
        'categories': categories,
        'photos': photos,
        'cartItems': cartItems,
        'active_category': active_category,
        'unique_photos': unique_photos,
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


# ACCOUNT
@login_required(login_url='login')
def account(request):
    photos = Photo.objects.all()

    shippings = ShippingAddress.objects.all()
    orders = Order.objects.order_by('-pk')

    order_item_list = OrderItem.objects.all()
    page_name = f"- Account"

    data = cartData(request)
    cartItems = data['cartItems']

    order = data['order']
    items = data['items']

    context = {
        'order_item_list': order_item_list,
        'shippings': shippings,
        'cartItems': cartItems,
        'page_name': page_name,
        'photos': photos,
        'orders': orders,
        'order': order,
        'items': items,
    }

    return render(request, 'account.html', context)
# END OF ACCOUNT


@login_required(login_url='login')
def edit(request, id):
    if request.method == "POST":
        photo = Photo.objects.get(pk=id)
        form = PhotoForm(request.POST, instance=photo)
        if form.is_valid():
            form.save()
            return render(request, 'edit.html', {
                'form': form,
                'success': True
            })
    else:
        photo = Photo.objects.get(pk=id)
        form = PhotoForm(instance=photo)
    return render(request, 'edit.html', {
        'form': form,
    })


def music(request):
    page_name = "- DJ G400 Mixes"

    mixes = Mix.objects.all()

    latest_mix = mixes[2]

    context = {
        'page_name': page_name,
        'mixes': mixes,
        'latest_mix': latest_mix,
    }
    return render(request, 'music.html', context)


def music_player(request, id):

    mix = Mix.objects.get(pk=id)
    mixes = Mix.objects.all()

    page_name = f"- Playing {mix.title}"

    context = {
        'page_name': page_name,
        'mix': mix,
        'mixes': mixes,
    }
    return render(request, 'music_player.html', context)


@login_required(login_url='login')
def add(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST)
        if form.is_valid():
            new_photo_name = form.cleaned_data['name']
            new_photo_name_link = form.cleaned_data['name_link']
            new_photo_category = form.cleaned_data['category']
            new_photo_image = form.cleaned_data['image']
            new_photo_description = form.cleaned_data['description']
            new_photo_similar_products = form.cleaned_data['similar_products']
            new_photo_price = form.cleaned_data['price']
            new_photo_stock = form.cleaned_data['stock']
            new_photo_color = form.cleaned_data['color']
            new_photo_size = form.cleaned_data['size']
            new_photo_rating = form.cleaned_data['rating']
            new_photo_popular = form.cleaned_data['popular']
            new_photo_shop = form.cleaned_data['shop']
            new_photo_digital = form.cleaned_data['digital']

            new_photo = Photo(
                name=new_photo_name,
                name_link=new_photo_name_link,
                category=new_photo_category,
                image=new_photo_image,
                description=new_photo_description,
                similar_products=new_photo_similar_products,
                price=new_photo_price,
                stock=new_photo_stock,
                color=new_photo_color,
                size=new_photo_size,
                rating=new_photo_rating,
                popular=new_photo_popular,
                shop=new_photo_shop,
                digital=new_photo_digital,
            )

            new_photo.save()

            return render(request, 'add.html', {
                'form': PhotoForm(),
                'success': True,
                'message': "New product was added successfully!",
            })
        else:
            form = PhotoForm()
    return render(request, 'add.html', {
        'form': PhotoForm()
    })


@login_required(login_url='login')
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            new_blog_title = form.cleaned_data['title']
            new_blog_summary = form.cleaned_data['summary']
            new_blog_content = form.cleaned_data['content']
            new_blog_author = form.cleaned_data['author']
            new_blog_keywords = form.cleaned_data['keywords']
            new_blog_image = form.cleaned_data['image']
            new_blog_youtube = form.cleaned_data['youtube']
            new_blog_brand = form.cleaned_data['brand']

            new_blog = Blog(
                title=new_blog_title,
                summary=new_blog_summary,
                content=new_blog_content,
                author=new_blog_author,
                keywords=new_blog_keywords,
                image=new_blog_image,
                youtube=new_blog_youtube,
                brand=new_blog_brand,
            )

            new_blog.save()

            return render(request, 'add_blog.html', {
                'form': BlogForm(),
                'success': True,
                'message': "New blog was added successfully!",
            })
        else:
            form = BlogForm()
    return render(request, 'add_blog.html', {
        'form': BlogForm()
    })


@login_required(login_url='login')
def edit_blog(request, id):
    if request.method == "POST":
        blog = Blog.objects.get(pk=id)
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return render(request, 'edit.html', {
                'form': form,
                'success': True
            })
    else:
        blog = Blog.objects.get(pk=id)
        form = BlogForm(instance=blog)
    return render(request, 'edit_blog.html', {
        'form': form,
    })
