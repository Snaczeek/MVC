from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import login_required
from django.contrib.auth.decorators import user_passes_test

from .models import Book, Borrow
from .forms import BookForm, AuthorForm, RegisterForm

# Helper function for decorators
def is_admin(user):
    return user.is_superuser

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

@user_passes_test(is_admin)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form})

@user_passes_test(is_admin)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form})

@user_passes_test(is_admin)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    
    return render(request, 'library/book_confirm_delete.html', {'book': book})

@login_required
def book_borrow(request, pk):
    book = get_object_or_404(Book, id=pk)

    if book.is_borrowed:
        return redirect('book_list')

    if request.method == 'POST':
        Borrow.objects.create(book=book, user=request.user)
        book.is_borrowed = True
        book.save()
        return redirect('book_list')

    return render(request, 'library/borrow_form.html', {'book': book})

@login_required
def book_return(request, pk):
    borrow = get_object_or_404(Borrow, id=pk, user=request.user)

    if request.method == 'POST':
        book = borrow.book
        book.is_borrowed = False
        book.save()
        borrow.delete()
        return redirect('my_borrows')
    
    return render(request, 'library/return_confirm.html', {'borrow': borrow})

@login_required
def my_borrows(request):
    borrows = Borrow.objects.filter(user=request.user).all()
    return render(request, 'library/my_borrows.html', {'borrows': borrows})

@user_passes_test(is_admin)
def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = AuthorForm()
    return render(request, 'library/author_form.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
