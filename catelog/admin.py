from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)

class BookInline(admin.StackedInline):
    model = Book
    extra = 0 # antal tomme rækker der vises
    # exclude = ['summary'] # ekskluderer summary
    # fields = ['title', 'isbn', 'genre', ] # viser kun disse felter
    fieldsets = ( # opdeler felterne i sektioner (virker kun med stackedInline)
        (None, {
            'fields': [('title', )]
        }),
        ('More fields', {
            'classes': ('collapse',),
            'fields': ('summary', 'isbn', 'genre', 'language'),
        }),
    )
    ordering = ['title'] # - for at sortere i omvendt rækkefølge

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['last_name', 'first_name', ('date_of_birth', 'date_of_death'), 'about',]
    # exclude = ['first_name'] # excluderer first_name

    inlines = [BookInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0 # antal tomme rækker der vises

# Register the Admin class for Book model using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BookInstanceInline]

# Register the Admin class for BookInstance model using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'imprint', 'borrower', 'due_back', 'status')
    list_filter = ('book', 'status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            # 'classes': ['collapse'],
            'fields': ('status', 'borrower', 'due_back') 
        }),
    )