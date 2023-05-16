from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from . utils import cookieCart, cartData, guestOrder, search_items
import http.client
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q


# ERROR - DONE
def error(request):
    print("Error 404")
    
    retry_link = ""
    error_message = ""
    
    context = {'retry_link': retry_link,
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

    context = {'summary': summary, 
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
    context = {'help': help,
                'page_name': page_name,
                'cartItems': cartItems,
                }
    return render(request, 'help.html', context)
# END OF HELP SECTION - DONE


# DASHBOARD

def dashboard(request):
    products = Product.objects.all()
    blogs = Blog.objects.all()
    shipping_addresses = ShippingAddress.objects.all()
    
    total_products = Product.objects.count()
    total_blogs = Blog.objects.count()
    context = {
            'products': products, 
            'blogs': blogs,
            'total_products': total_products, 
            "total_blogs": total_blogs,
            'shipping_addresses': shipping_addresses,
            }
    return render(request, 'dashboard.html', context)
# END OF DASHBOARD

def index(request):
    
    page_name = "| Online Clothing Store | Affordable and Stylish Clothes from Kenya"
    products = Product.objects.all()
    blogs = Blog.objects.all()
    
    data = cartData(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        email = request.POST.get('email', '')
        newsletter_subscriber = Newsletter(email=email)
        newsletter_subscriber.save()
        print(f"{email} subscribed to our newsletter from the homepage!")
        return redirect('index')
    
    context = {'products': products, 
                'blogs': blogs, 
                'cartItems': cartItems,
                'page_name': page_name,
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
    
    recent_products = Product.objects.order_by('-pk')
    products = Product.objects.all()
    blogs = Blog.objects.order_by('-pk')
    
    items_per_page = 8
    paginator = Paginator(recent_products, items_per_page)
    
    context = { 
                'products': products, 
                'page_name': page_name,
                'cartItems': cartItems,
                'recent_products': recent_products,
                'paginator': paginator,
                'blogs': blogs,
                }
    
    return render(request, 'store.html', context)


def brand(request):
    page_name = f"| Brands"
    
    list_of_brand_products = Product.objects.filter(brand=brand)
    list_of_brand_blogs = Blog.objects.filter(brand=brand)

    data = cartData(request)
    cartItems = data['cartItems']

    recent_products = Product.objects.order_by('-pk')
    recent_blogs = Blog.objects.order_by('-pk')
    products = Product.objects.all()
    

    context = {'products': products, 
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
    
    products = Product.objects.all()

    context = {
                'page_name': page_name,
                'items': items,
                'cartItems': cartItems,
                'order': order,
                'products': products,
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
    product = get_object_or_404(Product, pk=pk)
    price_range = Product.objects.filter(price__lte=product.price + 25).exclude(pk=pk)
    
    keywords = product.keywords.split(',')
    similar_products = Product.objects.filter(
        Q(keywords__icontains=keywords[0]) |
        Q(description__icontains=keywords[0]) |
        Q(name__icontains=keywords[0]) |
        Q(shop__icontains=keywords[0]) |
        Q(brand__icontains=keywords[0])
    ).exclude(pk=pk).distinct()

    page_name = f"| {product.name}"
    
    data = cartData(request)
    cartItems = data['cartItems']
    shop = product.shop


    # Create a dynamic URL based on the first 5 words of the product name
    words = product.name.split()[:5]
    url_name = '-'.join(words)
    dynamic_url = f"/product/{pk}/{url_name}/"

    
    imgURL = product.imageURL

    colors = product.available_colors.split(',')
    sizes = product.sizes.split(',')
    
    context = {
            'product': product, 
            'page_name': page_name, 
            'dynamic_url': dynamic_url, 
            'shop':shop,
            'colors': colors,
            'cartItems': cartItems,
            'imgURL':imgURL,
            'sizes': sizes,
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

# WISHLIST
def wishlist(request):
    products = Product.objects.all()
    total_products = Product.objects.count()
    page_name = f"| Wishlist"
    
    data = cartData(request)
    cartItems = data['cartItems']
    
    
    context = {'products': products, 
                'total_products':total_products,
                'page_name': page_name,
                'cartItems': cartItems,
                }
    return render(request, 'wishlist.html', context)
# END OF WISHLIST

# BRAND
def brands(request):
    page_name = f"| Brands"
    
    products = Product.objects.all()
    blogs = Blog.objects.all()
    
    brands_list = set(Product.objects.values_list('shop', flat=True))
    categories = set(Product.objects.values_list('description', flat=True)) # add more categories as needed
    keywords = categories

    # print(keywords)
    # data = {'KINYOZI Salon Street', 'OX Sheep bucket', 'Red stylish bucket hat by akiba studios', 'Stylish bucket hat', 'Cool vibes, Akiba Studio with a new Tropical, Hawaii theme', 'Black pants with RED AK embroidery', 'Blue Top, Ladies', 'White trucker hat from Akiba Studios', 'Farm boyz blue shirt', 'Stay cozy with our “World Wide Web” knit pullover Featuring our “spider web” embroidery', 'Stylish akiba asorted hats', 'Black Akiba Pants with AK embroidery', 'NFT wallpaper playing playstation', 'Akiba front side trucker hat', 'Yellow stylish bucket hat for summer with cartoon embroidery on front side.', 'Introducing our latest print Kintsungi graphic print and a scattered poem inspired by the Kintsungi philosophy', 'Black half jacket by Akiba Studios, Street Fashion', 'FARM BOYZ 1 - Pink Blue Jersey', 'Black pants with ORANGE AK embroidery', 'Green lukustore.nl limiteed edition of the bucket hat', 'Blue Akiba Studios Bucket Hat for summer'}
    akiba_studios_products = search_items(keywords)
    # Products from akiba studios printed on the terminal


    
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'brands_list': brands_list, 
                'page_name': page_name,
                'cartItems': cartItems, 
                'categories': categories,
                'keywords': keywords,
                'akiba_studios_products': akiba_studios_products,
                'blogs': blogs,
                'products': products,
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
    productId = data['productId']
    action = data['action']
    
    print(f'The product {productId} was {action}ed')
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
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
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # if order.shipping == True:
        #     ShippingAddress.objects.create(
        #             customer=customer,
        #             order=order,
        #             address=data['shipping']['address'],
        #             city=data['shipping']['city'],
        #             state=data['shipping']['state'],
        #             zipcode=data['shipping']['zipcode'],
        #         )

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

    return JsonResponse('Payment Complete', safe=False)



# customer
def newCustomer(request):
    page_name = f" | Sign Up"
    
    data = cartData(request)
    cartItems = data['cartItems']
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        newCustomer = User.objects.filter(email=email).first()
        if newCustomer:
            return redirect('/')
        else:
            print(f"{username} New customer!")
            newCustomer = NewCustomer(
                    username=username,
                    email=email,
                    password=password,
                    )
            newCustomer.save()
        return redirect('/')
    
    context = {
                'page_name': page_name,
                'cartItems': cartItems,
                }
    
    return render(request, 'signup.html', context)
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

def addProduct(request):

    if request.method == 'POST':
        name = request.POST.get('name', '')
        shop = request.POST.get('shop', '')
        description = request.POST.get('description', '')
        keywords = request.POST.get('keywords', '')
        image = request.POST.get('image', '')
        price = request.POST.get('price', '')
        popular_true = request.POST.get('popular_true', '')
        popular_false = request.POST.get('popular_false', '')
        size = request.POST.get('size', '')

        product = Product(name=name,
                        shop=shop,
                        description=description,
                        keywords=keywords,
                        image=image,
                        price=price,
                        popular_false=popular_false,
                        popular_true=popular_true,
                        size=size,
                    )
        product.save()
        print(f"New Product Saved! {product.pk}, {product.name}")
    
    return render(request, 'add_product.html')

def delete(request, pk):
    if request.method == "POST":
        product = Product.objects.get(pk=pk)
        product.delete()
        return redirect("dashboard/")
    return render(request, 'delete.html')
