from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The all() is implied by default
    num_authors = Author.objects.count()

    # Books containing the word 'the' (case insensitive match)
    num_books_with_the = Book.objects.filter(title__icontains='the').count()

    # Genres containing the letter 'a' (case insensitive match)
    num_genres_with_a = Genre.objects.filter(name__icontains='a').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_with_the': num_books_with_the,
        'num_genres_with_a': num_genres_with_a,
    }

    # Render the HTML template with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    #  pagination: The different pages are accessed using GET parameters — 
    # to access page 2 you would use the URL /catalog/books/?page=2
    # Support to scroll through the result set is added to base_generic.html template.
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author