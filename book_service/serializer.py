from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Genre, Author, Publisher, Book

class GenreSerializer(ModelSerializer):
    books_count = SerializerMethodField()
    class Meta:
        model = Genre
        fields = ['id','name', 'books_count']

    def get_books_count(self, genre):
        total = genre.books.all().count()
        return total


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']

class PublisherSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name']

class BookSerializer(ModelSerializer):
    author = AuthorSerializer()
    publisher = PublisherSerializer()
    genre = GenreSerializer(many=True)
    class Meta:
        model = Book
        fields = '__all__'