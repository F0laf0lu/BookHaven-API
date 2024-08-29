import random
from book_service.booktitles import generate_random_title
from datetime import datetime
from book_service.models import Author, Genre, Book, Publisher

def populate():
    
    authors = [ 
        Author(first_name='Isaac', last_name='Asimov'),
        Author(first_name='Arthur C.', last_name='Clarke'),
        Author(first_name='J.K.', last_name='Rowling'),
        Author(first_name='J.R.R.', last_name='Tolkien'),
        Author(first_name='George R.R.', last_name='Martin'),
        Author(first_name='Albert', last_name='Einstein'),
        Author(first_name='John', last_name='Thomas'),
        Author(first_name='Bob', last_name='Martin'),
        Author(first_name='Andrew', last_name='Hunt'),
        Author(first_name='Sidney', last_name='Sheldon')
    ]

    Author.objects.bulk_create(authors)

    genres = [
        Genre(name='Science Fiction'),
        Genre(name='Fantasy'),
        Genre(name='Adventure'),
        Genre(name='Mystery'),
        Genre(name='Historical Fiction'),
        Genre(name='Romance'),
        Genre(name='Memoir'),
        Genre(name='Self Help'),
        Genre(name='Horror'),
        Genre(name='Humor'),
        Genre(name='Biography'),
        Genre(name="Children's Literature"),
        Genre(name='Poetry'),
    ]

    Genre.objects.bulk_create(genres)


    publishers = [
        Publisher(name='Penguin Random House', address='123 Penguin St.', website='https://www.penguinrandomhouse.com/'),
        Publisher(name='HarperCollins', address='456 Harper Ave.', website='https://www.harpercollins.com/'),
        Publisher(name='Simon & Schuster', address='789 Simon Rd.', website='https://www.simonandschuster.com/'),

        Publisher(name='Macmillan Publishers', address='123 Macmillan Publishers St.', website='https://www.macmillan.com/'),
        Publisher(name='Scholastic', address='456 Harper Ave.', website='https://www.scholastic.com/'),
        Publisher(name='Parrésia Publishers', address='789 Simone Rd.', website='https://www.parrésiapublishers.com/'),
        
        Publisher(name='HarperCollins', address='123 harper collins St.', website='https://www.harpercollins.com/'),
        Publisher(name='Cassava Republic Press', address='456 cassava Ave.', website='https://www.cassavarepublicpress.com/'),
        Publisher(name='DAW Books', address='789 daw Rd.', website='https://www.dawbooks.com/'),
        
        Publisher(name='Harvard University Press', address='123 Havard St.', website='https://www.harvarduniversitypress.com/'),
        Publisher(name='Evans Brothers Ltd', address='456 Harper Ave.', website='https://www.evansbrothers.com/'),
        Publisher(name='Seven Stories Press', address='789 seven press Rd.', website='https://www.sevenstoriespress.com/'),
    ]

    Publisher.objects.bulk_create(publishers)


    # Fetch from db
    all_authors = list(Author.objects.all())
    all_genres = list(Genre.objects.all())
    all_publishers = list(Publisher.objects.all())

    books = []
    for i in range(100):
        title = generate_random_title()
        description = f'This is a summary for {title}. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum vestibulum. Cras venenatis euismod malesuada. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur fermentum, quam nec vestibulum ultrices, purus velit cursus mi, a tincidunt libero ipsum in velit.'
        author = random.choice(all_authors)
        publisher = random.choice(all_publishers)
        publication_date = datetime.now().date()
        price = round(random.uniform(5.0, 50.0), 2)

        book = Book(
            title=title,
            author=author,
            description=description,
            publisher=publisher,
            publication_date=publication_date,
            price=price
        )

        books.append(book)

    Book.objects.bulk_create(books)

    for book in Book.objects.all():
        # Randomly select 1-3 genres for each book
        genres = random.sample(all_genres, random.randint(1, 3))
        book.genre.set(genres)

    print('Database populated successfully with 100 books!')


if __name__ == '__main__':
    populate()
