from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth.models import User
from math import ceil
from django.contrib.auth.models import Group, User
from .forms import SignUpForm, ContactForm
from django.contrib.auth.models import auth, User
from .models import Category, Cart, CartItem, Order, OrderItem, Review, Product2, feedback
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.mail import send_mail
# Create your views here.


def home(request, category_slug=None):

    category_page = None
    products_list = None
    products_list2 = None
    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products_list = Product.objects.filter(
            category=category_page, available=True)
        products_list2 = Product2.objects.filter(
            category=category_page, available=True)

    else:
        products_list = Product.objects.all().filter(available=True)
        products_list2 = Product2.objects.all().filter(available=True)

    return render(request, 'E:\project_boot_up_1/index.html', {'category': category_page, 'products': products_list, 'products2': products_list2})


def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = User.objects.create_user(
            username=username, password=password, email=email, last_name=lastname, first_name=firstname)
        user.save()

        print('yoyoyoyoyoyoyoyoyoyoyoyoyoyoyoyooyoyoyoyoy')

    else:
        return render(request, "registration/register.html")


def feedback(request):
    if request.method == 'POST':
        feed = feedback()
        feed.name = request.POST.get('Name')
        feed.number = request.POST.get('Number')
        feed.email = request.POST.get('Email')
        feed.des = request.POST.get('Massage')
        feed.save()
        print(request.POST.get('Massage'))
    '''feedback.objects.create(name=request.POST['Name'],
                                number=num,
                                 email=email,
                                 des=message)'''
    return render(request, 'E:\project_boot_up_1/contact.html')


def collection(request, category_slug=None):
    category_page = None
    products_list = None
    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products_list = Product2.objects.filter(
            category=category_page, available=True)
    else:
        products_list = Product2.objects.all().filter(available=True)

    return render(request, 'E:\project_boot_up_1/collection.html', {'category': category_page, 'products': products_list})


def shoes(request, category_slug=None):
    category_page = None
    products_list = None
    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products_list = Product.objects.filter(
            category=category_page, available=True)
    else:
        products_list = Product.objects.all().filter(available=True)

    return render(request, 'E:\project_boot_up_1/shoes.html', {'category': category_page, 'products': products_list})


def productPage(request, category_slug, product_slug):
    try:
        print('yes')
        product = Product2.objects.get(
            category__slug=category_slug, slug=product_slug)
        if request.method == 'POST' and request.user.is_authenticated and request.POST['content'].strip() != '':
           print()
        return render(request, 'E:\project_boot_up_1/product.html', {'product': product})

    except Exception as e:
        try:
            product = display.objects.get(
                category__slug=category_slug, slug=product_slug)
            return render(request, 'E:\project_boot_up_1/product.html', {'product': product})
        except Exception as e:
            print('no')
            product = Product.objects.get(
                category__slug=category_slug, slug=product_slug)
            content = request.POST.get('size1')
            print(product)
            if request.method == 'POST' and request.user.is_authenticated and request.POST['content'].strip() != '':
                Review.objects.create(product=product,
                                    user=request.user,
                                    content=request.POST['content'])

            reviews = Review.objects.filter(product=product)
            return render(request, 'E:\project_boot_up_1/product.html', {'product': product, 'reviews': reviews})


def cart(request):
    return render(request, 'E:\project_boot_up_1/cart.html')


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
            )
        cart_item.save()

    return redirect('cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'BOOT UP- New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(
                email=email,
                source=token
            )
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency='INR',
                description=description,
                customer=customer.id
            )
            # Creating the order
            try:
                print("yes")
                a = Order.objects.create(
                    token=token,
                    total=total,
                    emailAddress=email,
                    billingName=billingName,
                    billingAddress1=billingAddress1,
                    billingCity=billingCity,
                    billingPostcode=billingPostcode,
                    billingCountry=billingCountry,
                    shippingName=shippingName,
                    shippingAddress1=shippingAddress1,
                    shippingCity=shippingCity,
                    shippingPostcode=shippingPostcode,
                    shippingCountry=shippingCountry
                )
                a.save()
               
                print("s")
                for order_item in cart_items:
                    or_item = OrderItem.objects.create(
                        product=order_item.product.name,
                        quantity=order_item.quantity,
                        price=order_item.product.price,
                        order=order_details
                    )
                    or_item.save()

                    # reduce stock
                    products = Product.objects.get(id=order_item.product.id)
                    products.stock = int(
                        order_item.product.stock - order_item.quantity)
                    products.save()
                    order_item.delete()

                    # print a message when the order is created
                    print('the order has been created')

                return redirect('thanks_page', order_details.id)
            except Exception:
                pass

        except stripe.error.CardError as e:
            return False, e
    return render(request, 'E:\project_boot_up_1/cart.html', dict(cart_items=cart_items, total=total, counter=counter,data_key=data_key, stripe_total=stripe_total, description=description))




def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')


def cart_remove_product(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')


def signupView(request):
    if request.method == 'POST':
        user=User()
        user.username=request.POST.get('user')
        user.first_name=request.POST.get('fname')
        user.last_name=request.POST.get('lname')
        user.email=request.POST.get('email')
        '''user.password=request.POST.get('pass')'''
        user.set_password(request.POST.get('pass'))
        user.save() 
        return redirect('/')

    else:
        return render(request, 'E:\project_boot_up_1/signup.html')

@login_required(redirect_field_name='next', login_url='login')
def orderHistory(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.filter(emailAddress=email)
        print(email)
        print(order_details)
    return render(request, 'E:\project_boot_up_1/orders_list.html', {'order_details': order_details})

def thanks_page(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
    return render(request, 'E:\project_boot_up_1/thankyou.html', {'customer_order': customer_order})

@login_required(redirect_field_name='next', login_url='login')
def orderHistory(request):
    if request.user.is_authenticated:
        email = request.user.email
        order_details = Order.objects.filter(emailAddress=email)
        print(email)
        print(order_details)
    return render(request, 'E:\project_boot_up_1/orders_list.html', {'order_details': order_details})

@login_required(redirect_field_name='next', login_url='signin')
def viewOrder(request,order_id):
    ne=order_id
    
    
    
    return render(request, 'E:\project_boot_up_1/order_detail.html')

def sendEmail(order_id):
    transaction = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=transaction)

    try:
        subject = "Bootup - New Order #{}".format(transaction.id)
        to = ['{}'.format(transaction.emailAddress)]
        from_email = "orders@Bootup.com"
        order_information = {
            'transaction': transaction,
            'order_items': order_items
        }
        message = get_template('E:\project_boot_up_1/email.html').render(order_information)
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
    except IOError as e:
        return e
