import json
import os

LIBRARY_FILE = "library.txt"
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_library(library):
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(library, file, indent=2)

def format_book(book, index=None):
    read_status = "Read" if book["read"] else "Unread"
    book_str = f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}"
    return f"{index + 1}. {book_str}" if index is not None else book_str


def add_book(library):
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    year = int(input("Enter the publication year: ").strip())
    genre = input("Enter the genre: ").strip()
    read_input = input("Have you read this book? (yes/no): ").strip().lower()
    read = read_input in ["yes", "y"]

    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    }

    library.append(book)
    print("✅ Book added successfully!")

def remove_book(library):
    title = input("Enter the title of the book to remove: ").strip().lower()
    for book in library:
        if book["title"].lower() == title:
            library.remove(book)
            print("✅ Book removed successfully!")
            return
    print("❌ Book not found.")

def search_book(library):
    print("Search by:\n1. Title\n2. Author")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        keyword = input("Enter the title: ").strip().lower()
        results = [book for book in library if keyword in book["title"].lower()]
    elif choice == '2':
        keyword = input("Enter the author: ").strip().lower()
        results = [book for book in library if keyword in book["author"].lower()]
    else:
        print("❌ Invalid choice.")
        return

    if results:
        print("🔍 Matching Books:")
        for i, book in enumerate(results):
            print(format_book(book, i))
    else:
        print("❌ No matching books found.")

def display_books(library):
    if not library:
        print("📭 Your library is empty.")
    else:
        print("📚 Your Library:")
        for i, book in enumerate(library):
            print(format_book(book, i))

def display_statistics(library):
    total = len(library)
    if total == 0:
        print("📊 No books in library to calculate stats.")
        return
    read_count = sum(1 for book in library if book["read"])
    percent_read = (read_count / total) * 100
    print(f"📈 Total books: {total}")
    print(f"📖 Percentage read: {percent_read:.1f}%")



def menu():
    library = load_library()
    while True:
        print("\n📘 Welcome to your Personal Library Manager")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_book(library)
        elif choice == '2':
            remove_book(library)
        elif choice == '3':
            search_book(library)
        elif choice == '4':
            display_books(library)
        elif choice == '5':
            display_statistics(library)
        elif choice == '6':
            save_library(library)
            print("💾 Library saved to file. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()
