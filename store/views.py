from django.shortcuts import render, redirect
from django.http import JsonResponse
import datetime
from .models import *
from .extras import *
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(request, username=username, password=password)
            customer, created = Customer.objects.get_or_create(user=user, name=request.POST.get('username'),
                                                      email=request.POST.get('email'))
            customer.save()
            loginUser(request)
            return redirect('store')
    cartItems = 0
    context = {'form': form, 'cartItems':cartItems}
    return render(request, 'store/register.html', context)


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not password:
            password = request.POST.get('password1')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.user.customer = Customer.objects.get(name=username)
            return redirect('store')
        else:
            messages.info(request, 'Username or password is incorrect')
    cartItems=0
    context = {'cartItems':cartItems}
    return render(request, 'store/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('store')


def store(request):
    data = cartData(request)
    context = {'products': Product.objects.all(), 'cartItems': data['cartItems']}
    return render(request, 'store/products.html', context)


def cart(request):
    data = cartData(request)
    context = {'items': data['items'], 'order': data['order'], 'cartItems': data['cartItems']}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    context = {'items': data['items'], 'order': data['order'], 'cartItems': data['cartItems']}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        zipcode=data['shipping']['zipcode'],
    )
    return JsonResponse('Payment submitted..', safe=False)
