from django.shortcuts import render, redirect
from .models import *
from quotes.models import *
from django.contrib import messages

# Create your views here.
def quotes(request):
    if request.method == 'POST':
        errors = Quote.objects.validator(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect('quotes')
        Quote.objects.create(content=request.POST['content'], author=request.POST['author'], poster=User.objects.get(id=request.session['user_id']))
    context = {
        'quotes': Quote.objects.all()
    }
    return render(request, 'quotes.html', context)

def like(request, id):
    like_msg = Quote.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    like_msg.likes.add(user)
    return redirect('/quotes')

def delete(request, id):
    Quote.objects.get(id=id).delete()
    return redirect('/quotes')