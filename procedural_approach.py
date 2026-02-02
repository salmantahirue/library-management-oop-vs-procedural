"""
LIBRARY MANAGEMENT SYSTEM - PROCEDURAL/FUNCTIONAL APPROACH

Problem Statement:
A library needs to manage books, members, and track borrowing/returning operations.
Books have: title, author, ISBN, availability status
Members have: name, member_id, borrowed books list
Operations: Add book, Add member, Borrow book, Return book, View all books, View all members

This is a procedural/functional programming approach where we use:
- Dictionaries to store data
- Functions to perform operations
- No classes or objects
"""

# Global data structures (stored in memory)
books = {}  # {isbn: {title, author, isbn, is_available}}
members = {}  # {member_id: {name, member_id, borrowed_books: [isbn1, isbn2]}}
borrow_records = []  # List of all borrowing transactions

# Counter for generating IDs
book_counter = 0
member_counter = 0


def add_book(title, author, isbn):
    """
    Add a new book to the library.
    
    Args:
        title (str): Book title
        author (str): Book author
        isbn (str): Book ISBN
    
    Returns:
        dict: Result message
    """
    global books, book_counter
    
    # Check if book already exists
    if isbn in books:
        return {"success": False, "message": f"Book with ISBN {isbn} already exists!"}
    
    # Add book
    books[isbn] = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "is_available": True
    }
    book_counter += 1
    
    return {"success": True, "message": f"Book '{title}' added successfully!"}


def add_member(name, member_id):
    """
    Add a new member to the library.
    
    Args:
        name (str): Member name
        member_id (str): Unique member ID
    
    Returns:
        dict: Result message
    """
    global members, member_counter
    
    # Check if member already exists
    if member_id in members:
        return {"success": False, "message": f"Member with ID {member_id} already exists!"}
    
    # Add member
    members[member_id] = {
        "name": name,
        "member_id": member_id,
        "borrowed_books": []
    }
    member_counter += 1
    
    return {"success": True, "message": f"Member '{name}' added successfully!"}


def borrow_book(member_id, isbn):
    """
    Allow a member to borrow a book.
    
    Args:
        member_id (str): Member ID
        isbn (str): Book ISBN
    
    Returns:
        dict: Result message
    """
    global books, members, borrow_records
    
    # Check if member exists
    if member_id not in members:
        return {"success": False, "message": f"Member with ID {member_id} not found!"}
    
    # Check if book exists
    if isbn not in books:
        return {"success": False, "message": f"Book with ISBN {isbn} not found!"}
    
    # Check if book is available
    if not books[isbn]["is_available"]:
        return {"success": False, "message": f"Book '{books[isbn]['title']}' is not available!"}
    
    # Check if member already borrowed this book
    if isbn in members[member_id]["borrowed_books"]:
        return {"success": False, "message": f"Member already has this book borrowed!"}
    
    # Update book availability
    books[isbn]["is_available"] = False
    
    # Add to member's borrowed list
    members[member_id]["borrowed_books"].append(isbn)
    
    # Record transaction
    borrow_records.append({
        "member_id": member_id,
        "isbn": isbn,
        "action": "borrow",
        "timestamp": "2024-01-01"  # Simplified timestamp
    })
    
    return {
        "success": True,
        "message": f"Book '{books[isbn]['title']}' borrowed successfully by {members[member_id]['name']}!"
    }


def return_book(member_id, isbn):
    """
    Allow a member to return a book.
    
    Args:
        member_id (str): Member ID
        isbn (str): Book ISBN
    
    Returns:
        dict: Result message
    """
    global books, members, borrow_records
    
    # Check if member exists
    if member_id not in members:
        return {"success": False, "message": f"Member with ID {member_id} not found!"}
    
    # Check if book exists
    if isbn not in books:
        return {"success": False, "message": f"Book with ISBN {isbn} not found!"}
    
    # Check if member has this book borrowed
    if isbn not in members[member_id]["borrowed_books"]:
        return {"success": False, "message": f"Member doesn't have this book borrowed!"}
    
    # Update book availability
    books[isbn]["is_available"] = True
    
    # Remove from member's borrowed list
    members[member_id]["borrowed_books"].remove(isbn)
    
    # Record transaction
    borrow_records.append({
        "member_id": member_id,
        "isbn": isbn,
        "action": "return",
        "timestamp": "2024-01-01"  # Simplified timestamp
    })
    
    return {
        "success": True,
        "message": f"Book '{books[isbn]['title']}' returned successfully by {members[member_id]['name']}!"
    }


def get_all_books():
    """
    Get all books in the library.
    
    Returns:
        list: List of all books
    """
    return list(books.values())


def get_all_members():
    """
    Get all members in the library.
    
    Returns:
        list: List of all members
    """
    return list(members.values())


def get_available_books():
    """
    Get all available books.
    
    Returns:
        list: List of available books
    """
    return [book for book in books.values() if book["is_available"]]


def get_member_borrowed_books(member_id):
    """
    Get all books borrowed by a member.
    
    Args:
        member_id (str): Member ID
    
    Returns:
        list: List of borrowed books
    """
    if member_id not in members:
        return []
    
    borrowed_isbns = members[member_id]["borrowed_books"]
    return [books[isbn] for isbn in borrowed_isbns if isbn in books]


def reset_library():
    """
    Reset all library data (for testing purposes).
    """
    global books, members, borrow_records, book_counter, member_counter
    books = {}
    members = {}
    borrow_records = []
    book_counter = 0
    member_counter = 0


# Example usage (for testing)
if __name__ == "__main__":
    print("=== LIBRARY MANAGEMENT SYSTEM - PROCEDURAL APPROACH ===\n")
    
    # Add some books
    print("1. Adding books...")
    print(add_book("Python Programming", "John Doe", "ISBN001"))
    print(add_book("Data Structures", "Jane Smith", "ISBN002"))
    print(add_book("Algorithms", "Bob Johnson", "ISBN003"))
    
    # Add some members
    print("\n2. Adding members...")
    print(add_member("Alice", "M001"))
    print(add_member("Bob", "M002"))
    
    # Borrow books
    print("\n3. Borrowing books...")
    print(borrow_book("M001", "ISBN001"))
    print(borrow_book("M001", "ISBN002"))
    print(borrow_book("M002", "ISBN003"))
    
    # Try to borrow unavailable book
    print("\n4. Trying to borrow unavailable book...")
    print(borrow_book("M002", "ISBN001"))
    
    # View all books
    print("\n5. All books:")
    for book in get_all_books():
        status = "Available" if book["is_available"] else "Borrowed"
        print(f"  - {book['title']} by {book['author']} ({status})")
    
    # View all members
    print("\n6. All members:")
    for member in get_all_members():
        print(f"  - {member['name']} (ID: {member['member_id']})")
        borrowed = get_member_borrowed_books(member['member_id'])
        print(f"    Borrowed books: {len(borrowed)}")
    
    # Return a book
    print("\n7. Returning a book...")
    print(return_book("M001", "ISBN001"))
    
    print("\n8. Available books after return:")
    for book in get_available_books():
        print(f"  - {book['title']} by {book['author']}")
