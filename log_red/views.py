from django.shortcuts import render, redirect
from .models import *
from quotes.models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect('/')
        password = request.POST['password']
        confirm_pw = request.POST['confirm_pw']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        conf_hash = bcrypt.hashpw(confirm_pw.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, confirm_pw=conf_hash)
        request.session['name'] = new_user.first_name
        request.session['user_id'] = new_user.id
        return redirect('/quotes')
    return redirect('/')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    if request.method == 'POST':
        logged_user = User.objects.filter(email=request.POST['email'])
        if len(logged_user) > 0:
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['name'] = logged_user.first_name
                request.session['user_id'] = logged_user.id
                return redirect('/quotes')

def logout(request):
    request.session.flush()
    return redirect('/')

def edit_user(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        errors = User.objects.edit(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect(f'/edit_user/{user.id}')
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        return redirect('/quotes')
    context = {
        'edit_user': user
    }
    return render(request, 'edit_user.html', context)

def user(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'user.html', context)

def back(request):
    return redirect('/quotes')

