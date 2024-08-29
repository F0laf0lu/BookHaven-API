from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=255, help_text="Enter a book genre e.g (Science Fiction)")

    def __str__(self) -> str:
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.first_name}, {self.last_name}'

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    genre = models.ManyToManyField(Genre, related_name="books", help_text="Select book genre")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['publication_date']