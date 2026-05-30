from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from adminapp.models import *
# Create your views here.


def index(request):
    books = Book.objects.all().order_by('-id')

    print("TOTAL BOOKS =", books.count())

    recent_books = books[:8]

    old_books = Book.objects.filter(category__name="Old")[:8]

    suggested_books = books.exclude(
        id__in=recent_books.values_list('id', flat=True)
    ).order_by('?')[:8]

    return render(request, 'index.html', {
        'books': books,
        'recent_books': recent_books,
        'old_books': old_books,
        'suggested_books': suggested_books
    })



def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Password check
        if password != cpassword:
            messages.warning(request, "Password and Confirm Password do not match.")
            return redirect('register')

        # Check if email already exists
        check = LoginInfo.objects.filter(username=email)
        if check:
            messages.warning(request, "This email is already registered.")
            return redirect('register')
        log=LoginInfo(username=email,password=password)
        user=UserInfo(login=log,name=name,email=email,contactno=contactno)
        log.save()
        user.save()
        messages.success(request,"Registered successfull . ")
        return redirect('register')
        
    return render(request,"register.html")

def contactpage(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        contactno=request.POST.get('contactno')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        Enquiry.objects.create(name=name,email=email,contactno=contactno,subject=subject,message=message)
        messages.success(request,'Enquiry has been submited')
        return redirect('contactpage')

    return render(request, "contactpage.html")
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LoginInfo

def login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = LoginInfo.objects.get(
                usertype="user",
                username=username,
                password=password
            )

            # ✅ session set FIRST
            request.session['userid'] = user.username

            messages.success(request, "Welcome User")

            return redirect('index')

        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')

def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            admin = LoginInfo.objects.get(usertype="admin", username=username, password=password)
            if admin is not None:
                messages.success(request, "Welcome admin")
                request.session['admin']=admin.username
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return redirect('adminlogin')
    return render(request, 'adminlogin.html')


def  book_detail(request,id):
    book=Book.objects.get(id=id)
    context={
        'book':book,
    }
    return render(request,'book_detail.html',context)

from django.db.models import Q

def searchbook(request):

    query = request.GET.get('q')

    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(author__icontains=query)
    )

    return render(request, 'search.html', {'books': books, 'query': query})


def about(request):
    return render(request, 'about.html')

            
    




