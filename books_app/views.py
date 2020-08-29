from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

def index(request):
    context = {
        'user': User.objects.all()
    }
    return render(request, 'index.html', context)

def register(request):
    errors = User.objects.validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    hashed_password = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_password)
    request.session['name'] = new_user.first_name
    request.session['id'] = new_user.id
    return redirect('/books')

def login(request):
    logged_user = User.objects.filter(email=request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
            request.session['name'] = logged_user.first_name
            request.session['id'] = logged_user.id
            return redirect('/books')
        else:
            messages.error(request, "Wrong password!")
            return redirect('/')
    else:
        messages.error(request, "Wrong email!")
        return redirect('/')

def books(request):
    if 'name' in request.session:
        context = {
            'all_books': Book.objects.all(),
            'logged_user': User.objects.get(id=request.session['id'])
        }
        request.session['mess_1'] = "This is one of your favorites"
        request.session['mess_2'] = "Add to Favorites"
        return render(request, 'books.html', context)        
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def add_book(request):
    errors = Book.objects.validate_book(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    uploaded_book = Book.objects.create(title=request.POST['title'], desc=request.POST['desc'], uploaded_by=User.objects.get(id=request.session['id']))
    user_liking=User.objects.get(id=request.session['id'])
    uploaded_book.users_who_like.add(user_liking)
    return redirect('/books')

def add_fav(request, book_id):
    user_liking=User.objects.get(id=request.session['id'])
    book_to_like = Book.objects.get(id=book_id)
    user_liking.liked_books.add(book_to_like)
    return redirect('/books')

def un_favorite(request, book_id):
    user_liking=User.objects.get(id=request.session['id'])
    book_liked = Book.objects.get(id=book_id)
    user_liking.liked_books.remove(book_liked)
    return redirect(f'/books/{book_id}')

def one_book(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id),
        'logged_user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'one_book.html', context)

def update(request, book_id):
    errors = Book.objects.validate_book(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/books/{book_id}')
    book = Book.objects.get(id=book_id)
    book.title = request.POST['title']
    book.desc = request.POST['desc']
    book.save()
    return redirect('/books')

def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/books')

def favorites(request):
    logged_user = User.objects.get(id=request.session['id'])
    context = {
        'fav_books': Book.objects.filter(users_who_like = logged_user).all()
    }
    return render(request, 'favorites.html', context)