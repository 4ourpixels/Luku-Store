from django.db import models
from django.contrib.auth.models import User
from django.utils.dateformat import DateFormat
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count
from django_resized import ResizedImageField
import uuid

# ABOUT US


class AboutUs(models.Model):
    summary = models.CharField(max_length=700, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.TextField(blank=True, null=True)
    twitter = models.TextField(blank=True, null=True)
    facebook = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="about-us/",
    )

    def __str__(self):
        return f"{self.name} | {self.role}"

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
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Type(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    product_code = models.TextField(null=True, blank=True)
    name_link = models.CharField(max_length=200, null=True, blank=True)
    similar_products_codes = models.CharField(max_length=300, blank=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    image = models.ImageField(
        null=False,
        blank=False,
        upload_to="products/",
        default='image.jpg'
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
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
    stock = models.IntegerField(default=0)

    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
    profile_pic = ResizedImageField(
        size=[500, 500], quality=100, upload_to="customers/", default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | {self.user.first_name}"


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
# END OF CUSTOMER MODEL


class Brand(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="brand/"
    )
    slug = models.SlugField(unique=True, null=True, blank=True)

    def total_products_products(self):
        return Product.objects.filter(brand=self).count()

    @classmethod
    def get_brands_sorted_by_online_product(cls):
        return cls.objects.filter(product__online=True).annotate(
            online_product_count=Count(
                'product', filter=models.Q(product__online=True))
        ).order_by('online_product_count')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def get_url(self):
        return reverse("brand_detail", kwargs={
            "slug": self.slug
        })


class Product(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    TARGET_CHOICES = [
        ("U", "U"),
        ("M", "M"),
        ("F", "F"),
    ]
    target = models.CharField(
        max_length=1, choices=TARGET_CHOICES, default="U", null=False, blank=True
    )
    item = models.CharField(max_length=200, null=True, blank=True)
    amount_f = models.IntegerField(default=0, blank=True, null=True)
    amount_t = models.IntegerField(default=0, blank=True, null=True)
    buying_price = models.IntegerField(default=0, blank=True, null=True)
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    total_cost = models.IntegerField(default=0, blank=True, null=True)
    POSSIBLE_BEST_SELLER_CHOICES = [
        (True, 'Best-Seller'),
        (False, 'Less-Seller'),
    ]
    possible_best_seller = models.BooleanField(
        default=True, choices=POSSIBLE_BEST_SELLER_CHOICES, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=150, null=True, blank=True)
    online = models.BooleanField(default=False, null=True, blank=True)
    priority = models.BooleanField(default=False, null=True, blank=True)
    product_code = models.CharField(max_length=10, null=True, blank=True)
    similar_products_codes = models.CharField(max_length=300, blank=True)
    description = models.TextField(null=True, blank=True)
    stock = models.IntegerField(default=0, null=True, blank=True)
    size_xs = models.IntegerField(default=0, null=True, blank=True)
    size_small = models.IntegerField(default=0, null=True, blank=True)
    size_medium = models.IntegerField(default=0, null=True, blank=True)
    size_large = models.IntegerField(default=0, null=True, blank=True)
    size_xl = models.IntegerField(default=0, null=True, blank=True)
    size_xxl = models.IntegerField(default=0, null=True, blank=True)
    rating = models.IntegerField(blank=True, default=0)
    digital = models.BooleanField(default=False, null=True, blank=True)
    img_md = models.ImageField(
        null=True,
        blank=True,
        upload_to="products/",
    )
    thumbnail = models.ImageField(
        null=True,
        blank=True,
        upload_to="products/",
    )
    slug = models.SlugField(unique=True, null=True, blank=True)

    def total_pieces(self):
        return Product.objects.aggregate(total_pieces=models.Sum('amount_f'))['total_pieces'] or 0

    def total_amount_T(self):
        return Product.objects.aggregate(total_amount_T=models.Sum('amount_t'))['total_amount_T'] or 0

    def total_consigment(self):
        return Product.objects.aggregate(total_consigment=models.Sum('buying_price'))['total_consigment'] or 0

    def grand_total_cost(self):
        return Product.objects.aggregate(grand_total_cost=models.Sum('total_cost'))['grand_total_cost'] or 0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.item)
        super().save(*args, **kwargs)

    @property
    def get_url(self):
        return reverse("view_product", kwargs={
            "slug": self.slug
        })

    def __str__(self):
        return f"{self.item} | ls0{self.pk}"


class ProductPhoto(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    product_code = models.TextField(null=True, blank=True)
    similar_products_codes = models.CharField(max_length=300, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True)

    image = models.ImageField(
        null=False,
        blank=False,
        upload_to="products/",
    )
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - #ls0{self.pk}"

    @property
    def get_url(self):
        return reverse("viewProductPhoto", kwargs={
            "pk": self.pk
        })


class ProductVideo(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    product_code = models.TextField(null=True, blank=True)
    similar_products_codes = models.CharField(max_length=300, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True)
    video = models.FileField(
        null=False,
        blank=False,
        upload_to="products/",
    )
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - #ls0{self.pk}"

    @property
    def get_url(self):
        return reverse("viewProductVideo", kwargs={
            "pk": self.pk
        })
# ORDER


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    paid = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        date_format = DateFormat(self.date_ordered.astimezone(
            timezone.get_current_timezone()))
        formatted_date = date_format.format('h:iA, l jS F Y')
        return f'#{self.pk} | {self.customer}  | At: {formatted_date}'

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
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
            if i.product.digital == False:
                shipping = True
        return shipping


@receiver(post_save, sender=Order)
def generate_transaction_id(sender, instance, created, **kwargs):
    if created and not instance.transaction_id:
        transaction_id = f"{instance.pk}-{int(timezone.now().timestamp())}-{uuid.uuid4().hex[:6]}"
        instance.transaction_id = transaction_id
        instance.save()

# END OF ORDER

# ORDER ITEM


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    size = models.TextField(null=True, blank=True)
    color = models.TextField(null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.selling_price * self.quantity
        return total

    def __str__(self):
        return f'{self.product}'

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

    def __str__(self):
        return f'{self.address} - Customer: {self.customer}'
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
        upload_to="media/"
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


class Mix(models.Model):
    title = models.CharField(max_length=100)
    mix_artist = models.CharField(max_length=100)
    featured_artists = models.TextField()
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="media/"
    )
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    file = models.FileField(upload_to='mix/', blank=True, null=True)

    play_count = models.PositiveIntegerField(default=0)
    favorite_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    stream_link = models.TextField(blank=True, null=True)

    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def get_url(self):
        return reverse("music_player", kwargs={
            "slug": self.slug
        })


class Video(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self):
        return self.title


class AmapianoSignUp(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    consent = models.BooleanField(default=True, null=True, blank=False)
    ticket_number = models.CharField(
        max_length=36, unique=True, blank=True, null=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SpectraTalksSignUp(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    consent = models.BooleanField(default=True, null=True, blank=False)
    ticket_number = models.CharField(
        max_length=36, unique=True, blank=True, null=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Spectra Talks With Luku Store.nl Signup'
        verbose_name_plural = 'Spectra Talks With Luku Store.nl Signups'


class LukuRadioSignup(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    consent = models.BooleanField(default=True, null=True, blank=False)
    ticket_number = models.CharField(
        max_length=36, unique=True, blank=True, null=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Luku Radio Vol 2 (Kenyan Edition) Signup'
        verbose_name_plural = 'Luku Radio Vol 2 (Kenyan Edition) Signups'


class EmailSignupMessage(models.Model):
    subject = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Email Signup Message'
        verbose_name_plural = 'Email Signup Messages'
