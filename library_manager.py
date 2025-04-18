import sqlite3

def get_connection():
    return sqlite3.connect('library.db')

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            year INTEGER,
            genre TEXT,
            read BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

def fetch_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()

    library = []
    for row in rows:
        library.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "year": row[3],
            "genre": row[4],
            "read": bool(row[5])
        })
    return library

def format_book(book, index=None):
    read_status = "Read" if book["read"] else "Unread"
    book_str = f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}"
    return f"{index + 1}. {book_str}" if index is not None else book_str

def add_book(_):
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    year = int(input("Enter the publication year: ").strip())
    genre = input("Enter the genre: ").strip()
    read_input = input("Have you read this book? (yes/no): ").strip().lower()
    read = read_input in ["yes", "y"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (title, author, year, genre, read)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, author, year, genre, read))
    conn.commit()
    conn.close()
    print("✅ Book added to database!")

def remove_book(_):
    title = input("Enter the title of the book to remove: ").strip().lower()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE LOWER(title) = ?", (title,))
    if cursor.rowcount:
        print("✅ Book removed from database!")
    else:
        print("❌ Book not found.")
    conn.commit()
    conn.close()

def search_book(_):
    library = fetch_all_books()
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

def display_books(_):
    library = fetch_all_books()
    if not library:
        print("📭 Your library is empty.")
    else:
        print("📚 Your Library:")
        for i, book in enumerate(library):
            print(format_book(book, i))

def display_statistics(_):
    library = fetch_all_books()
    total = len(library)
    if total == 0:
        print("📊 No books in library to calculate stats.")
        return
    read_count = sum(1 for book in library if book["read"])
    percent_read = (read_count / total) * 100
    print(f"📈 Total books: {total}")
    print(f"📖 Percentage read: {percent_read:.1f}%")

def menu():
    create_table()
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
            add_book(None)
        elif choice == '2':
            remove_book(None)
        elif choice == '3':
            search_book(None)
        elif choice == '4':
            display_books(None)
        elif choice == '5':
            display_statistics(None)
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
