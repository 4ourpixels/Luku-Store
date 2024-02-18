from django import forms
from .models import Order, AmapianoSignUp, Newsletter, Customer, Product, ProductPhoto, SpectraTalksSignUp, LukuRadioSignup, Event, EventParticipant
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

        def __init__(self, *args, **kwargs):
            super(RegisterUserForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['first_name'].widget.attrs['class'] = 'form-control'
            self.fields['last_name'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['class'] = 'form-control'


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

# Stocks Form Start


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['product_code', 'slug']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'target': forms.Select(attrs={'class': 'form-control'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
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
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'size_xs': forms.NumberInput(attrs={'class': 'form-control'}),
            'size_small': forms.NumberInput(attrs={'class': 'form-control'}),
            'size_medium': forms.NumberInput(attrs={'class': 'form-control'}),
            'size_large': forms.NumberInput(attrs={'class': 'form-control'}),
            'size_xl': forms.NumberInput(attrs={'class': 'form-control'}),
            'size_xxl': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Stocks Form End


class ProductPhotoForm(forms.ModelForm):
    class Meta:
        model = ProductPhoto
        fields = '__all__'


class SpectraTalksSignUpForm(forms.ModelForm):
    class Meta:
        model = SpectraTalksSignUp
        fields = ("__all__")

        def __init__(self, *args, **kwagrs):
            super(SpectraTalksSignUpForm, self).__init__(*args, **kwagrs)

            self.fields['first_name'].widget.attrs['class'] = 'form-control'
            self.fields['last_name'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['class'] = 'form-control'
            self.fields['consent'].widget.attrs['class'] = 'form-check-input'


class LukuRadioSignupForm(forms.ModelForm):
    class Meta:
        model = LukuRadioSignup
        fields = ("__all__")

        def __init__(self, *args, **kwagrs):
            super(LukuRadioSignupForm, self).__init__(*args, **kwagrs)

            self.fields['first_name'].widget.attrs['class'] = 'form-control'
            self.fields['last_name'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['class'] = 'form-control'
            self.fields['consent'].widget.attrs['class'] = 'form-check-input'


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class EventParticipantForm(forms.ModelForm):
    class Meta:
        model = EventParticipant
        fields = ("__all__")

        def __init__(self, *args, **kwagrs):
            super(EventParticipantForm, self).__init__(*args, **kwagrs)

            self.fields['first_name'].widget.attrs['class'] = 'form-control'
            self.fields['last_name'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['class'] = 'form-control'
            self.fields['consent'].widget.attrs['class'] = 'form-check-input'
            self.fields['event'].widget.attrs['class'] = 'form-control'
