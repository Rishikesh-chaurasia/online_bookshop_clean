from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import *
from adminapp.models import *
from .models import *


# ================= DASHBOARD =================
def userdash(request):
    if 'userid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('login')

    user = UserInfo.objects.get(email=request.session['userid'])

    return render(request, 'userdash.html', {
        'userid': request.session['userid'],
        'user': user
    })


# ================= PROFILE =================
def userprofile(request):
    if 'userid' not in request.session:
        return redirect('login')

    user = UserInfo.objects.get(email=request.session['userid'])

    return render(request, 'userprofile.html', {
        'userid': request.session['userid'],
        'user': user
    })


# ================= EDIT PROFILE =================
def editprofile(request):
    if 'userid' not in request.session:
        return redirect('login')

    user = UserInfo.objects.get(email=request.session['userid'])

    if request.method == "POST":
        user.name = request.POST.get('name')
        user.contactno = request.POST.get('contactno')
        user.address = request.POST.get('address')

        if request.FILES.get('profile'):
            user.picture = request.FILES.get('profile')

        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect('userprofile')

    return render(request, 'editprofile.html', {'user': user})


# ================= CART =================
def cart(request):
    if 'userid' not in request.session:
        return redirect('login')

    user = UserInfo.objects.filter(email=request.session['userid']).first()

    if not user:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=user)
    items = CartItem.objects.filter(cart=cart)

    total_price = sum(i.get_total_price() for i in items)

    return render(request, 'cart.html', {
        'user': user,
        'items': items,
        'total_price': total_price
    })


# ================= ADD TO CART =================
def addtocart(request, bid):
    if 'userid' not in request.session:
        return redirect('login')

    user = UserInfo.objects.filter(email=request.session['userid']).first()

    if not user:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=user)
    book = Book.objects.get(id=bid)

    quantity = int(request.POST.get('quantity', 1))

    CartItem.objects.create(
        cart=cart,
        book=book,
        quantity=quantity
    )

    messages.success(request, f"{book.title} added to cart")
    return redirect('index')


# ================= UPDATE ITEM =================
def updateitem(request, id, operator):
    if 'userid' not in request.session:
        return redirect('login')

    item = CartItem.objects.get(id=id)

    if operator == "+":
        if item.book.stock <= item.quantity:
            messages.warning(request, "Not enough stock")
            return redirect('cart')
        item.quantity += 1

    elif operator == "-":
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            messages.warning(request, "Item removed")
            return redirect('cart')

    item.save()
    messages.success(request, "Cart updated")
    return redirect('cart')


# ================= REMOVE ITEM =================
def removeitem(request, id):
    if 'userid' not in request.session:
        return redirect('login')

    CartItem.objects.filter(id=id).delete()

    messages.success(request, "Item removed")
    return redirect('cart')


# ================= CHECKOUT (NO STRIPE) =================
def checkout(request):
    if 'userid' not in request.session:
        return redirect('login')

    user = UserInfo.objects.get(email=request.session['userid'])

    cart, created = Cart.objects.get_or_create(user=user)
    items = CartItem.objects.filter(cart=cart)

    if not items.exists():
        messages.warning(request, "Cart is empty")
        return redirect('cart')

    # direct payment success (since Stripe removed)
    return redirect('payment-success')


# ================= PAYMENT SUCCESS =================
def payment_success(request):
    if 'userid' not in request.session:
        return redirect('login')

    user = UserInfo.objects.get(email=request.session['userid'])

    try:
        cart, created = Cart.objects.get_or_create(user=user)
        items = CartItem.objects.filter(cart=cart)

        if not items.exists():
            messages.warning(request, "Cart empty")
            return redirect('index')

        # STOCK CHECK
        for i in items:
            if i.book.stock < i.quantity:
                messages.error(request, f"{i.book.title} out of stock")
                return redirect('cart')

        total = sum(i.get_total_price() for i in items)

        order = Order.objects.create(
            user=user,
            total_amount=total
        )

        for i in items:
            book = i.book

            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=i.quantity,
                price=book.price
            )

            book.stock = max(0, book.stock - i.quantity)
            book.save()

        items.delete()

        messages.success(request, "Order placed successfully!")

        return render(request, 'payment_success.html', {
            'order': order
        })

    except Cart.DoesNotExist:
        return redirect('index')


# ================= ORDER =================
def order(request):
    if 'userid' not in request.session:
        return redirect('login')

    user = UserInfo.objects.get(email=request.session['userid'])

    orders = Order.objects.filter(user=user).order_by('-id')

    orderitems = []
    for o in orders:
        orderitems.append(OrderItem.objects.filter(order=o))

    return render(request, 'order.html', {
        'user': user,
        'orders': orders,
        'orderitems': orderitems
    })


# ================= CHANGE PASSWORD =================
def change_password(request):
    if 'userid' not in request.session:
        return redirect('login')

    user = UserInfo.objects.get(email=request.session['userid'])

    if request.method == "POST":

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if user.password != old_password:
            messages.error(request, "Old password is incorrect")
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('change_password')

        user.password = new_password
        user.save()

        messages.success(request, "Password changed successfully")
        return redirect('userprofile')

    return render(request, 'change_password.html')


# ================= LOGOUT =================
def userlogout(request):
    if 'userid' in request.session:
        del request.session['userid']
        messages.success(request, "Logged out successfully")

    return redirect('index')










    