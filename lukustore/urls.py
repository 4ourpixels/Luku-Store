from django.contrib import admin
from django.urls import path
from myapp.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index, name='index'),
    path('shop/', shop, name='shop'),
    path('blog/', blog_list, name='blog_list'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('lukufam/', lukufam, name='lukufam'),
    path('account/', account, name='account'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerPage, name='register'),
    path('cart/', cart, name='cart'),
    path('confirmed/', confirmed, name='confirmed'),
    path('checkout/', checkout, name='checkout'),
    path('newsletter/', newsletter, name='newsletter'),
    path('help/', help, name='help'),
    path('updateItem/', updateItem, name='updateItem'),
    path('processOrder/', processOrder, name='processOrder'),
    path('music/', music, name='music'),
    path('music/<int:id>/', music_player, name='music_player'),
    path('gallery/', gallery, name='gallery'),
    path('photo/<str:pk>/', viewPhoto, name='photo'),
    path('brands/', brand_list, name='brand_list'),
    path('<slug:slug>/', view_product, name='view_product'),
    path('404/', error404, name='error404'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
