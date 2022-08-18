"""boot_up URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from home import views
from django.urls import include 
from django.conf import settings

 

urlpatterns = [
    path('',views.home,name='home'),
    #path('<slug:category_slug>', views.home, name='products_by_category'),
    path('',include('django.contrib.auth.urls')),
    path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart/remove_product/<int:product_id>', views.cart_remove_product, name='cart_remove_product'),
    path('cart',views.cart,name='cart'),
    path('feedback',views.feedback,name='feedback'),
    path('signin',views.register,name='signin'),
    path('collection',views.collection,name='collection'),
    path('order_history/', views.orderHistory, name='order_history'),
    path('thankyou/<int:order_id>', views.thanks_page, name='thanks_page'), 
    path('shoes',views.shoes,name='shoes'),
    path('login/signup', views.signupView, name='signup'),
    path('<slug:category_slug>/<slug:product_slug>',views.productPage, name='product_detail'),
    
    #path('login/',views.login,name="login"),
    path('order/<int:product_id>', views.viewOrder, name='order_detail'),
    path('admi/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)