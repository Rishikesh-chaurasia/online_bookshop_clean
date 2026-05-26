from django.shortcuts import render,redirect
from .models import Student

# Create your views here.
def index(request):
    context ={
        'name':'rishi',
        'age':'21',
        'city':'lucknow',
        'country':'india',

    }
    return render(request,'index.html',context)
def register(request):
    if request.method=="POST":
        rollno=request.POST.get('rollno')
        name=request.POST.get('name')
        course=request.POST.get('course')
        stu = Student(rollno=rollno,name=name,course=course)
        stu.save()
        return redirect('index')
    return render(request,'register.html')