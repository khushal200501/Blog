from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from home.models import Contact
from apps.models import Post
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout

def home(request):
    allPosts = Post.objects.all()
    topPosts = Post.objects.all().order_by('-views')[:3]
    
    context={'allPosts':allPosts,'topPosts': topPosts,}
    return render(request, "home/home.html", context)    
    #return HttpResponse('home')

def about(request):
    messages.info(request, " Hold Tight! We are Under Development Mode. Your Next Great Experience is Loading.")
    return render(request,'home/about.html')

def contact(request):
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content= request.POST['content']

        if request.user.is_authenticated : 
            if len(name)<5 or len(email)<5 or len(phone)<10 or len(content)<4:
                messages.error(request, "Enter correct details.")
            else:
                contact=Contact(name=name, email=email, phone=phone, content=content)
                contact.save()
                messages.success(request, "Form submitted succesfully. We will get back to you soon.")
        else :
            messages.info(request, "Login/Signup is required to submit your query.")
            return redirect('/home/')
    return render(request,'home/contact.html')

def signuppage(request):
    if request.method =='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        # Check for errorneous inputs
        if len(username) > 10:
            messages.error(request, "Useranme cannot be greater than 10 characters.")
            return redirect('/')  
                
        if not username.isalnum():
            messages.error(request, "Username can contain letters and numbers only.")
            return redirect('/')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/') 

        # Create the user
        myuser=User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been created successfully.")
        return redirect('/')

    else:
        return HttpResponse('Signup Failed')
    
def loginpage(request):
    if request.method == 'POST':
        lusername=request.POST['lusername']
        lpassword=request.POST['lpassword']
        #Authenticate user
        user=authenticate(request,username=lusername, password=lpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in.")
            return redirect('/')

        else:
            messages.error(request, "Invalid login credentials.")
            return redirect("/")
    
    else:
        return HttpResponse("ERROR - 404 Page not found")

def logoutpage(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("/") 