"""
Flask Backend API for Library Management System Tutorial

This API serves both procedural and OOP approaches and provides
endpoints for the frontend to interact with.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import procedural_approach as procedural
import oop_approach as oop

app = Flask(__name__)
CORS(app)

# Store instances for each approach
procedural_library = None
oop_library = None


def init_procedural():
    """Initialize procedural library state."""
    global procedural_library
    procedural.reset_library()
    procedural_library = "initialized"


def init_oop():
    """Initialize OOP library state."""
    global oop_library
    oop_library = oop.Library()


@app.route('/')
def index():
    """Serve the main tutorial page."""
    return render_template('index.html')


@app.route('/api/problem-statement', methods=['GET'])
def get_problem_statement():
    """Get the problem statement."""
    return jsonify({
        "title": "Library Management System",
        "description": """
        A library needs to manage books, members, and track borrowing/returning operations.
        
        Requirements:
        - Books have: title, author, ISBN, and availability status
        - Members have: name, member ID, and list of borrowed books
        - Operations needed:
          * Add new books to the library
          * Register new members
          * Allow members to borrow books
          * Allow members to return books
          * View all books and their availability
          * View all members and their borrowed books
        
        This is a real-world scenario that demonstrates how different programming
        paradigms approach the same problem differently.
        """
    })


@app.route('/api/procedural/init', methods=['POST'])
def init_procedural_library():
    """Initialize procedural library."""
    init_procedural()
    return jsonify({"success": True, "message": "Procedural library initialized"})


@app.route('/api/procedural/add-book', methods=['POST'])
def procedural_add_book():
    """Add a book using procedural approach."""
    data = request.json
    result = procedural.add_book(
        data.get('title'),
        data.get('author'),
        data.get('isbn')
    )
    return jsonify(result)


@app.route('/api/procedural/add-member', methods=['POST'])
def procedural_add_member():
    """Add a member using procedural approach."""
    data = request.json
    result = procedural.add_member(
        data.get('name'),
        data.get('member_id')
    )
    return jsonify(result)


@app.route('/api/procedural/borrow-book', methods=['POST'])
def procedural_borrow_book():
    """Borrow a book using procedural approach."""
    data = request.json
    result = procedural.borrow_book(
        data.get('member_id'),
        data.get('isbn')
    )
    return jsonify(result)


@app.route('/api/procedural/return-book', methods=['POST'])
def procedural_return_book():
    """Return a book using procedural approach."""
    data = request.json
    result = procedural.return_book(
        data.get('member_id'),
        data.get('isbn')
    )
    return jsonify(result)


@app.route('/api/procedural/books', methods=['GET'])
def procedural_get_books():
    """Get all books using procedural approach."""
    books = procedural.get_all_books()
    return jsonify({"books": books})


@app.route('/api/procedural/members', methods=['GET'])
def procedural_get_members():
    """Get all members using procedural approach."""
    members = procedural.get_all_members()
    return jsonify({"members": members})


@app.route('/api/procedural/available-books', methods=['GET'])
def procedural_get_available_books():
    """Get available books using procedural approach."""
    books = procedural.get_available_books()
    return jsonify({"books": books})


@app.route('/api/procedural/member-books/<member_id>', methods=['GET'])
def procedural_get_member_books(member_id):
    """Get books borrowed by a member using procedural approach."""
    books = procedural.get_member_borrowed_books(member_id)
    return jsonify({"books": books})


@app.route('/api/procedural/reset', methods=['POST'])
def procedural_reset():
    """Reset procedural library."""
    procedural.reset_library()
    return jsonify({"success": True, "message": "Library reset"})


# OOP Endpoints
@app.route('/api/oop/init', methods=['POST'])
def init_oop_library():
    """Initialize OOP library."""
    global oop_library
    oop_library = oop.Library()
    return jsonify({"success": True, "message": "OOP library initialized"})


@app.route('/api/oop/add-book', methods=['POST'])
def oop_add_book():
    """Add a book using OOP approach."""
    global oop_library
    if oop_library is None:
        oop_library = oop.Library()
    
    data = request.json
    result = oop_library.add_book(
        data.get('title'),
        data.get('author'),
        data.get('isbn')
    )
    return jsonify(result)


@app.route('/api/oop/add-member', methods=['POST'])
def oop_add_member():
    """Add a member using OOP approach."""
    global oop_library
    if oop_library is None:
        oop_library = oop.Library()
    
    data = request.json
    result = oop_library.add_member(
        data.get('name'),
        data.get('member_id')
    )
    return jsonify(result)


@app.route('/api/oop/borrow-book', methods=['POST'])
def oop_borrow_book():
    """Borrow a book using OOP approach."""
    global oop_library
    if oop_library is None:
        oop_library = oop.Library()
    
    data = request.json
    result = oop_library.borrow_book(
        data.get('member_id'),
        data.get('isbn')
    )
    return jsonify(result)


@app.route('/api/oop/return-book', methods=['POST'])
def oop_return_book():
    """Return a book using OOP approach."""
    global oop_library
    if oop_library is None:
        oop_library = oop.Library()
    
    data = request.json
    result = oop_library.return_book(
        data.get('member_id'),
        data.get('isbn')
    )
    return jsonify(result)


@app.route('/api/oop/books', methods=['GET'])
def oop_get_books():
    """Get all books using OOP approach."""
    global oop_library
    if oop_library is None:
        oop_library = oop.Library()
    
    books = oop_library.get_all_books()
    return jsonify({"books": books})


@app.route('/api/oop/members', methods=['GET'])
def oop_get_members():
    """Get all members using OOP approach."""
    global oop_library
    if oop_library is None:
        oop_library = oop.Library()
    
    members = oop_library.get_all_members()
    return jsonify({"members": members})


@app.route('/api/oop/available-books', methods=['GET'])
def oop_get_available_books():
    """Get available books using OOP approach."""
    global oop_library
    if oop_library is None:
        oop_library = oop.Library()
    
    books = oop_library.get_available_books()
    return jsonify({"books": books})


@app.route('/api/oop/member-books/<member_id>', methods=['GET'])
def oop_get_member_books(member_id):
    """Get books borrowed by a member using OOP approach."""
    global oop_library
    if oop_library is None:
        oop_library = oop.Library()
    
    books = oop_library.get_member_borrowed_books(member_id)
    return jsonify({"books": books})


@app.route('/api/oop/reset', methods=['POST'])
def oop_reset():
    """Reset OOP library."""
    global oop_library
    oop_library = oop.Library()
    return jsonify({"success": True, "message": "Library reset"})


if __name__ == '__main__':
    # Initialize both libraries
    init_procedural()
    init_oop()
    app.run(debug=True, port=5000)
