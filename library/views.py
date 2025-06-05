from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from firebase_admin import db
from .forms import BookForm
import logging
import time

logger = logging.getLogger(__name__)

def book_list(request):
    """Display all books from Firebase"""
    try:
        # Get reference to the books node in Firebase
        ref = db.reference('books')
        books_data = ref.get()
        
        # Handle empty database
        if books_data is None:
            books_data = {}
            
        # Calculate unique authors count
        unique_authors = set()
        if books_data:
            for book in books_data.values():
                if 'author_name' in book:
                    unique_authors.add(book['author_name'])
            
        context = {
            'books': books_data,
            'book_count': len(books_data),
            'unique_authors_count': len(unique_authors)
        }
        return render(request, 'library/book_list.html', context)
    
    except Exception as e:
        logger.error(f"Error fetching books: {str(e)}")
        messages.error(request, "Error loading books. Please try again.")
        return render(request, 'library/book_list.html', {'books': {}, 'book_count': 0})

def add_book(request):
    """Add a new book to Firebase"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                # Get form data
                book_data = {
                    'book_title': form.cleaned_data['book_title'],
                    'author_name': form.cleaned_data['author_name'],
                    'genre': form.cleaned_data['genre']
                }
                
                # Check if book ID already exists
                book_id = form.cleaned_data['id']
                ref = db.reference('books')
                existing_book = ref.child(str(book_id)).get()
                
                if existing_book:
                    messages.error(request, f"Book with ID {book_id} already exists!")
                    return render(request, 'library/add_book.html', {'form': form})
                
                # Add book to Firebase
                ref.child(str(book_id)).set(book_data)
                
                # Add success message
                messages.success(request, f"Book '{book_data['book_title']}' has been added successfully!")
                
                # Force a small delay to ensure Firebase write completes
                time.sleep(0.5)
                
                # Use HttpResponseRedirect for cleaner redirect
                return HttpResponseRedirect(reverse('book_list'))
                
            except Exception as e:
                logger.error(f"Error adding book: {str(e)}")
                messages.error(request, "Error adding book. Please try again.")
                return render(request, 'library/add_book.html', {'form': form})
        else:
            # Form validation failed
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookForm()
    
    return render(request, 'library/add_book.html', {'form': form})

def delete_book(request, book_id):
    """Delete a book from Firebase"""
    try:
        # Get reference to the specific book
        ref = db.reference('books').child(str(book_id))
        book_data = ref.get()
        
        if book_data is None:
            messages.error(request, "Book not found!")
            return HttpResponseRedirect(reverse('book_list'))
        
        # Store book title before deletion
        book_title = book_data.get('book_title', 'Unknown')
        
        # Delete the book
        ref.delete()
        
        # Add success message
        messages.success(request, f"Book '{book_title}' has been deleted successfully!")
        
        # Force a small delay to ensure Firebase delete completes
        time.sleep(0.5)
        
    except Exception as e:
        logger.error(f"Error deleting book {book_id}: {str(e)}")
        messages.error(request, "Error deleting book. Please try again.")
    
    # Use HttpResponseRedirect for cleaner redirect
    return HttpResponseRedirect(reverse('book_list'))