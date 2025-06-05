from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

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

    # Number of visits to this page, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_with_the': num_books_with_the,
        'num_genres_with_a': num_genres_with_a,
        'num_visits': num_visits,
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

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing book on loan by current user."""
    model = BookInstance
    template_name = 'catelog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    
class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books loaned out to users."""
    permission_required = 'catelog.can_mark_returned'
    model = BookInstance
    template_name = 'catelog/bookinstance_list_loaned_out.html'
    paginate_by = 10

    def get_queryset(self):
        return(
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )