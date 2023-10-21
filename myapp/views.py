from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from .forms import *
from . utils import cartData, guestOrder
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# ABOUT US
def lukufam(request):
    page_name = f"- About Us"

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
        'page_name': page_name,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands
    }

    return render(request, 'lukufam.html', context)
# END OF ABOUT US

# HELP SECTION - DONE


def help(request):
    page_name = f"- Help"

    data = cartData(request)
    cartItems = data['cartItems']
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    help = Help.objects.first()
    context = {
        'help': help,
        'page_name': page_name,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'help.html', context)
# END OF HELP SECTION - DONE


def index(request):
    page_name = "- Home of African Streetwear | Online Clothing Store"

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
        'brands': brands,
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

    }
    return render(request, 'index.html', context)


def shop(request):
    page_name = f"- Shop"
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
        'page_name': page_name,
        'cartItems': cartItems,
        'latest_photo': latest_photo,
        'unique_photos': unique_photos,
        'categories': categories,
        'blogs': blogs,
        'brands': brands,
        'products': products,
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

        page_name = f"- {product.name}"

        context = {
            'product': product,
            'cartItems': cartItems,
            'photos': photos,
            'page_name': page_name,
            'blogs': blogs,
            'brands': brands,
            'similar_products': similar_products,
        }

        return render(request, 'product.html', context)
    except Product.DoesNotExist:
        page_name = f'- Error getitng {product.name}'
        print("Error: ", str(e))
        # Handle the case when the product doesn't exist
        # You can render a specific template or return an appropriate response
        context = {
            'error': str(e),
            'page_name': page_name
        }
        return render(request, '404.html', context)

    except Exception as e:
        # Handle other exceptions
        page_name = '- Error'
        print("Error :", str(e))
        context = {
            'error': str(e),
            'page_name': page_name
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

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    discount = 0
    page_name = f"- Cart({cartItems})"

    products = Product.objects.all()
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    context = {
        'page_name': page_name,
        'items': items,
        'cartItems': cartItems,
        'order': order,
        'products': products,
        'discount': discount,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'cart.html', context)

# END OF CART

# CHECKOUT


def checkout(request):
    page_name = f"- Checkout"
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'page_name': page_name,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'checkout.html', context)

# END OF CHECKOUT


def blog_list(request):
    page_name = f"- Blogs"
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
        'page_name': page_name,
    }
    return render(request, 'blog_list.html', context)


def blog_detail(request, slug):
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    blog = get_object_or_404(Blog, slug=slug)
    page_name = f"- {blog.title}"
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
        'page_name': page_name,
        'blogs': blogs,
        'cartItems': cartItems,
        'photos_in_ss23_category': photos_in_ss23_category,
        'keywords': keywords,
        'brands': brands,
    }
    return render(request, 'blog_detail.html', context)

# Brands Start


def brand_list(request):
    page_name = f"- Brands"
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
        'blogs': blogs,
        'page_name': page_name,
        'brands': brands,
    }
    return render(request, 'brand_list.html', context)


def newsletter(request):
    page_name = f"- Newsletter"
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
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
        'blogs': blogs,
        'brands': brands,
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


def loginPage(request):
    page_name = f"- Log In"
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
                    return redirect('index')
                else:
                    return redirect('register')
            else:
                messages.info(request, 'Username Or Password is incorrect')

    context = {
        'page_name': page_name,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    page_name = f"- Sign Up"
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
        'page_name': page_name,
        'cartItems': cartItems,
        'form': form,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'register.html', context)
# customer


def confirmed(request):
    page_name = f"- Order Complete!"
    data = cartData(request)
    cartItems = data['cartItems']
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    context = {
        'page_name': page_name,
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
    photo = Photo.objects.get(pk=pk)
    data = cartData(request)
    cartItems = data['cartItems']
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    name_link = photo.similar_products.split(',')

    similar_images = Photo.objects.filter(
        Q(name_link__icontains=name_link[0]) |
        Q(name__icontains=name_link[0])
    ).exclude(pk=pk).distinct()

    similar_products = photo.similar_products.split(',')

    similar_products = Photo.objects.filter(
        Q(similar_products__icontains=similar_products[0]) |
        Q(name__icontains=similar_products[0])
    ).exclude(pk=pk).distinct()

    page_name = f"- {photo.name}"

    context = {
        'photo': photo,
        'cartItems': cartItems,
        'similar_images': similar_images,
        'similar_products': similar_products,
        'page_name': page_name,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'photo.html', context)


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
        'products': products,
        'orders': orders,
        'order': order,
        'items': items,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'account.html', context)
# END OF ACCOUNT


def music(request):
    page_name = "- DJ G400 Mixes"
    mixes = Mix.objects.all()
    latest_mix = mixes[2]
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    context = {
        'page_name': page_name,
        'mixes': mixes,
        'latest_mix': latest_mix,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'music.html', context)


def music_player(request, id):
    mix = Mix.objects.get(pk=id)
    mixes = Mix.objects.all()
    page_name = f"- Playing {mix.title}"
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    context = {
        'page_name': page_name,
        'mix': mix,
        'mixes': mixes,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'music_player.html', context)


def dashboard(request):
    mixes = Mix.objects.order_by('-pk')
    blogs = Blog.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    products = Product.objects.order_by('-pk')
    photos = Photo.objects.order_by('-pk')
    help = Help.objects.order_by('-pk')
    categories = Category.objects.order_by('-pk')
    customers = Customer.objects.order_by('-pk')
    orders = Order.objects.order_by('-pk')
    order_items = OrderItem.objects.order_by('-pk')
    shipping_addresses = ShippingAddress.objects.order_by('-pk')
    newsletters = Newsletter.objects.order_by('-pk')
    homepages = HomePage.objects.order_by('-pk')

    page_name = "Dashboard"

    context = {
        'page_name': page_name,
        'mixes': mixes,
        'blogs': blogs,
        'brands': brands,
        'products': products,
        'photos': photos,
        'help': help,
        'categories': categories,
        'customers': customers,
        'orders': orders,
        'order_items': order_items,
        'shipping_addresses': shipping_addresses,
        'newsletters': newsletters,
        'homepages': homepages,
    }

    return render(request, 'dashboard.html', context)
