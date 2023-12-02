from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(
        max_length=50)
    last_name = forms.CharField(
        max_length=50)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

        def __init__(self, *args, **kwagrs):
            super(RegisterUserForm, self).__init__(*args, **kwagrs)

            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['first_name'].widget.attrs['class'] = 'form-control'
            self.fields['last_name'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['class'] = 'form-control'


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("__all__")

        def __init__(self, *args, **kwagrs):
            super(PhotoForm, self).__init__(*args, **kwagrs)

            self.fields['name'].widget.attrs['class'] = 'form-control'
            self.fields['name_link'].widget.attrs['class'] = 'form-control'
            self.fields['type'].widget.attrs['class'] = 'form-control'
            self.fields['category'].widget.attrs['class'] = 'form-control'
            self.fields['image'].widget.attrs['class'] = 'form-control'
            self.fields['description'].widget.attrs['class'] = 'form-control'
            self.fields['similar_products'].widget.attrs['class'] = 'form-control'
            self.fields['price'].widget.attrs['class'] = 'form-control'
            self.fields['stock'].widget.attrs['class'] = 'form-control'
            self.fields['color'].widget.attrs['class'] = 'form-control'
            self.fields['size'].widget.attrs['class'] = 'form-control'
            self.fields['rating'].widget.attrs['class'] = 'form-control'
            self.fields['popular'].widget.attrs['class'] = 'form-check-input'
            self.fields['shop'].widget.attrs['class'] = 'form-check-input'
            self.fields['digital'].widget.attrs['class'] = 'form-check-input'


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ("__all__")

        def __init__(self, *args, **kwagrs):
            super(BlogForm, self).__init__(*args, **kwagrs)

            self.fields['title'].widget.attrs['class'] = 'form-control'
            self.fields['summary'].widget.attrs['class'] = 'form-control'
            self.fields['content'].widget.attrs['class'] = 'form-control'
            self.fields['author'].widget.attrs['class'] = 'form-control'
            self.fields['keywords'].widget.attrs['class'] = 'form-control'
            self.fields['image'].widget.attrs['class'] = 'form-control'
            self.fields['youtube'].widget.attrs['class'] = 'form-control'


class AmapianoSignUpForm(forms.ModelForm):
    class Meta:
        model = AmapianoSignUp
        fields = ("__all__")

        def __init__(self, *args, **kwagrs):
            super(AmapianoSignUpForm, self).__init__(*args, **kwagrs)

            self.fields['first_name'].widget.attrs['class'] = 'form-control'
            self.fields['last_name'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['class'] = 'form-control'
            self.fields['consent'].widget.attrs['class'] = 'form-check-input'


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ("__all__")

        def __init__(self, *args, **kwagrs):
            super(NewsletterForm, self).__init__(*args, **kwagrs)
            self.fields['customer'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['class'] = 'form-control'


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ("__all__")
        exclude = ['user']

        def __init__(self, *args, **kwagrs):
            super(CustomerForm, self).__init__(*args, **kwagrs)
            self.fields['user'].widget.attrs['class'] = 'form-control'
            self.fields['first_name'].widget.attrs['class'] = 'form-control'
            self.fields['last_name'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['class'] = 'form-control'
            self.fields['profile_pic'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['class'] = 'form-control'


class WatermarkColorForm(forms.Form):
    watermark_color = forms.ChoiceField(
        choices=[('white', 'White'), ('black', 'Black')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='white',
    )


# Stocks Form Start


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'
        exclude = ['product_code', 'slug']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'target': forms.Select(attrs={'class': 'form-control'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_f': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_t': forms.NumberInput(attrs={'class': 'form-control'}),
            'buying_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'possible_best_seller': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'online': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'priority': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'similar_products_codes': forms.TextInput(attrs={'class': 'form-control'}),
            'image_original_size': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_large_size': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_medium_size': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_thumbnail_size': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
# Stocks Form End
