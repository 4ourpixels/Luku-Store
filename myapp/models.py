from django.db import models
from django.contrib.auth.models import User
from django.utils.dateformat import DateFormat
from django.utils import timezone


# BLOG ENTRY


class Blog(models.Model):
    title = models.CharField(max_length=50)
    summary = models.CharField(max_length=80)
    content = models.TextField()
    author = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="blog/",
        default='blog.jpg'
    )
    youtube = models.TextField(blank=True, null=True)
    BRAND = (
        ('Luku Store.nl', 'Luku Store.nl'),
        ('Akiba Studios', 'Akiba Studios'),
    )
    brand = models.CharField(
        max_length=15,
        choices=BRAND,
        null=True,
        blank=True,
        default='Luku Store.nl'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} || Published On: {self.pub_date.strftime('%A, %B %d, %Y')}"
# END OF BLOG ENTRY

# ABOUT US


class AboutUs(models.Model):
    summary = models.CharField(max_length=700, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=50, blank=True, null=True)
    twitter = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    image = models.ImageField(
        null=False,
        blank=False,
        upload_to="about-us/",
        default='image.jpg'
    )

    def __str__(self):
        return f"{self.name} || {self.role}"

# END OF ABOUT US

# HELP


class Help(models.Model):
    privacy_policy = models.TextField()
    terms_of_service = models.TextField()
    faqs = models.TextField()
    orders_n_delivery = models.TextField()
    return_n_refunds_policy = models.TextField()
    payment_methods = models.TextField()
# END OF HELP


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    icon = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    name_link = models.CharField(max_length=200, null=True, blank=True)
    similar_products = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    image = models.ImageField(
        null=False,
        blank=False,
        upload_to="products/",
        default='image.jpg'
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    color = models.CharField(max_length=75, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    rating = models.IntegerField(blank=True, default=0)
    popular = models.BooleanField(default=False, null=True, blank=False)
    SHOP = (
        ('Luku Store.nl', 'Luku Store.nl'),
        ('Akiba Studios', 'Akiba Studios'),
    )
    shop = models.CharField(
        max_length=50,
        choices=SHOP,
        null=True,
        default='Luku Store.nl'
    )
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        try:
            if self.name:
                return self.name
            else:
                return f"Type: {self.type}"
        except Exception as e:
            return f"Error retrieving string representation: {str(e)}"


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="media/",
        default='image.jpg',
    )

    def __str__(self):
        return self.name


def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            user=instance, name=instance.username, email=instance.email)


models.signals.post_save.connect(create_customer, sender=User)
# END OF CUSTOMER MODEL

# ORDER


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True, blank=False)

    def __str__(self):
        date_format = DateFormat(self.date_ordered.astimezone(
            timezone.get_current_timezone()))
        formatted_date = date_format.format('h:iA, l jS F Y')
        return f'Order #{self.pk} || {self.customer} || At: {formatted_date}'

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.photo.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.photo.digital == False:
                shipping = True
        return shipping
# END OF ORDER

# ORDER ITEM


class OrderItem(models.Model):
    photo = models.ForeignKey(
        Photo, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.photo.price * self.quantity
        return total

    def __str__(self):
        return f'{self.photo}'

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
# END OF ORDER ITEM

# SHIPPING ADDRESS


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.CharField(max_length=200, null=True)

    LABEL = (
        ('Home', 'Home'),
        ('Office', 'Office'),
        ('Default', 'Default'),
    )
    label = models.CharField(
        max_length=15, choices=LABEL, null=True, default='Home')

    def __str__(self):
        return self.address

    def __str__(self):
        return f"{self.customer}'s {self.label} Address"
# END OF SHIPPING ADDRESS


# NEWSLETTER


class Newsletter(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(default=" ")

    def __str__(self):
        return self.email

# END OF NEWSLETTER


class HomePage(models.Model):
    quote = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    quote_author = models.CharField(max_length=200, null=True, blank=True)

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="media/",
        default='image.jpg',
    )
    button = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class ContactForm(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class MixAlbum(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    genre = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="media/",
        default='image.jpg',
    )

    def __str__(self):
        return self.name


class Mix(models.Model):
    title = models.CharField(max_length=100)
    mix_artist = models.CharField(max_length=100)
    featured_artists = models.CharField(max_length=100)
    album = models.ForeignKey(
        MixAlbum,
        on_delete=models.SET_NULL,
        null=True
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="media/",
        default='image.jpg',
    )
    genre = models.CharField(max_length=50)
    duration = models.PositiveIntegerField()
    release_date = models.DateField()
    file = models.FileField(upload_to='mix/', blank=True, null=True)

    play_count = models.PositiveIntegerField(default=0)
    favorite_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    listen_count = models.PositiveIntegerField(default=0)

    youtube_link = models.TextField(blank=True, null=True)
    download_link = models.TextField(blank=True, null=True)
    stream_link = models.TextField(blank=True, null=True)
    hearthis_link = models.TextField(blank=True, null=True)
    apple_link = models.TextField(blank=True, null=True)
    mixcloud_link = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
