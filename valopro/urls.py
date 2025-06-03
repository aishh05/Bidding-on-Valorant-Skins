"""
URL configuration for valopro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from valoapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name=''),
    
    #skins
    path('addskin/',views.addskin,name='addskin'),
    path('skinlist/',views.skinlist,name='skinlist'),
    path('updateskin/',views.updateskin,name='updateskin'),
    path('edit/<int:sid>',views.editbyid,name='edit'),
    path('delete/<int:sid>',views.deletebyid,name='delete'),
    path('shopcust/',views.shopcust,name='shopcust'),
     
    # customer
    path('addcustomer/',views.addcustomer,name='addcustomer'),
    path('customerlist/',views.customerlist,name='customerlist'),
    path('updateskin/',views.updateskin,name='updateskin'),
    path('edit/<str:cemailid>',views.editbyemail,name='edit'),
    path('delete/<str:cemailid>',views.deletebyemail,name='delete'),
    
    
    #bid
    path('place_bid/<int:sid>/', views.place_bid, name='place_bid'),
    path('add_bid_to_cart/<int:sid>/', views.add_bid_to_cart, name='add_bid_to_cart'),
    path('bidding/',views.bidding,name='bidding'),
    
    # cart
    path('addtocart/<int:sid>',views.addtocart,name='addtocart'),
    path('showcart/',views.showcart,name='showcart'),
    path('updateprice/<int:cid>/<int:q>/<str:tprice>/',views.updateprice,name='updateprice'),
    
    #login
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    
    # order
    path('placeorder/',views.placeorder,name='placeorder'),
    # payment
    path('placeorder/paymentsuccess',views.paymentsuccess,name='paymentsuccess')
    
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
