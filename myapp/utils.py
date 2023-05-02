import json
from . models import *
import http.client

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        
    print('Cart:', cart)
    items = []
    order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'shipping': False,
            }
    cartItems = order['get_cart_items']

        
    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            
            product = Product.objects.get(pk=i)
            total = (product.price * cart[i]['quantity'])
            
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
                
            item = {
                'product':{
                    'id': product.pk,
                    'name': product.name,                        
                    'price': product.price, 
                    'imageURL': product.imageURL,                        
                    },                    
                'quantity': cart[i]['quantity'],                    
                'get_total': total                    
                }                
            items.append(item)
                    
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    # first check if user is authenticated or logged in
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
    print("User is not logged in...")

    print("COOKIES: ", request.COOKIES)
    name = data ['form']['name']
    email = data ['form']['email']
        
    cookieData = cookieCart(request)
    items = cookieData['items']
    
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()
        
    order = Order.objects.create(
            customer=customer,
            complete=False,
            )
        
    for item in items:
        product = Product.objects.get(pk=item['product']['id'])
            
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
            )
        orderItem.save()  
        print("Order Item saved")
        print("Returning Customer and Order from the guestOrder utils function")
    return customer, order

# Brands Page

# function for returning 'Akiba Studio'
# from the description of the product
def search_items(data):
    result = []
    for item in data:
        if 'Akiba Studio' in item:
        # if 'Trucker Hat' in item or 'Akiba Studio' in item:
            result.append(item)
    return result

# End of Brands Page
