from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('lukufam/', views.lukufam, name='lukufam'),
    path('account/', views.account, name='account'),
    path('settings/', views.account_settings, name='account_settings'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('cart/', views.cart, name='cart'),
    path('confirmed/', views.confirmed, name='confirmed'),
    path('checkout/', views.checkout, name='checkout'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('help/', views.help, name='help'),
    path('updateItem/', views.updateItem, name='updateItem'),
    path('processOrder/', views.processOrder, name='processOrder'),
    path('music/', views.music, name='music'),
    path('music/mix/DJ-G400/<slug:slug>/',
         views.music_player, name='music_player'),
    path('gallery/', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('brands/', views.brand_list, name='brand_list'),
    path('brand/<slug:slug>/', views.brand_detail, name='brand_detail'),
    path('shop/<slug:slug>/', views.view_product, name='view_product'),
    path('404/', views.error404, name='error404'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('amapiano/', views.amapiano_workshop_signup,
         name='amapiano_workshop_signup'),
    path('<slug:slug>', views.view_stock, name='view_stock'),
    path('edit_stock/<slug:slug>/', views.edit_stock, name='edit_stock'),
    path('delete_stock/<slug:slug>/', views.delete_stock, name='delete_stock'),
    path('add_stock/', views.add_stock, name='add_stock'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
