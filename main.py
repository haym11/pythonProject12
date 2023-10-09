from pydantic import BaseModel

class BookModel(BaseModel):
    title: str
    author: str
    year: int

    def __str__(self):
        return f"{self.title} ({self.year}) by {self.author}"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)

    def list_books(self):
        for book in self.books:
            print(book)

    def books_by_author(self, author):
        for book in self.books:
            if book.author == author:
                print(book)

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for book in self.books:
                file.write(f"{book.title},{book.author},{book.year}\n")

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(',')
                title, author, year = data
                book = BookModel(title=title, author=author, year=int(year))
                self.add_book(book)

def log_add_book(func):
    def wrapper(self, book):
        print(f"Adding book: {book}")
        func(self, book)
        print("Book added successfully")
    return wrapper

def check_book_exists(func):
    def wrapper(self, book):
        if book in self.books:
            func(self, book)
            print("Book removed successfully")
        else:
            print("Book not found in the library")
    return wrapper

class LibraryWithDecorators(Library):

    @log_add_book
    def add_book(self, book):
        super().add_book(book)

    @check_book_exists
    def remove_book(self, book):
        super().remove_book(book)

class FileManager:
    def __init__(self, library):
        self.library = library

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def save_library(self, filename):
        self.library.save_to_file(filename)

    def load_library(self, filename):
        self.library.load_from_file(filename)

if __name__ == "__main__":
    library = LibraryWithDecorators()

    book1 = BookModel(title="Book 1", author="Author 1", year=2020)
    book2 = BookModel(title="Book 2", author="Author 2", year=2021)
    journal1 = BookModel(title="Journal 1", author="Author 1", year=2022)

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(journal1)

    print("Library Contents:")
    library.list_books()

    print("\nBooks by Author 1:")
    library.books_by_author("Author 1")

    with FileManager(library) as fm:
        fm.save_library("library.txt")

    library.remove_book(book1)

    print("\nLibrary Contents after removing Book 1:")
    library.list_books()

    with FileManager(library) as fm:
        fm.load_library("library.txt")

    print("\nLibrary Contents after loading from file:")
    library.list_books()
