from django import forms
from django.core.exceptions import ValidationError
import re

class BookForm(forms.Form):
    id = forms.IntegerField(
        label='Book ID',
        min_value=1,
        max_value=999999,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter unique book ID (e.g., 1001)',
            'min': '1',
            'max': '999999'
        }),
        help_text='Enter a unique positive number between 1 and 999999'
    )
    
    book_title = forms.CharField(
        label='Book Title',
        max_length=200,
        min_length=1,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the book title',
            'maxlength': '200'
        }),
        help_text='Enter the full title of the book'
    )
    
    author_name = forms.CharField(
        label='Author Name',
        max_length=150,
        min_length=2,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter author\'s full name',
            'maxlength': '150'
        }),
        help_text='Enter the author\'s full name'
    )
    
    genre = forms.ChoiceField(
        label='Genre',
        choices=[
            ('', 'Select a genre'),
            ('fiction', 'Fiction'),
            ('non-fiction', 'Non-Fiction'),
            ('mystery', 'Mystery'),
            ('romance', 'Romance'),
            ('sci-fi', 'Science Fiction'),
            ('fantasy', 'Fantasy'),
            ('biography', 'Biography'),
            ('history', 'History'),
            ('self-help', 'Self-Help'),
            ('business', 'Business'),
            ('children', 'Children'),
            ('young-adult', 'Young Adult'),
            ('poetry', 'Poetry'),
            ('drama', 'Drama'),
            ('other', 'Other'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text='Select the most appropriate genre for this book'
    )
    
    def clean_book_title(self):
        """Validate and clean book title"""
        title = self.cleaned_data.get('book_title', '').strip()
        
        if not title:
            raise ValidationError("Book title is required.")
        
        if len(title) < 1:
            raise ValidationError("Book title must be at least 1 character long.")
        
        if len(title) > 200:
            raise ValidationError("Book title cannot exceed 200 characters.")
        
        # Check for valid characters (allow letters, numbers, spaces, and common punctuation)
        if not re.match(r'^[a-zA-Z0-9\s\-_.,!?:()&\'\"]+$', title):
            raise ValidationError("Book title contains invalid characters.")
        
        return title
    
    def clean_author_name(self):
        """Validate and clean author name"""
        author = self.cleaned_data.get('author_name', '').strip()
        
        if not author:
            raise ValidationError("Author name is required.")
        
        if len(author) < 2:
            raise ValidationError("Author name must be at least 2 characters long.")
        
        if len(author) > 150:
            raise ValidationError("Author name cannot exceed 150 characters.")
        
        # Check for valid characters (allow letters, spaces, dots, hyphens, apostrophes)
        if not re.match(r'^[a-zA-Z\s.\-\']+$', author):
            raise ValidationError("Author name should only contain letters, spaces, dots, hyphens, and apostrophes.")
        
        return author
    
    def clean_id(self):
        """Validate book ID"""
        book_id = self.cleaned_data.get('id')
        
        if book_id is None:
            raise ValidationError("Book ID is required.")
        
        if book_id <= 0:
            raise ValidationError("Book ID must be a positive number.")
        
        if book_id > 999999:
            raise ValidationError("Book ID cannot exceed 999999.")
        
        return book_id
    
    def clean_genre(self):
        """Validate genre selection"""
        genre = self.cleaned_data.get('genre')
        
        if not genre:
            raise ValidationError("Please select a genre.")
        
        valid_genres = [choice[0] for choice in self.fields['genre'].choices if choice[0]]
        if genre not in valid_genres:
            raise ValidationError("Please select a valid genre.")
        
        return genre
    
    def clean(self):
        """Additional form-wide validation"""
        cleaned_data = super().clean()
        
        # You can add cross-field validation here if needed
        # For example, checking if certain combinations are valid
        
        return cleaned_data