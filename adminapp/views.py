from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from .models import * 
from adminapp.models import Book
from userapp.models import Order

# Create your views here.

def admindash(request):
    if not 'admin' in request.session:
        messages.error(request,"you are not logged in.'")
        return redirect('adminlogin')
    adminid =request.session.get('adminid')
    total_revenue=0
    orders = Order.objects.all()
    for order in orders:
        total_revenue += order.total_amount
    context= {
        'adminid':adminid,
        'user_count':UserInfo.objects.all().count(),
        'book_count':Book.objects.all().count(),
        'cat_count':Category.objects.all().count(),
        'order_count':Order.objects.all().count(),
        'enqs_count':Enquiry.objects.all().count(),
        'total_revenue':total_revenue


    }

    return render(request,"admindash.html",context)

def adminlogout(request):
    if 'admin' in request.session:
        del request.session['admin']
        messages.success(request,'you are logged out.')
        return redirect('index')
    else:
        messages.error(request,'something went to wrong')

def addcat(request):
    if not 'admin' in request.session:
        messages.error(request("you are not logged in.'"))
        return redirect('adminlogin')
    adminid =request.session.get('adminid')
    context= {
        'admin':adminid
    }
    if request.method=="POST":
        name=request.POST.get('name')
        description=request.POST.get('description')
        check=Category.objects.filter(name=name)
        if check:
            messages.warning(request,"Category already exist.")
            return redirect('addcat')
        
        Category.objects.create(name=name, description=description)
        messages.success(request,"Category added succussfully.")
        return redirect('viewcat')




    return render(request,"addcat.html",context)


def viewcat(request):
    if not 'admin' in request.session:
        messages.error(request("you are not logged in.'"))
        return redirect('adminlogin')
    adminid =request.session.get('adminid')
    cat=Category.objects.all()

    context= {
        'admin':adminid,
        'cat':cat,
        
    }

    return render(request,"viewcat.html",context)

def addbook(request):
    if not 'admin' in request.session:
        messages.error(request("you are not logged in.'"))
        return redirect('adminlogin')
    adminid =request.session.get('adminid')
    categories=Category.objects.all()
    context= {
        'admin':adminid,
        'categories':categories,
    }
    if request.method =="POST":
        title=request.POST.get('title')
        author =request.POST.get('author')
        catid=request.POST.get('catid')
        cat=Category.objects.get(id=catid)
       # category= cat,
        description=request.POST.get('description')
        original_price=request.POST.get('original_price')
        price =request.POST.get('price')
        published_date=request.POST.get('published_date')
        language=request.POST.get('language')
        cover_image=request.FILES.get('cover_image')
        stock=request.POST.get('stock')
        Book.objects.create(
            title=title,
            author=author,
            category= cat,
            description=description,
            original_price=original_price,
            price=price,
            published_date=published_date,
            language=language,
            cover_image=cover_image,
            stock=stock,

        )
        messages.success(request,"New book added succsessfully")
        return redirect('viewbook')
    

    return render(request,"addbook.html",context)

def viewenqs(request):
    if not 'admin' in request.session:
        messages.error(request("you are not logged in.'"))
        return redirect('adminlogin')
    adminid =request.session.get('adminid')
    enqs=Enquiry.objects.all()
    context= {
        'admin':adminid,
        'enqs':enqs
    }

    return render(request,"viewenqs.html",context)

def viewbook(request):
    if not 'admin' in request.session:
        messages.error(request,"you are not logged in.'")
        return redirect('adminlogin')
    adminid =request.session.get('adminid')
    books=Book.objects.all()
    context= {
        'admin':adminid,
        'books':books,
    
        
    }

    return render(request,"viewbook.html",context)

def adminpassword(request):

    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect('adminlogin')

    adminid = request.session.get('adminid')
    admin = admin.objects.get(id=adminid)

    if request.method == "POST":

        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        confirmpassword = request.POST.get('confirmpassword')

        # check old password
        if admin.password != oldpassword:
            messages.error(request, "Old password is incorrect")
            return redirect('adminpassword')

        # check new match
        if newpassword != confirmpassword:
            messages.error(request, "New passwords do not match")
            return redirect('adminpassword')

        # update password
        admin.password = newpassword
        admin.save()

        messages.success(request, "Password updated successfully")
        return redirect('adminpassword')

    context = {
        'admin': admin
    }

    return render(request, "adminpassword.html", context)









