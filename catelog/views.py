from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# import for forms
import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import ProtectedError

# from catelog.forms import RenewBookForm
from catelog.forms import RenewBookModelForm
# from catelog.forms import RenewBookForm
# from catelog.forms import RenewBookModelForm
from catelog.forms import RenewBookModelForm, BookInstanceUpdateForm

# Create your views here.
from .models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()  # type: ignore
    num_instances = BookInstance.objects.all().count()  # type: ignore

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()  # type: ignore

    # The all() is implied by default
    num_authors = Author.objects.count()  # type: ignore

    # Books containing the word 'the' (case insensitive match)
    num_books_with_the = Book.objects.filter(title__icontains="the").count()  # type: ignore

    # Genres containing the letter 'a' (case insensitive match)
    num_genres_with_a = Genre.objects.filter(name__icontains="a").count()  # type: ignore

    # Number of visits to this page, as counted in the session variable.
    num_visits = request.session.get("num_visits", 0)
    num_visits += 1
    request.session["num_visits"] = num_visits

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_books_with_the": num_books_with_the,
        "num_genres_with_a": num_genres_with_a,
        "num_visits": num_visits,
    }

    # Render the HTML template with the data in the context variable
    return render(request, "index.html", context=context)


from django.views import generic


class BookListView(generic.ListView):
    model = Book
    #  pagination: The different pages are accessed using GET parameters —
    # to access page 2 you would use the URL /catalog/books/?page=2
    # Support to scroll through the result set is added to base_generic.html template.
    paginate_by = 15


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
    template_name = "catelog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)  # type: ignore
            .filter(status__exact="o")
            .order_by("due_back")
        )


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books loaned out to users."""

    permission_required = "catelog.can_mark_returned"
    model = BookInstance
    template_name = "catelog/bookinstance_list_loaned_out.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")  # type: ignore


@login_required
@permission_required("catelog.can_mark_returned", raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST method then process the Form data
    if request.method == "POST":
        # Create a form instance and populate it with data from the request (binding):
        # form = RenewBookForm(request.POST)
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            # book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.due_back = form.cleaned_data["due_back"]
            book_instance.save()

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse("loaned-out"))

    # If this is a GET (or any other method) create the default form:
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        # form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})
        form = RenewBookModelForm(initial={"due_back": proposed_renewal_date})

    context = {
        "form": form,
        "book_instance": book_instance,
    }

    return render(request, "catelog/book_renew_librarian.html", context=context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death", "about"]
    initial = {"date_of_death": "11/11/2023"}
    permission_required = "catelog.add_author"


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # Not recommended (potential security issue if more fields added)
    fields = "__all__"
    permission_required = "catelog.change_author"


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy("authors")
    permission_required = "catelog.delete_author"

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        # except Exception as e: # udkommenteret da e ikke bruges
        except Exception:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )


myBookFields = ["title", "author", "summary", "isbn", "genre", "language"]


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    # fields = ["title", "author", "summary", "isbn", "genre", "language"]
    fields = myBookFields
    permission_required = "catelog.add_book"
    # help_text = {"author": "Skriv kort resume af bogen her ..."}  # virker ikke ..


class BookUpdate(PermissionRequiredMixin, UpdateView):
    """View der viser en form til editering af en eksisterende instans af en bog (Book)
    Args:
        PermissionRequiredMixin (_type_): _description_
        UpdateView (_type_): _description_
    """

    model = Book
    fields = myBookFields
    permission_required = "catelog.change_book"


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy("books")
    permission_required = "catelog.delete_book"

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except ProtectedError as e:
            # Book cannot be deleted because it has related BookInstances
            print(f"Cannot delete book '{self.object.title}': {e}")
            return HttpResponseRedirect(
                reverse("book-delete", kwargs={"pk": self.object.pk})
            )


myBookInstanceFields = ["book", "imprint", "due_back", "status", "borrower"]


class BookInstanceCreate(PermissionRequiredMixin, CreateView):
    model = BookInstance
    fields = myBookInstanceFields
    permission_required = "catelog.add_bookinstance"
    # success_url = reverse_lazy("book-detail", 10)
    # success_url = reverse_lazy("books")

    def get_initial(self):
        """Set initial values for the form."""
        initial = super().get_initial()
        # Get the book ID from the URL parameter
        book_id = self.kwargs.get("pk")
        if book_id:
            initial["book"] = book_id
        return initial


class BookInstanceUpdate(PermissionRequiredMixin, UpdateView):
    """View der viser en form til editering af en eksisterende 
       instans af en bog-kopi (Bookinstance)"""

    model = BookInstance
    # fields = ["book", "imprint", "due_back", "status", "borrower"]  # Exclude 'id' field
    form_class = BookInstanceUpdateForm
    permission_required = "catelog.change_bookinstance"
    
    def get_context_data(self, **kwargs):
        """Add custom variables to the template context."""
        context = super().get_context_data(**kwargs)
        
        # Add custom variables
        context['is_update'] = True # bruges i template til check for om det er create eller update.
        # context['book_instance'] = self.object
        context['book_title'] = self.object.book.title if self.object.book else "No book"
        context['instance_id'] = str(self.object.id)
        # context['status_display'] = self.object.get_status_display()  # Human-readable status
        # context['is_overdue'] = self.object.is_overdue  # Property from model
        # context['borrower_name'] = self.object.borrower.get_full_name() if self.object.borrower else "None"
        
        return context

class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
    model = BookInstance
    # success_url = reverse_lazy("books")
    permission_required = "catelog.delete_bookinstance"
    
    def form_valid(self, form):
        try:
            self.object.delete()
            # return HttpResponseRedirect(self.success_url)
            return HttpResponseRedirect(
                reverse("book-detail", kwargs={"pk": self.object.book.pk})
            )
        except Exception as e:
            print(f"Copy cannot be deleted due to exception '{e}'")
            return HttpResponseRedirect(
                reverse("bookinstance-delete", kwargs={"pk": self.object.pk})
            )
