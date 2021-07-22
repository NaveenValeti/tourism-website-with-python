from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Item


# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    validator = User.objects.basic_validator(request.POST)
    if len(validator) > 0:
        for key, value in validator.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashpw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email_address = request.POST['email'], password = hashpw)
        request.session['loggedInId'] = newUser.id
    return redirect('/success')

def success(request):
    if 'loggedInId' not in request.session:
        messages.error(request, "You must log in first")
        return redirect("/")
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
        'allItems': Item.objects.all(),
        'favItems': Item.objects.filter(wishlist=User.objects.get(id=request.session['loggedInId'])),
        'nonFav': Item.objects.exclude(wishlist=User.objects.get(id=request.session['loggedInId'])),
    }
    return render(request, 'success.html', context)

def login(request):
    loginValidator = User.objects.login_validator(request.POST)
    if len(loginValidator) > 0:
        for key, value in loginValidator.items():
            messages.error(request, value)
        return redirect('/')
    else:
        duplicateEmail = User.objects.filter(email_address = request.POST['email'])
        request.session['loggedInId'] = duplicateEmail[0].id
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect("/")

def createItem(request):
    return render(request, 'newItem.html')

def uploadItem(request):
    print(request.POST)
    itemErrors = Item.objects.item_validator(request.POST)
    print(itemErrors)
    if len(itemErrors) > 0:
        for key, value in itemErrors.items():
            messages.error(request, value)
        return redirect('/item/create')
    else:
        Item.objects.create(item = request.POST['itemName'], added_by = User.objects.get(id=request.session['loggedInId']), release_date = request.POST['rd'], plan = request.POST['plan'], start_date = request.POST['td'])
    return redirect("/success")

def itemInfo(request, itemId):
    anItem = Item.objects.get(id=itemId)
    context = {
        'anItem': anItem,
        'aUser': anItem.added_by.first_name,
        'lname': anItem.added_by.last_name
    }
    return render(request, 'itemInfo.html', context)

def addFav(request, itemId):
    Item.objects.get(id=itemId).wishlist.add(User.objects.get(id=request.session['loggedInId']))
    return redirect("/success")

def remove(request, itemId):
    Item.objects.get(id=itemId).wishlist.remove(User.objects.get(id=request.session['loggedInId']))
    return redirect("/success")

def delete(request, itemId):
    deleteItem = Item.objects.get(id=itemId)
    deleteItem.delete()
    return redirect("/success")