// Global state
let currentApproach = null; // 'procedural' or 'oop'
let currentStep = 0;

// Tutorial steps for each approach
const tutorialSteps = {
    procedural: [
        {
            title: "Understanding the Problem",
            description: "First, we identify what data structures we need. In procedural programming, we use dictionaries (objects) to store books and members, and lists to track transactions."
        },
        {
            title: "Global Data Structures",
            description: "We create global dictionaries: 'books' to store book information and 'members' to store member information. This is simple but can lead to data inconsistency issues."
        },
        {
            title: "Creating Functions",
            description: "We write separate functions for each operation: add_book(), add_member(), borrow_book(), return_book(). Each function directly manipulates the global data structures."
        },
        {
            title: "Data Access",
            description: "Functions directly access and modify global dictionaries. There's no encapsulation - any part of the code can accidentally modify the data incorrectly."
        },
        {
            title: "Testing the Implementation",
            description: "Now you can test the procedural approach using the interactive interface below. Try adding books, members, and performing operations."
        }
    ],
    oop: [
        {
            title: "Understanding the Problem in OOP Way",
            description: "In OOP, we think about the problem in terms of 'objects' and 'classes'. We identify entities: Book, Member, and Library. Each entity has its own data (attributes) and behaviors (methods)."
        },
        {
            title: "Identifying Classes",
            description: "We create three classes: Book (represents a book with title, author, ISBN, availability), Member (represents a member with name, ID, borrowed books), and Library (manages all books and members)."
        },
        {
            title: "Encapsulation",
            description: "Each class encapsulates its data (using private attributes with _ prefix) and provides controlled access through methods. For example, Book class has private _is_available attribute and public borrow()/return_book() methods."
        },
        {
            title: "Abstraction",
            description: "We hide complex implementation details. Users of the Book class don't need to know how availability is tracked internally - they just call borrow() or return_book() methods."
        },
        {
            title: "Coordination Through Library Class",
            description: "The Library class coordinates operations between Book and Member objects. When borrowing, it checks both the book's availability and member's borrowing limit, then updates both objects."
        },
        {
            title: "Benefits of OOP",
            description: "OOP provides: 1) Better organization (related data and functions together), 2) Data protection (private attributes), 3) Reusability (can create multiple Book/Member instances), 4) Easier maintenance (changes in one class don't affect others)."
        },
        {
            title: "Testing the Implementation",
            description: "Now you can test the OOP approach using the interactive interface below. Notice how the same operations work, but the code is more organized and maintainable."
        }
    ]
};

// Limitations for each approach
const limitations = {
    procedural: [
        {
            title: "Global State Management",
            description: "Global dictionaries can be modified from anywhere in the code, making it hard to track where changes occur and leading to potential bugs."
        },
        {
            title: "No Data Protection",
            description: "There's no way to prevent invalid data. For example, someone could directly set a book's availability without going through proper checks."
        },
        {
            title: "Code Organization",
            description: "As the program grows, functions become scattered and it's hard to see which functions operate on which data structures."
        },
        {
            title: "Difficult to Extend",
            description: "Adding new features (like different book types or member types) requires modifying multiple functions, increasing the risk of breaking existing code."
        },
        {
            title: "No Reusability",
            description: "Can't easily create multiple independent library instances. All data is in global scope, making it hard to test or use in different contexts."
        }
    ],
    oop: [
        {
            title: "Encapsulation Solves Data Protection",
            description: "Private attributes (_title, _is_available) prevent direct access. Data can only be modified through controlled methods, ensuring data integrity."
        },
        {
            title: "Better Organization",
            description: "Related data and functions are grouped together in classes. It's clear which methods belong to which entity, making code easier to understand and maintain."
        },
        {
            title: "Easy to Extend",
            description: "New features can be added by creating new classes (inheritance) or modifying existing ones without affecting other parts of the code."
        },
        {
            title: "Multiple Instances",
            description: "Can create multiple Library instances, each with its own books and members. This enables better testing and modularity."
        },
        {
            title: "Business Rules Enforcement",
            description: "Business rules (like borrowing limits) are enforced within the class methods, making it impossible to bypass them accidentally."
        }
    ]
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadProblemStatement();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('procedural-btn').addEventListener('click', () => selectApproach('procedural'));
    document.getElementById('oop-btn').addEventListener('click', () => selectApproach('oop'));
    
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const tabName = e.target.dataset.tab;
            switchTab(tabName);
        });
    });
    
    // Code tabs
    document.querySelectorAll('.code-tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const codeType = e.target.dataset.code;
            switchCodeTab(codeType);
        });
    });
}

async function loadProblemStatement() {
    try {
        const response = await fetch('/api/problem-statement');
        const data = await response.json();
        document.getElementById('problem-content').textContent = data.description.trim();
    } catch (error) {
        console.error('Error loading problem statement:', error);
        document.getElementById('problem-content').textContent = 'Error loading problem statement.';
    }
}

function selectApproach(approach) {
    currentApproach = approach;
    currentStep = 0;
    
    // Initialize the library
    initializeLibrary(approach);
    
    // Show tutorial section
    document.getElementById('tutorial-section').style.display = 'block';
    document.getElementById('interactive-section').style.display = 'block';
    document.getElementById('limitations-section').style.display = 'block';
    document.getElementById('code-section').style.display = 'block';
    
    // Load tutorial steps
    loadTutorialSteps(approach);
    
    // Load limitations
    loadLimitations(approach);
    
    // Load code examples
    loadCodeExamples(approach);
    
    // Scroll to tutorial
    document.getElementById('tutorial-section').scrollIntoView({ behavior: 'smooth' });
}

async function initializeLibrary(approach) {
    try {
        const endpoint = approach === 'procedural' ? '/api/procedural/init' : '/api/oop/init';
        await fetch(endpoint, { method: 'POST' });
    } catch (error) {
        console.error('Error initializing library:', error);
    }
}

function loadTutorialSteps(approach) {
    const steps = tutorialSteps[approach];
    const container = document.getElementById('steps-container');
    const title = document.getElementById('tutorial-title');
    
    title.textContent = approach === 'procedural' 
        ? 'Procedural/Functional Programming Approach - Step by Step'
        : 'Object-Oriented Programming Approach - Step by Step';
    
    container.innerHTML = steps.map((step, index) => `
        <div class="step">
            <span class="step-number">${index + 1}</span>
            <div>
                <div class="step-title">${step.title}</div>
                <div class="step-description">${step.description}</div>
            </div>
        </div>
    `).join('');
}

function loadLimitations(approach) {
    const items = limitations[approach];
    const container = document.getElementById('limitations-content');
    const title = document.getElementById('limitations-title');
    
    if (approach === 'procedural') {
        title.textContent = 'Limitations of Procedural/Functional Approach';
        container.innerHTML = items.map(item => `
            <div class="limitation-item">
                <div class="limitation-title">⚠️ ${item.title}</div>
                <div class="limitation-description">${item.description}</div>
            </div>
        `).join('');
    } else {
        title.textContent = 'How OOP Solves These Problems';
        container.innerHTML = items.map(item => `
            <div class="solution-item">
                <div class="solution-title">✅ ${item.title}</div>
                <div class="solution-description">${item.description}</div>
            </div>
        `).join('');
    }
}

async function loadCodeExamples(approach) {
    // For now, we'll show a simplified version
    // In a real implementation, you might want to load actual code files
    const codeContainer = document.getElementById('code-content');
    
    if (approach === 'procedural') {
        codeContainer.innerHTML = `
            <pre># Procedural Approach Example

# Global data structures
books = {}
members = {}

def add_book(title, author, isbn):
    books[isbn] = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "is_available": True
    }

def borrow_book(member_id, isbn):
    books[isbn]["is_available"] = False
    members[member_id]["borrowed_books"].append(isbn)
        </pre>
        `;
    } else {
        codeContainer.innerHTML = `
            <pre># OOP Approach Example

class Book:
    def __init__(self, title, author, isbn):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._is_available = True
    
    def borrow(self, member_id):
        if not self._is_available:
            return False
        self._is_available = False
        return True

class Library:
    def __init__(self):
        self._books = {}
        self._members = {}
    
    def borrow_book(self, member_id, isbn):
        book = self._books[isbn]
        member = self._members[member_id]
        if book.borrow(member_id):
            member.add_borrowed_book(isbn)
        </pre>
        `;
    }
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Add active class to button
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Load data for the tab
    if (tabName === 'books') {
        loadBooks();
    } else if (tabName === 'members') {
        loadMembers();
    }
}

function switchCodeTab(codeType) {
    document.querySelectorAll('.code-tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-code="${codeType}"]`).classList.add('active');
    loadCodeExamples(codeType === 'procedural' ? 'procedural' : 'oop');
}

// API Functions
async function addBook() {
    if (!currentApproach) {
        showMessage('Please select an approach first!', 'error');
        return;
    }
    
    const title = document.getElementById('book-title').value;
    const author = document.getElementById('book-author').value;
    const isbn = document.getElementById('book-isbn').value;
    
    if (!title || !author || !isbn) {
        showMessage('Please fill in all fields!', 'error');
        return;
    }
    
    try {
        const endpoint = currentApproach === 'procedural' 
            ? '/api/procedural/add-book' 
            : '/api/oop/add-book';
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, author, isbn })
        });
        
        const result = await response.json();
        showMessage(result.message, result.success ? 'success' : 'error');
        
        if (result.success) {
            document.getElementById('book-title').value = '';
            document.getElementById('book-author').value = '';
            document.getElementById('book-isbn').value = '';
            loadBooks();
        }
    } catch (error) {
        showMessage('Error adding book: ' + error.message, 'error');
    }
}

async function addMember() {
    if (!currentApproach) {
        showMessage('Please select an approach first!', 'error');
        return;
    }
    
    const name = document.getElementById('member-name').value;
    const memberId = document.getElementById('member-id').value;
    
    if (!name || !memberId) {
        showMessage('Please fill in all fields!', 'error');
        return;
    }
    
    try {
        const endpoint = currentApproach === 'procedural' 
            ? '/api/procedural/add-member' 
            : '/api/oop/add-member';
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, member_id: memberId })
        });
        
        const result = await response.json();
        showMessage(result.message, result.success ? 'success' : 'error');
        
        if (result.success) {
            document.getElementById('member-name').value = '';
            document.getElementById('member-id').value = '';
            loadMembers();
        }
    } catch (error) {
        showMessage('Error adding member: ' + error.message, 'error');
    }
}

async function borrowBook() {
    if (!currentApproach) {
        showMessage('Please select an approach first!', 'error');
        return;
    }
    
    const memberId = document.getElementById('borrow-member-id').value;
    const isbn = document.getElementById('borrow-isbn').value;
    
    if (!memberId || !isbn) {
        showMessage('Please fill in all fields!', 'error');
        return;
    }
    
    try {
        const endpoint = currentApproach === 'procedural' 
            ? '/api/procedural/borrow-book' 
            : '/api/oop/borrow-book';
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ member_id: memberId, isbn })
        });
        
        const result = await response.json();
        showMessage(result.message, result.success ? 'success' : 'error', 'operations-messages');
        
        if (result.success) {
            document.getElementById('borrow-member-id').value = '';
            document.getElementById('borrow-isbn').value = '';
            loadBooks();
            loadMembers();
        }
    } catch (error) {
        showMessage('Error borrowing book: ' + error.message, 'error', 'operations-messages');
    }
}

async function returnBook() {
    if (!currentApproach) {
        showMessage('Please select an approach first!', 'error');
        return;
    }
    
    const memberId = document.getElementById('return-member-id').value;
    const isbn = document.getElementById('return-isbn').value;
    
    if (!memberId || !isbn) {
        showMessage('Please fill in all fields!', 'error');
        return;
    }
    
    try {
        const endpoint = currentApproach === 'procedural' 
            ? '/api/procedural/return-book' 
            : '/api/oop/return-book';
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ member_id: memberId, isbn })
        });
        
        const result = await response.json();
        showMessage(result.message, result.success ? 'success' : 'error', 'operations-messages');
        
        if (result.success) {
            document.getElementById('return-member-id').value = '';
            document.getElementById('return-isbn').value = '';
            loadBooks();
            loadMembers();
        }
    } catch (error) {
        showMessage('Error returning book: ' + error.message, 'error', 'operations-messages');
    }
}

async function loadBooks() {
    if (!currentApproach) return;
    
    try {
        const endpoint = currentApproach === 'procedural' 
            ? '/api/procedural/books' 
            : '/api/oop/books';
        
        const response = await fetch(endpoint);
        const data = await response.json();
        
        const container = document.getElementById('books-list');
        
        if (data.books.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #666;">No books added yet. Add your first book above!</p>';
            return;
        }
        
        container.innerHTML = data.books.map(book => `
            <div class="list-item">
                <div class="list-item-info">
                    <div class="list-item-title">${book.title}</div>
                    <div class="list-item-detail">Author: ${book.author} | ISBN: ${book.isbn}</div>
                </div>
                <span class="status-badge ${book.is_available ? 'status-available' : 'status-borrowed'}">
                    ${book.is_available ? 'Available' : 'Borrowed'}
                </span>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading books:', error);
    }
}

async function loadMembers() {
    if (!currentApproach) return;
    
    try {
        const endpoint = currentApproach === 'procedural' 
            ? '/api/procedural/members' 
            : '/api/oop/members';
        
        const response = await fetch(endpoint);
        const data = await response.json();
        
        const container = document.getElementById('members-list');
        
        if (data.members.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #666;">No members registered yet. Add your first member above!</p>';
            return;
        }
        
        container.innerHTML = data.members.map(member => `
            <div class="list-item">
                <div class="list-item-info">
                    <div class="list-item-title">${member.name}</div>
                    <div class="list-item-detail">Member ID: ${member.member_id} | Borrowed: ${member.borrowed_count || member.borrowed_books?.length || 0} book(s)</div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading members:', error);
    }
}

function showMessage(message, type, containerId = null) {
    const container = containerId 
        ? document.getElementById(containerId)
        : document.getElementById('operations-messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    container.appendChild(messageDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

async function resetLibrary() {
    if (!currentApproach) {
        showMessage('Please select an approach first!', 'error');
        return;
    }
    
    if (!confirm('Are you sure you want to reset the library? All data will be lost.')) {
        return;
    }
    
    try {
        const endpoint = currentApproach === 'procedural' 
            ? '/api/procedural/reset' 
            : '/api/oop/reset';
        
        await fetch(endpoint, { method: 'POST' });
        
        // Re-initialize
        await initializeLibrary(currentApproach);
        
        // Reload data
        loadBooks();
        loadMembers();
        
        // Clear messages
        document.getElementById('operations-messages').innerHTML = '';
        
        showMessage('Library reset successfully!', 'success');
    } catch (error) {
        showMessage('Error resetting library: ' + error.message, 'error');
    }
}
