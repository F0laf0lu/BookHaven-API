from django.urls import path
from .views import BookListView, GenreListiew, BookRetrieveView, AuthorListiew

urlpatterns = [
    path('all_books', BookListView.as_view(), name='book_list'),
    path('<int:pk>', BookRetrieveView.as_view(), name='book'),
    path('genre', GenreListiew.as_view(), name='all-genre'),
    path('authors', AuthorListiew.as_view(), name='all-authors')
]
