import React, { useEffect, useState, useMemo } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const API = '/api';

const PRESET_CATEGORIES = [
  'Computer Science',
  'DevOps & Cloud',
  'Software Architecture',
  'Algorithms & Data Structures',
  'Artificial Intelligence',
  'Mathematics',
  'Literature',
];

function App() {
  const [books, setBooks] = useState([]);
  const [stats, setStats] = useState({ total: 0, available: 0, borrowed: 0, overdue: 0 });
  const [healthStatus, setHealthStatus] = useState('CHECKING');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [categoryFilter, setCategoryFilter] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notification, setNotification] = useState(null);

  // Modals state
  const [showAddModal, setShowAddModal] = useState(false);
  const [checkoutTarget, setCheckoutTarget] = useState(null);
  const [checkoutBorrower, setCheckoutBorrower] = useState('');
  const [checkoutDays, setCheckoutDays] = useState(14);

  const notify = (message, type = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 4000);
  };

  const fetchHealth = async () => {
    try {
      const res = await fetch('/health');
      if (res.ok) {
        setHealthStatus('ONLINE');
      } else {
        setHealthStatus('OFFLINE');
      }
    } catch {
      setHealthStatus('OFFLINE');
    }
  };

  const loadData = async () => {
    try {
      setError('');
      fetchHealth();
      const [booksRes, statsRes] = await Promise.all([
        fetch(`${API}/books`),
        fetch(`${API}/books/stats`),
      ]);

      if (!booksRes.ok || !statsRes.ok) {
        throw new Error(`API Error: ${booksRes.status} / ${statsRes.status}`);
      }

      const booksData = await booksRes.json();
      const statsData = await statsRes.json();

      setBooks(booksData);
      setStats(statsData);
    } catch (err) {
      setError(err.message || 'Failed to connect to BookFlow backend');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(fetchHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleCreateBook = async (e) => {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    const title = form.get('title')?.toString().trim();
    const author = form.get('author')?.toString().trim();
    const category = form.get('category')?.toString().trim();

    if (!title || !author || !category) {
      notify('All fields are required', 'error');
      return;
    }

    try {
      const res = await fetch(`${API}/books`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, author, category }),
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Failed to add book');
      }
      setShowAddModal(false);
      notify(`Book "${title}" added successfully!`);
      loadData();
    } catch (err) {
      notify(err.message, 'error');
    }
  };

  const handleCheckout = async (e) => {
    e.preventDefault();
    if (!checkoutTarget) return;

    if (!checkoutBorrower.trim()) {
      notify('Student borrower name is required', 'error');
      return;
    }

    try {
      const res = await fetch(`${API}/books/${checkoutTarget.id}/checkout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          borrower_name: checkoutBorrower.trim(),
          loan_days: Number(checkoutDays) || 14,
        }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Checkout failed');
      }

      notify(`"${checkoutTarget.title}" loaned to ${checkoutBorrower}`);
      setCheckoutTarget(null);
      setCheckoutBorrower('');
      setCheckoutDays(14);
      loadData();
    } catch (err) {
      notify(err.message, 'error');
    }
  };

  const handleReturn = async (book) => {
    try {
      const res = await fetch(`${API}/books/${book.id}/return`, {
        method: 'POST',
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Return failed');
      }
      notify(`"${book.title}" returned to library shelf`);
      loadData();
    } catch (err) {
      notify(err.message, 'error');
    }
  };

  const handleDelete = async (book) => {
    if (!window.confirm(`Are you sure you want to remove "${book.title}" from the catalogue?`)) {
      return;
    }
    try {
      const res = await fetch(`${API}/books/${book.id}`, { method: 'DELETE' });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Delete failed');
      }
      notify(`"${book.title}" removed from catalogue`);
      loadData();
    } catch (err) {
      notify(err.message, 'error');
    }
  };

  const isOverdue = (book) => {
    if (book.status !== 'BORROWED' || !book.due_date) return false;
    const today = new Date().toISOString().split('T')[0];
    return book.due_date < today;
  };

  const filteredBooks = useMemo(() => {
    return books.filter((b) => {
      // Status filter
      if (statusFilter === 'AVAILABLE' && b.status !== 'AVAILABLE') return false;
      if (statusFilter === 'BORROWED' && b.status !== 'BORROWED') return false;
      if (statusFilter === 'OVERDUE' && !isOverdue(b)) return false;

      // Category filter
      if (categoryFilter !== 'ALL' && b.category !== categoryFilter) return false;

      // Search query
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const titleMatch = b.title.toLowerCase().includes(q);
        const authorMatch = b.author.toLowerCase().includes(q);
        const borrowerMatch = b.borrower_name?.toLowerCase().includes(q);
        const catMatch = b.category.toLowerCase().includes(q);
        return titleMatch || authorMatch || borrowerMatch || catMatch;
      }

      return true;
    });
  }, [books, statusFilter, categoryFilter, searchQuery]);

  return (
    <div className="bookflow-app">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-logo">📚</div>
          <div className="brand-info">
            <h2>BookFlow</h2>
            <span className="brand-tag">Library Tracker</span>
          </div>
        </div>

        <nav className="nav-menu">
          <button
            className={`nav-item ${statusFilter === 'ALL' ? 'active' : ''}`}
            onClick={() => {
              setStatusFilter('ALL');
              setCategoryFilter('ALL');
            }}
          >
            <span className="nav-icon">📖</span>
            <span>All Books</span>
            <span className="badge">{stats.total}</span>
          </button>
          <button
            className={`nav-item ${statusFilter === 'AVAILABLE' ? 'active' : ''}`}
            onClick={() => setStatusFilter('AVAILABLE')}
          >
            <span className="nav-icon">🟢</span>
            <span>Available</span>
            <span className="badge success">{stats.available}</span>
          </button>
          <button
            className={`nav-item ${statusFilter === 'BORROWED' ? 'active' : ''}`}
            onClick={() => setStatusFilter('BORROWED')}
          >
            <span className="nav-icon">📤</span>
            <span>On Loan</span>
            <span className="badge warning">{stats.borrowed}</span>
          </button>
          <button
            className={`nav-item ${statusFilter === 'OVERDUE' ? 'active' : ''}`}
            onClick={() => setStatusFilter('OVERDUE')}
          >
            <span className="nav-icon">⚠️</span>
            <span>Overdue</span>
            <span className="badge danger">{stats.overdue}</span>
          </button>
        </nav>

        <div className="sidebar-footer">
          <div className="system-health">
            <span className={`status-dot ${healthStatus === 'ONLINE' ? 'online' : 'offline'}`}></span>
            <div>
              <strong>Backend Service</strong>
              <small>{healthStatus === 'ONLINE' ? 'Port 8000 Healthy' : 'Disconnected'}</small>
            </div>
          </div>
          <div className="architecture-box">
            <span className="arch-label">SST DevOps Capstone</span>
            <p>FastAPI • Postgres • Helm • EKS</p>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        {notification && (
          <div className={`toast toast-${notification.type}`}>
            <span>{notification.type === 'success' ? '✓' : '⚠'}</span>
            <p>{notification.message}</p>
          </div>
        )}

        <header className="page-header">
          <div>
            <div className="breadcrumbs">CAMPUS LIBRARY / CATALOGUE & CIRCULATION</div>
            <h1>Student Lending Desk</h1>
            <p className="subtitle">
              Manage student book loans, track return due dates, and monitor library circulation.
            </p>
          </div>
          <div className="header-actions">
            <button className="btn-refresh" onClick={loadData} title="Refresh Catalogue">
              ↻ Refresh
            </button>
            <button className="btn-primary" onClick={() => setShowAddModal(true)}>
              + Add New Book
            </button>
          </div>
        </header>

        {error && (
          <div className="error-banner">
            <span>⚠️</span>
            <div>
              <strong>Backend Connection Issue:</strong> {error}
              <p>Verify that FastAPI backend is running on port 8000 and PostgreSQL is accessible.</p>
            </div>
            <button onClick={loadData}>Retry</button>
          </div>
        )}

        {/* KPI Stats Cards */}
        <section className="stats-grid">
          <div className="stat-card" onClick={() => setStatusFilter('ALL')}>
            <div className="stat-icon icon-total">📚</div>
            <div className="stat-details">
              <span className="stat-label">Total Books</span>
              <strong className="stat-value">{stats.total}</strong>
              <span className="stat-sub">Full catalogue catalogued</span>
            </div>
          </div>
          <div className="stat-card" onClick={() => setStatusFilter('AVAILABLE')}>
            <div className="stat-icon icon-available">🟢</div>
            <div className="stat-details">
              <span className="stat-label">Available on Shelves</span>
              <strong className="stat-value">{stats.available}</strong>
              <span className="stat-sub">Ready for loan</span>
            </div>
          </div>
          <div className="stat-card" onClick={() => setStatusFilter('BORROWED')}>
            <div className="stat-icon icon-borrowed">📖</div>
            <div className="stat-details">
              <span className="stat-label">Active Loans</span>
              <strong className="stat-value">{stats.borrowed}</strong>
              <span className="stat-sub">Currently borrowed</span>
            </div>
          </div>
          <div className="stat-card" onClick={() => setStatusFilter('OVERDUE')}>
            <div className="stat-icon icon-overdue">⚠️</div>
            <div className="stat-details">
              <span className="stat-label">Overdue Books</span>
              <strong className="stat-value">{stats.overdue}</strong>
              <span className="stat-sub">Exceeded due date</span>
            </div>
          </div>
        </section>

        {/* Filter and Search Bar */}
        <section className="controls-bar">
          <div className="search-box">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="Search by title, author, or student name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            {searchQuery && (
              <button className="search-clear" onClick={() => setSearchQuery('')}>
                ×
              </button>
            )}
          </div>

          <div className="filter-select-wrap">
            <label htmlFor="cat-filter">Category:</label>
            <select
              id="cat-filter"
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
            >
              <option value="ALL">All Categories</option>
              {PRESET_CATEGORIES.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          <div className="status-pills">
            {['ALL', 'AVAILABLE', 'BORROWED', 'OVERDUE'].map((s) => (
              <button
                key={s}
                className={`pill-btn ${statusFilter === s ? 'active' : ''}`}
                onClick={() => setStatusFilter(s)}
              >
                {s === 'ALL' ? 'All' : s.charAt(0) + s.slice(1).toLowerCase()}
              </button>
            ))}
          </div>
        </section>

        {/* Books Catalogue Table */}
        <section className="table-container">
          {loading ? (
            <div className="empty-state">
              <div className="spinner"></div>
              <p>Loading library catalogue from database...</p>
            </div>
          ) : filteredBooks.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📭</div>
              <h3>No books match your criteria</h3>
              <p>Try resetting filters or search terms, or add a new book to the catalogue.</p>
              <button
                className="btn-secondary"
                onClick={() => {
                  setStatusFilter('ALL');
                  setCategoryFilter('ALL');
                  setSearchQuery('');
                }}
              >
                Reset All Filters
              </button>
            </div>
          ) : (
            <table className="books-table">
              <thead>
                <tr>
                  <th>Book Details</th>
                  <th>Category</th>
                  <th>Lending Status</th>
                  <th>Borrower / Due Date</th>
                  <th style={{ textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredBooks.map((book) => {
                  const overdue = isOverdue(book);
                  return (
                    <tr key={book.id} className={overdue ? 'row-overdue' : ''}>
                      <td>
                        <div className="book-title-cell">
                          <span className="book-icon">📕</span>
                          <div>
                            <strong className="book-title">{book.title}</strong>
                            <span className="book-author">by {book.author}</span>
                          </div>
                        </div>
                      </td>
                      <td>
                        <span className="category-tag">{book.category}</span>
                      </td>
                      <td>
                        {book.status === 'AVAILABLE' ? (
                          <span className="status-badge badge-available">
                            <span className="dot"></span> Available
                          </span>
                        ) : overdue ? (
                          <span className="status-badge badge-overdue">
                            <span className="dot"></span> Overdue Loan
                          </span>
                        ) : (
                          <span className="status-badge badge-borrowed">
                            <span className="dot"></span> Borrowed
                          </span>
                        )}
                      </td>
                      <td>
                        {book.status === 'BORROWED' ? (
                          <div className="borrower-info">
                            <strong className="borrower-name">{book.borrower_name}</strong>
                            <small className={`due-date ${overdue ? 'date-overdue' : ''}`}>
                              Due: {book.due_date} {overdue ? '(Overdue!)' : ''}
                            </small>
                          </div>
                        ) : (
                          <span className="text-muted">— In Library —</span>
                        )}
                      </td>
                      <td>
                        <div className="actions-cell">
                          {book.status === 'AVAILABLE' ? (
                            <button
                              className="btn-action btn-checkout"
                              onClick={() => {
                                setCheckoutTarget(book);
                                setCheckoutBorrower('');
                                setCheckoutDays(14);
                              }}
                            >
                              Loan Out
                            </button>
                          ) : (
                            <button
                              className="btn-action btn-return"
                              onClick={() => handleReturn(book)}
                            >
                              Return
                            </button>
                          )}
                          <button
                            className="btn-action-icon"
                            title="Delete Book"
                            onClick={() => handleDelete(book)}
                          >
                            🗑
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </section>
      </main>

      {/* Modal: Add Book */}
      {showAddModal && (
        <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Add New Book to Library</h3>
              <button className="modal-close" onClick={() => setShowAddModal(false)}>
                ×
              </button>
            </div>
            <form onSubmit={handleCreateBook}>
              <div className="modal-body">
                <label className="form-group">
                  <span>Book Title:</span>
                  <input
                    name="title"
                    required
                    placeholder="e.g. Designing Data-Intensive Applications"
                  />
                </label>
                <label className="form-group">
                  <span>Author:</span>
                  <input name="author" required placeholder="e.g. Martin Kleppmann" />
                </label>
                <label className="form-group">
                  <span>Category:</span>
                  <select name="category" required defaultValue="Computer Science">
                    {PRESET_CATEGORIES.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => setShowAddModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Add to Catalogue
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Checkout / Loan Book */}
      {checkoutTarget && (
        <div className="modal-overlay" onClick={() => setCheckoutTarget(null)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Loan Book to Student</h3>
              <button className="modal-close" onClick={() => setCheckoutTarget(null)}>
                ×
              </button>
            </div>
            <form onSubmit={handleCheckout}>
              <div className="modal-body">
                <div className="target-book-summary">
                  <span className="summary-icon">📖</span>
                  <div>
                    <strong>{checkoutTarget.title}</strong>
                    <small>by {checkoutTarget.author}</small>
                  </div>
                </div>

                <label className="form-group">
                  <span>Student Borrower Name:</span>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Aarav Sharma (Roll #2024-CS-042)"
                    value={checkoutBorrower}
                    onChange={(e) => setCheckoutBorrower(e.target.value)}
                    autoFocus
                  />
                </label>

                <label className="form-group">
                  <span>Loan Duration:</span>
                  <select
                    value={checkoutDays}
                    onChange={(e) => setCheckoutDays(Number(e.target.value))}
                  >
                    <option value={7}>7 Days (Short Loan)</option>
                    <option value={14}>14 Days (Standard Loan)</option>
                    <option value={21}>21 Days (Extended Loan)</option>
                    <option value={30}>30 Days (Semester Special)</option>
                  </select>
                </label>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => setCheckoutTarget(null)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Confirm Loan
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
