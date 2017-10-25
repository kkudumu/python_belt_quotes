from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count
from .models import User, Quote
from django.core.exceptions import ObjectDoesNotExist
import time
import re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.
def index(request):
    return render(request, "quotes/index.html")

def register(request):
    logged = True
    if len(request.POST["name"]) < 2:
        messages.error(request, "The Name Field must have at least 2 characters")
        logged = False
    if request.POST["name"].isalpha() == False: 
        messages.error(request, "Your name can only have letters")
        logged = False
    if not EMAIL_REGEX.match(request.POST["email"]):
        messages.error(request, "Please enter a valid email address")
        logged = False  
    if len(request.POST["password"]) < 8:
        messages.error(request, "Your password must contain at least 8 characters")
        logged = False  
    if request.POST["password"] != request.POST["confirm_password"]:
        messages.error(request, "Your passwords didn't match")
        logged = False
    if len(request.POST["date_of_birth"]) < 1:
        messages.error(request, "Date of Birth Field cannot be empty")     
        logged = False
    if not logged:
        return redirect ("/")     
    
    User.objects.create(name=request.POST["name"], password=request.POST["password"], email=request.POST["email"], date_of_birth=request.POST["date_of_birth"])
    request.session["current_user"] = User.objects.get(email=request.POST["email"]).id
    return redirect("/quotes")

def login(request):
    try:
        users = User.objects.get(email=request.POST["email"], password=request.POST["password"])
    
    except ObjectDoesNotExist:
        messages.error(request, "Invalid username or password")
        return redirect("/")    
    
    else:
        context = {}
        request.session["current_user"] = User.objects.get(email=request.POST["email"], password=request.POST["password"]).id
        if "current_user" in request.session.keys():
            return redirect("/quotes")

def quotes(request):
    if "current_user" in request.session.keys():
        context = {
            "user" : User.objects.get(pk = request.session["current_user"]),
            "quotes" : Quote.objects.all().exclude(favorite__id = request.session["current_user"]),
            "other_quotes" : Quote.objects.all().exclude(favorite__id = request.session["current_user"]),
            "on_list" : Quote.objects.filter(favorite__id = request.session["current_user"]),
            "not_on_list" : Quote.objects.exclude(favorite__id = request.session["current_user"])
        }
    return render(request, "quotes/quotes.html", context)


def create(request):
    logged = True 
    if len(request.POST["quote_author"]) < 3:
        messages.error(request, "The 'Quoted By' field must have more than 3 characters")
        logged = False
    if len(request.POST["content"]) < 10:
        messages.error(request, "The quote must be longer than 10 characters.")
        logged = False
    else:
        newquote = Quote.objects.create(content = request.POST["content"], quote_author = request.POST["quote_author"], quote_submit = User.objects.get(id = User.objects.filter(id = request.session["current_user"])))
        newquote.save()
    return redirect("/quotes")

def show(request, id):
    if "current_user" in request.session.keys():
        poster = User.objects.filter(id = request.session["current_user"])
        quotes = Quote.objects.filter(favorite = poster)
        count = Quote.objects.filter(favorite = poster).count()
        context = {
            "poster": poster,
            "quotes": quotes,
            "count": count
        }
    return render(request, "quotes/show.html", context)

def add(request, id):
    # quotes_id = Quote.objects.get(id = id)
    print "1"
    # if len(Quote.objects.filter(id = quotes_id).filter(favorite = id)) > 0:
    #     messages.error(request, "You've already added this quote.")
    #     print "2"
    #     return redirect("/quotes")
    # else:
    if "current_user" in request.session.keys():
        quotes_id = Quote.objects.get(id = id)
        quote_add = User.objects.get(id = request.session["current_user"])
        add_favorite = Quote.objects.get(id = id)
        quote_add.favorite.add(add_favorite)
        quotes_id.save()
        add_favorite.save()
        quote_add.save()
        

    # add = Quote.objects.filter(id = User.objects.get(pk=request.session["current_user"])).add(quotes_id)
    # context = {
    #     "add" : add
    # }
    
    # print "5"
    return redirect("/quotes")

def remove(request, id):
    if "current_user" in request.session.keys():
        quotes_id = Quote.objects.get(id = id)
        quote_remove = User.objects.get(id = request.session["current_user"])
        remove_favorite = Quote.objects.get(id = id)
        Quote.objects.filter(id = id).delete()
        # Quote.objects.exclude(favorite__id = request.session["current_user"])
        

        
        
    # try:
    #     remove = Quote.objects.get(id = id)
    # except Quote.DoesNotExist:
    #     messages.error(request, "Quote doesn't exist.")
    # remove_user = User.objects.get(id = id)
    # remove_quote = Quote.objects.get(id = quotes_id)
    # quote_removed = remove_quote.favorite.remove(remove_user)
    # remove = Quote.objects.remove(request.session["current_user"], id)
    return redirect("/quotes")

def logout(request):
    request.session.clear()
    messages.add_message(request, messages.INFO, "Successfully logged out")
    return redirect("/")