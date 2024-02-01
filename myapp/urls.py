from django.urls import path
from blog.views import add_blog
from .checkout import updateItem, processOrder, confirmed
from .event import event_signup
from .dashboard import dashboard
from .newsletter import newsletter
from .account import account, account_settings, loginPage, logoutUser, registerPage
from .product import view_product, edit_product, delete_product, add_product_photo, allProductPhotos, viewProductPhoto, viewProductVideo, handle_order
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('lukufam/', views.about, name='about'),
    path('account/', account, name='account'),
    path('settings/', account_settings, name='account_settings'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('add-blog/', add_blog, name='add_blog'),
    path('register/', registerPage, name='register'),
    path('cart/', views.cart, name='cart'),
    path('confirmed/', confirmed, name='confirmed'),
    path('checkout/', views.checkout, name='checkout'),
    path('newsletter/', newsletter, name='newsletter'),
    path('help/', views.help, name='help'),
    path('updateItem/', updateItem, name='updateItem'),
    path('processOrder/', processOrder, name='processOrder'),
    path('music/', views.music, name='music'),
    path('music/mix/DJ-G400/<slug:slug>/',
         views.music_player, name='music_player'),
    path('brands/', views.brand_list, name='brand_list'),
    path('brand/<slug:slug>/', views.brand_detail, name='brand_detail'),
    path('404/', views.error404, name='error404'),
    path('dashboard/', dashboard, name='dashboard'),
    path('amapiano/', views.amapiano_workshop_signup,
         name='amapiano_workshop_signup'),
    path('shop/<slug:slug>/', view_product, name='view_product'),
    path('edit_product/<slug:slug>/', edit_product, name='edit_product'),
    path('delete_product/<slug:slug>/',
         delete_product, name='delete_product'),
    path('add_product_photo/', add_product_photo, name='add_product_photo'),
    path('event/Spectra-Talks-with-Luku-Store-nl-and-WhoWhatWhereKE/',
         views.spectra_talks_signup, name='spectra_talks_signup'),
    path('all-product-photos/', allProductPhotos, name='allProductPhotos'),
    path('view-product-photo/<int:pk>',
         viewProductPhoto, name='viewProductPhoto'),
    path('view-product-video/<int:pk>',
         viewProductVideo, name='viewProductVideo'),
    path('search/', views.search_result, name='search_result'),
    path('Luku-Radio-Vol-02/', event_signup, name='event_signup'),
    path('handle_order/', handle_order, name='handle_order'),
]
