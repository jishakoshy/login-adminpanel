from django.db import connection
from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from .models import SampleUser
from django.contrib import messages


# Create your views here.
@never_cache
def signup(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password1']
        cpassword = request.POST['password2']
        user = SampleUser(first_name= fname,last_name=lname,username=username,password=password)
        user.save()
        return redirect('login')
    return render(request,'signup.html')


@never_cache
def HomePage(request):
    if 'username' in request.session:
        username = request.session['username']
        user = SampleUser.objects.get(username=username)
        return render(request, 'home.html')
    else:
        return redirect('login')



@never_cache
def LoginPage(request):
    if 'username' in request.session:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass')
            try:

                user = SampleUser.objects.get(username = username,password = password)
                if user is not None:
                    if not user.is_superuser:
                        request.session['username'] = username
                        return redirect('home')
                else:
                    message = "Username or Password is incorrect"
                    return render(request, 'login.html', {'message': message})
            except SampleUser.DoesNotExist:
                message = "Username or Password is incorrect"
                return render(request, 'login.html', {'message': message})
        return render(request, 'login.html')
 
    
@never_cache
def Logout(request):
    if 'username' in request.session:
        request.session.flush()
        return redirect('login')

@never_cache
def adminlogin(request):
    if 'username' in request.session:
        username = request.session['username']
        user = SampleUser.objects.get(username = username)
        if user.is_superuser:
            return redirect('adminpanel')
        else:
            return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = SampleUser.objects.get(username= username,password=password)
            if user is not None:
                if user.is_superuser:
                    request.session['username'] = username
                    return redirect('adminpanel')
                else:
                    messages.info(request,'login using user credentails')
                    return redirect('login')
        except SampleUser.DoesNotExist:
            messages.info(request,'invalid credentials')
            return redirect('login')
    return render(request,'admin.html')

@never_cache
def adminpanel(request):
    # if request.method == 'POST':
        if 'username' in request.session:
            username = request.session['username']
            user = SampleUser.objects.get(username=username)
            if user.is_superuser:
                search = request.POST.get('search')

                if search:
                    userinfo = SampleUser.objects.filter(username__startswith=search)

                else:
                    userinfo = SampleUser.objects.filter(is_superuser = False)
                return render(request,'adminpanel.html',{'datas':userinfo})
        return redirect('login')

@never_cache
def adduser(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password1']
        cpassword = request.POST['password2']
        user = SampleUser(first_name= fname,last_name=lname,username=username,password=password)
        user.save()
        return redirect('adminpanel')
    return render(request,'adduser.html')



@never_cache
def edituser(request,id):
    if 'username' in request.session:
        user = SampleUser.objects.get(id = id)
        return render(request,'edit_user.html',{'user':user})

@never_cache
def updatedata(request,id):
    user = SampleUser.objects.get(id=id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.last_name = request.POST.get('lname')
        user.save()
        return redirect('adminpanel')
    return redirect(request,'edit_user',{'user':user})
@never_cache
def deleteuser(request,id):
    user = SampleUser.objects.get(id =id)
    user.delete()
    return redirect('adminpanel')


