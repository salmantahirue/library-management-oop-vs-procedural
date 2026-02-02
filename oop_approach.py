"""
LIBRARY MANAGEMENT SYSTEM - OBJECT-ORIENTED PROGRAMMING APPROACH

Same problem solved using OOP principles:
- Encapsulation: Data and methods bundled together
- Abstraction: Hide complex implementation details
- Inheritance: Reusable code through class hierarchies
- Polymorphism: Different behaviors through method overriding

This approach uses:
- Classes to represent entities (Book, Member, Library)
- Methods to perform operations
- Private attributes with controlled access
- Better organization and maintainability
"""

from datetime import datetime
from typing import List, Optional


class Book:
    """
    Represents a book in the library.
    
    Encapsulation: All book-related data and operations are in one class.
    """
    
    def __init__(self, title: str, author: str, isbn: str):
        """
        Initialize a book.
        
        Args:
            title: Book title
            author: Book author
            isbn: Unique ISBN identifier
        """
        self._title = title  # Private attribute (encapsulation)
        self._author = author
        self._isbn = isbn
        self._is_available = True
        self._borrow_history = []  # Track who borrow ed this book
    
    # Getters (controlled access to private attributes)
    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
    
    @property
    def isbn(self):
        return self._isbn
    
    @property
    def is_available(self):
        return self._is_available
    
    @property
    def borrow_history(self):
        return self._borrow_history.copy()  # Return copy to prevent external modification
    
    def borrow(self, member_id: str) -> bool:
        """
        Mark book as borrowed.
        
        Args:
            member_id: ID of member borrowing the book
        
        Returns:
            bool: True if successful, False if already borrowed
        """
        if not self._is_available:
            return False
        
        self._is_available = False
        self._borrow_history.append({
            "member_id": member_id,
            "action": "borrow",
            "timestamp": datetime.now().isoformat()
        })
        return True
    
    def return_book(self, member_id: str) -> bool:
        """
        Mark book as returned.
        
        Args:
            member_id: ID of member returning the book
        
        Returns:
            bool: True if successful, False if not borrowed
        """
        if self._is_available:
            return False
        
        self._is_available = True
        self._borrow_history.append({
            "member_id": member_id,
            "action": "return",
            "timestamp": datetime.now().isoformat()
        })
        return True
    
    def to_dict(self):
        """Convert book to dictionary for JSON serialization."""
        return {
            "title": self._title,
            "author": self._author,
            "isbn": self._isbn,
            "is_available": self._is_available
        }
    
    def __str__(self):
        return f"Book(title='{self._title}', author='{self._author}', isbn='{self._isbn}')"
    
    def __repr__(self):
        return self.__str__()


class Member:
    """
    Represents a library member.
    
    Encapsulation: All member-related data and operations are in one class.
    """
    
    def __init__(self, name: str, member_id: str):
        """
        Initialize a member.
        
        Args:
            name: Member name
            member_id: Unique member ID
        """
        self._name = name  # Private attribute
        self._member_id = member_id
        self._borrowed_books: List[str] = []  # List of ISBNs
        self._borrow_history = []  # Track borrowing history
    
    # Getters
    @property
    def name(self):
        return self._name
    
    @property
    def member_id(self):
        return self._member_id
    
    @property
    def borrowed_books(self):
        return self._borrowed_books.copy()  # Return copy to prevent external modification
    
    @property
    def borrow_history(self):
        return self._borrow_history.copy()
    
    def can_borrow(self) -> bool:
        """
        Check if member can borrow more books.
        Business rule: Maximum 5 books at a time.
        
        Returns:
            bool: True if can borrow, False otherwise
        """
        return len(self._borrowed_books) < 5
    
    def add_borrowed_book(self, isbn: str) -> bool:
        """
        Add a book to member's borrowed list.
        
        Args:
            isbn: Book ISBN
        
        Returns:
            bool: True if successful, False if already borrowed or limit reached
        """
        if not self.can_borrow():
            return False
        
        if isbn in self._borrowed_books:
            return False
        
        self._borrowed_books.append(isbn)
        self._borrow_history.append({
            "isbn": isbn,
            "action": "borrow",
            "timestamp": datetime.now().isoformat()
        })
        return True
    
    def remove_borrowed_book(self, isbn: str) -> bool:
        """
        Remove a book from member's borrowed list.
        
        Args:
            isbn: Book ISBN
        
        Returns:
            bool: True if successful, False if not borrowed
        """
        if isbn not in self._borrowed_books:
            return False
        
        self._borrowed_books.remove(isbn)
        self._borrow_history.append({
            "isbn": isbn,
            "action": "return",
            "timestamp": datetime.now().isoformat()
        })
        return True
    
    def to_dict(self):
        """Convert member to dictionary for JSON serialization."""
        return {
            "name": self._name,
            "member_id": self._member_id,
            "borrowed_books": self._borrowed_books.copy(),
            "borrowed_count": len(self._borrowed_books)
        }
    
    def __str__(self):
        return f"Member(name='{self._name}', member_id='{self._member_id}')"
    
    def __repr__(self):
        return self.__str__()


class Library:
    """
    Represents the library system.
    
    This class manages all books and members, and coordinates operations.
    Encapsulation: All library operations are centralized here.
    """
    
    def __init__(self):
        """Initialize an empty library."""
        self._books: dict[str, Book] = {}  # {isbn: Book object}
        self._members: dict[str, Member] = {}  # {member_id: Member object}
    
    def add_book(self, title: str, author: str, isbn: str) -> dict:
        """
        Add a new book to the library.
        
        Args:
            title: Book title
            author: Book author
            isbn: Unique ISBN
        
        Returns:
            dict: Result message
        """
        if isbn in self._books:
            return {
                "success": False,
                "message": f"Book with ISBN {isbn} already exists!"
            }
        
        book = Book(title, author, isbn)
        self._books[isbn] = book
        
        return {
            "success": True,
            "message": f"Book '{title}' added successfully!"
        }
    
    def add_member(self, name: str, member_id: str) -> dict:
        """
        Add a new member to the library.
        
        Args:
            name: Member name
            member_id: Unique member ID
        
        Returns:
            dict: Result message
        """
        if member_id in self._members:
            return {
                "success": False,
                "message": f"Member with ID {member_id} already exists!"
            }
        
        member = Member(name, member_id)
        self._members[member_id] = member
        
        return {
            "success": True,
            "message": f"Member '{name}' added successfully!"
        }
    
    def borrow_book(self, member_id: str, isbn: str) -> dict:
        """
        Allow a member to borrow a book.
        
        This method coordinates between Book and Member objects.
        
        Args:
            member_id: Member ID
            isbn: Book ISBN
        
        Returns:
            dict: Result message
        """
        # Check if member exists
        if member_id not in self._members:
            return {
                "success": False,
                "message": f"Member with ID {member_id} not found!"
            }
        
        # Check if book exists
        if isbn not in self._books:
            return {
                "success": False,
                "message": f"Book with ISBN {isbn} not found!"
            }
        
        member = self._members[member_id]
        book = self._books[isbn]
        
        # Check if member can borrow more books
        if not member.can_borrow():
            return {
                "success": False,
                "message": f"Member has reached the borrowing limit (5 books)!"
            }
        
        # Check if book is available
        if not book.is_available:
            return {
                "success": False,
                "message": f"Book '{book.title}' is not available!"
            }
        
        # Perform the borrowing operation
        if book.borrow(member_id) and member.add_borrowed_book(isbn):
            return {
                "success": True,
                "message": f"Book '{book.title}' borrowed successfully by {member.name}!"
            }
        
        return {
            "success": False,
            "message": "Failed to borrow book. Please try again."
        }
    
    def return_book(self, member_id: str, isbn: str) -> dict:
        """
        Allow a member to return a book.
        
        Args:
            member_id: Member ID
            isbn: Book ISBN
        
        Returns:
            dict: Result message
        """
        # Check if member exists
        if member_id not in self._members:
            return {
                "success": False,
                "message": f"Member with ID {member_id} not found!"
            }
        
        # Check if book exists
        if isbn not in self._books:
            return {
                "success": False,
                "message": f"Book with ISBN {isbn} not found!"
            }
        
        member = self._members[member_id]
        book = self._books[isbn]
        
        # Check if member has this book borrowed
        if isbn not in member.borrowed_books:
            return {
                "success": False,
                "message": f"Member doesn't have this book borrowed!"
            }
        
        # Perform the return operation
        if book.return_book(member_id) and member.remove_borrowed_book(isbn):
            return {
                "success": True,
                "message": f"Book '{book.title}' returned successfully by {member.name}!"
            }
        
        return {
            "success": False,
            "message": "Failed to return book. Please try again."
        }
    
    def get_all_books(self) -> List[dict]:
        """Get all books in the library."""
        return [book.to_dict() for book in self._books.values()]
    
    def get_all_members(self) -> List[dict]:
        """Get all members in the library."""
        return [member.to_dict() for member in self._members.values()]
    
    def get_available_books(self) -> List[dict]:
        """Get all available books."""
        return [book.to_dict() for book in self._books.values() if book.is_available]
    
    def get_member_borrowed_books(self, member_id: str) -> List[dict]:
        """
        Get all books borrowed by a member.
        
        Args:
            member_id: Member ID
        
        Returns:
            List of book dictionaries
        """
        if member_id not in self._members:
            return []
        
        member = self._members[member_id]
        borrowed_books = []
        
        for isbn in member.borrowed_books:
            if isbn in self._books:
                borrowed_books.append(self._books[isbn].to_dict())
        
        return borrowed_books
    
    def reset_library(self):
        """Reset all library data (for testing purposes)."""
        self._books = {}
        self._members = {}


# Example usage (for testing)
if __name__ == "__main__":
    print("=== LIBRARY MANAGEMENT SYSTEM - OOP APPROACH ===\n")
    
    # Create library instance
    library = Library()
    
    # Add some books
    print("1. Adding books...")
    print(library.add_book("Python Programming", "John Doe", "ISBN001"))
    print(library.add_book("Data Structures", "Jane Smith", "ISBN002"))
    print(library.add_book("Algorithms", "Bob Johnson", "ISBN003"))
    
    # Add some members
    print("\n2. Adding members...")
    print(library.add_member("Alice", "M001"))
    print(library.add_member("Bob", "M002"))
    
    # Borrow books
    print("\n3. Borrowing books...")
    print(library.borrow_book("M001", "ISBN001"))
    print(library.borrow_book("M001", "ISBN002"))
    print(library.borrow_book("M002", "ISBN003"))
    
    # Try to borrow unavailable book
    print("\n4. Trying to borrow unavailable book...")
    print(library.borrow_book("M002", "ISBN001"))
    
    # View all books
    print("\n5. All books:")
    for book in library.get_all_books():
        status = "Available" if book["is_available"] else "Borrowed"
        print(f"  - {book['title']} by {book['author']} ({status})")
    
    # View all members
    print("\n6. All members:")
    for member in library.get_all_members():
        print(f"  - {member['name']} (ID: {member['member_id']})")
        print(f"    Borrowed books: {member['borrowed_count']}")
    
    # Return a book
    print("\n7. Returning a book...")
    print(library.return_book("M001", "ISBN001"))
    
    print("\n8. Available books after return:")
    for book in library.get_available_books():
        print(f"  - {book['title']} by {book['author']}")
