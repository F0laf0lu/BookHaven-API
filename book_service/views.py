from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Genre, Author
from .serializer import BookSerializer, GenreSerializer, AuthorSerializer

# Create your views here.
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all().prefetch_related('genre').select_related('author', 'publisher')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'author', 'price', 'publication_date']
    search_fields = ['title', 'author__first_name', 'author__last_name', 'genre__name', 'publisher__name']
    ordering_fields = ['price', 'publication_date']
    


class BookRetrieveView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class GenreListiew(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = None


class AuthorListiew(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = None
    search_fields = ['first_name', 'last_name']

